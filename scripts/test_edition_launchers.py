"""Exercise independent edition launchers, including nine local HTTP smokes."""
from __future__ import annotations

import argparse
from contextlib import closing, redirect_stdout
from datetime import datetime, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import URLError
from urllib.request import build_opener, ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
EDITIONS = ('Alpha-v0.1.0-Alkimim', 'Alpha-v0.2.0-Alkimim', 'Stable-v1.0.0')
PROJECTS = ('board-crm', 'tiny-catalog', 'work-board')
CATALOG = 'board-crm  (port 8001)\ntiny-catalog  (port 8000)\nwork-board  (port 8002)\n'
RECORDS = []


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


class LauncherChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix='oal-launchers-', dir=os.environ.get('OAL_TEST_TMPDIR'))
        cls.temp = Path(cls.workspace.name)
        cls.unrelated = cls.temp / 'unrelated'
        cls.unrelated.mkdir()
        cls.copies = {}
        for i, edition in enumerate(EDITIONS):
            destination = cls.temp / f'renamed-{i}'
            shutil.copytree(ROOT / 'versioning' / edition, destination,
                            ignore=shutil.ignore_patterns('data', '__pycache__', '.pytest_cache', '.venv', '*.sqlite3'))
            cls.copies[edition] = destination

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def invoke(self, script, args, cwd, expected=0):
        command = [sys.executable, str(script), *args]
        started = now()
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding='utf-8', timeout=20)
        RECORDS.append({'kind': 'cli', 'started_at': started, 'finished_at': now(),
                        'command': command, 'working_directory': str(cwd),
                        'exit_code': result.returncode, 'expected_exit_code': expected,
                        'stdout': result.stdout, 'stderr': result.stderr})
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def catalog_help(self, edition):
        local = ROOT / 'versioning' / edition
        isolated = self.copies[edition]
        for script, cwd in ((local / 'run_examples.py', ROOT),
                            (Path('run_examples.py'), local),
                            (local / 'run_examples.py', self.unrelated),
                            (isolated / 'run_examples.py', self.unrelated)):
            with self.subTest(cwd=cwd, script=script):
                self.assertEqual(self.invoke(script, ['--list'], cwd).stdout, CATALOG)
                self.assertIn(edition, self.invoke(script, ['--help'], cwd).stdout)
        for project in PROJECTS:
            result = self.invoke(isolated / 'run_examples.py', [project, '--help'], self.unrelated)
            self.assertIn(f'{edition}/{project}', result.stdout)
            for flag in ('--port', '--database', '--no-browser'):
                self.assertIn(flag, result.stdout)

    def invalid_selections(self, edition):
        script = self.copies[edition] / 'run_examples.py'
        foreign = next(item for item in EDITIONS if item != edition)
        for name in ('missing-example', f'{foreign}/tiny-catalog', f'{edition}/tiny-catalog'):
            result = self.invoke(script, [name], self.unrelated, expected=1)
            self.assertIn(f'Unknown example in {edition}', result.stderr)
            self.assertIn('Use a bare NAME', result.stderr)
        for port in ('0', '65536', 'invalid'):
            self.invoke(script, ['tiny-catalog', '--port', port, '--no-browser'], self.unrelated, expected=2)
        self.invoke(script, [], self.unrelated, expected=2)

    def controls(self, edition):
        """Check default browser, loopback, and graceful Ctrl+C without opening UI."""
        script = self.copies[edition] / 'run_examples.py'
        spec = importlib.util.spec_from_file_location('launcher_under_test', script)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {spec.name: module}):
            spec.loader.exec_module(module)
        example = module.resolve('tiny-catalog', module.discover())
        factory = MagicMock()
        server = MagicMock()
        server.__enter__.return_value.serve_forever.side_effect = KeyboardInterrupt
        output = io.StringIO()
        with patch.object(module, 'import_module', return_value=MagicMock(**{example.entrypoint.split(':')[1]: factory})), \
             patch.object(module, 'make_server', return_value=server) as make_server, \
             patch.object(module, 'Timer') as timer, patch.object(sys, 'path', list(sys.path)), redirect_stdout(output):
            self.assertEqual(module.PythonWSGIExecutor().run(example, []), 0)
            factory.assert_called_once_with(script.parent / 'data' / example.database_name)
            self.assertEqual(sys.path[0], str(example.directory / 'src'))
            make_server.assert_called_once_with('127.0.0.1', example.default_port, factory.return_value)
            timer.return_value.start.assert_called_once()
            self.assertIn('Stopped.', output.getvalue())
            timer.reset_mock()
            module.PythonWSGIExecutor().run(example, ['--no-browser'])
            timer.assert_not_called()

    def http_smoke(self, edition, project):
        isolated = self.copies[edition]
        metadata = json.loads((isolated / 'examples' / project / 'runner.json').read_text(encoding='utf-8'))
        # Absolute legacy path, cwd-relative legacy path, then edition-local default.
        legacy = self.temp / 'data' / edition / metadata['database_name']
        cwd = self.unrelated
        if project == 'board-crm':
            database = legacy
            database_args = ['--database', str(database)]
            mode = 'absolute-existing'
        elif project == 'tiny-catalog':
            database = legacy
            database_args = ['--database', os.path.relpath(database, cwd)]
            mode = 'relative-existing'
        else:
            database = isolated / 'data' / metadata['database_name']
            database_args = []
            mode = 'edition-default'
        database.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(database)) as connection, connection:
            connection.execute('CREATE TABLE launcher_preservation_marker(value TEXT)')
            connection.execute("INSERT INTO launcher_preservation_marker VALUES ('keep-existing-data')")
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        command = [sys.executable, str(isolated / 'run_examples.py'), project, '--port', str(port), '--no-browser', *database_args]
        record = {'kind': 'http-smoke', 'edition': edition, 'example': project, 'command': command,
                  'working_directory': str(cwd), 'database': str(database), 'database_mode': mode,
                  'started_at': now(), 'browser_javascript_tested': False}
        log_path = self.temp / f'{edition}-{project}.log'
        process = None
        try:
            with log_path.open('w', encoding='utf-8') as log:
                process = subprocess.Popen(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
                record['process_id'] = process.pid
                opener = build_opener(ProxyHandler({}))
                deadline = time.monotonic() + 20
                while True:
                    try:
                        with opener.open(f'http://127.0.0.1:{port}/', timeout=1) as response:
                            body = response.read()
                            self.assertEqual(response.status, 200)
                            self.assertIn(b'<html', body.lower())
                            record.update(http_status=response.status, response_bytes=len(body))
                            break
                    except (URLError, TimeoutError) as error:
                        if isinstance(getattr(error, 'reason', None), PermissionError):
                            raise
                        self.assertIsNone(process.poll(), 'server exited before HTTP response')
                        if time.monotonic() >= deadline:
                            self.fail('server did not respond within 20 seconds')
                        time.sleep(0.1)
                with closing(sqlite3.connect(database)) as connection:
                    self.assertEqual(connection.execute('SELECT value FROM launcher_preservation_marker').fetchone(), ('keep-existing-data',))
                record['existing_database_preserved'] = True
        finally:
            if process is not None:
                if process.poll() is None:
                    if os.name == 'nt':
                        # Windows virtual-environment executables may launch a child.
                        stopped = subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                                 capture_output=True, text=True, timeout=10)
                        record['termination_method'] = 'taskkill /PID <spawned PID> /T /F'
                        record['termination_command_exit_code'] = stopped.returncode
                    else:
                        process.terminate()
                        record['termination_method'] = 'SIGTERM'
                try:
                    record['exit_code_after_termination'] = process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    record['exit_code_after_termination'] = process.wait(timeout=5)
                record['terminated'] = process.poll() is not None
            record['finished_at'] = now()
            record['log'] = log_path.read_text(encoding='utf-8') if log_path.exists() else ''
            RECORDS.append(record)
        self.assertIn(f'{edition}/{project}', record['log'])
        self.assertTrue(record['terminated'])
        with self.assertRaises(URLError):
            opener.open(f'http://127.0.0.1:{port}/', timeout=1)
        record['port_closed_after_termination'] = True


for index, edition in enumerate(EDITIONS):
    for check in ('catalog_help', 'invalid_selections', 'controls'):
        def test(self, edition=edition, check=check):
            getattr(self, check)(edition)
        setattr(LauncherChecks, f'test_{index}_{check}', test)
    for project in PROJECTS:
        def test(self, edition=edition, project=project):
            self.http_smoke(edition, project)
        setattr(LauncherChecks, f'test_{index}_http_{project.replace("-", "_")}', test)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LauncherChecks))
    if args.report:
        args.report.write_text(json.dumps({'status': 'passed' if result.wasSuccessful() else 'failed',
            'tests_run': result.testsRun, 'records': RECORDS,
            'limits': 'HTTP and process termination only; no browser JavaScript or visual accessibility. Ctrl+C/browser controls are mocked, not OS signal/UI integration tests.'}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
