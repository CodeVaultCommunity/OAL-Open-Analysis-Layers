const board = document.querySelector('#board');
const message = document.querySelector('#message');
const projectFilter = document.querySelector('#filter-project');

async function api(path, options = {}) {
  const response = await fetch(path, { ...options, headers: { 'Content-Type': 'application/json', ...(options.headers || {}) } });
  const result = await response.json();
  if (!response.ok) throw new Error(result.message || result.error || `HTTP ${response.status}`);
  return result;
}

function control(label, onClick) {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = label;
  button.addEventListener('click', onClick);
  return button;
}

async function run(action) {
  try { message.textContent = ''; await action(); await load(); }
  catch (error) { message.textContent = error.message; }
}

function card(item) {
  const article = document.createElement('article');
  article.className = 'card';
  const heading = document.createElement('h3');
  heading.textContent = item.title;
  const details = document.createElement('small');
  details.textContent = `${item.project} · ${item.priority} · ${item.assignee || 'unassigned'} · v${item.version}`;
  const description = document.createElement('p');
  description.textContent = item.description;
  const actions = document.createElement('div');
  actions.className = 'actions';
  actions.append(control('Assign', () => run(async () => {
    const assignee = (window.prompt('Assignee') || '').trim();
    if (!assignee) return;
    if (assignee.length > 80) throw new Error('Assignee must have at most 80 characters.');
    await api(`/api/items/${encodeURIComponent(item.id)}/assign`, { method: 'POST', body: JSON.stringify({ assignee, expected_version: item.version }) });
  })));
  if (item.status !== 'done') actions.append(control('Advance', () => run(async () => {
    const status = item.status === 'backlog' ? 'in_progress' : 'done';
    await api(`/api/items/${encodeURIComponent(item.id)}/transition`, { method: 'POST', body: JSON.stringify({ status, expected_version: item.version }) });
  })));
  actions.append(control('Comment', () => run(async () => {
    const body = (window.prompt('Comment') || '').trim();
    if (!body) return;
    if (body.length > 1000) throw new Error('Comment must have at most 1000 characters.');
    await api(`/api/items/${encodeURIComponent(item.id)}/comments`, { method: 'POST', body: JSON.stringify({ body }) });
  })));
  actions.append(control('Read comments', async () => {
    try {
      const result = await api(`/api/items/${encodeURIComponent(item.id)}/comments`);
      message.textContent = result.comments.map(comment => `${comment.author}: ${comment.body}`).join(' | ') || 'No comments yet.';
    } catch (error) { message.textContent = error.message; }
  }));
  article.append(heading, details, description, actions);
  return article;
}

async function load() {
  try {
    const query = projectFilter.value.trim() ? `?project=${encodeURIComponent(projectFilter.value.trim())}` : '';
    const result = await api(`/api/items${query}`);
    board.replaceChildren();
    for (const status of ['backlog', 'in_progress', 'done']) {
      const column = document.createElement('section');
      column.className = 'column';
      const heading = document.createElement('h3');
      heading.textContent = status.replace('_', ' ');
      column.append(heading, ...result.items.filter(item => item.status === status).map(card));
      board.append(column);
    }
  } catch (error) { message.textContent = error.message; }
}

document.querySelector('#create-form').addEventListener('submit', event => run(async () => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form));
  await api('/api/items', { method: 'POST', body: JSON.stringify(data) });
  form.reset();
}));
document.querySelector('#refresh').addEventListener('click', load);
projectFilter.addEventListener('change', load);
load();
