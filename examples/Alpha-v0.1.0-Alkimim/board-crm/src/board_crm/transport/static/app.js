const STAGES = ["NEW", "QUALIFIED", "PROPOSAL", "WON", "LOST"];
const ACTIVE = STAGES.slice(0, 3);
const strings = {
  "pt-BR": {
    eyebrow:"Exemplo executável", headline:"Seu funil, em um quadro.", intro:"Crie oportunidades, mova cartões entre etapas e registre o resultado de cada negociação.", cases:"casos de uso especificados", createTitle:"Nova oportunidade", title:"Título", company:"Empresa", owner:"Responsável", create:"Criar cartão", filter:"Filtrar por responsável", refresh:"Atualizar", help:"Arraste um cartão para uma etapa vizinha ou use o seletor no próprio cartão. Etapas encerradas não recebem cartões.", footer:"Demonstração local. Dados salvos no SQLite configurado ao iniciar o servidor.", NEW:"Novas", QUALIFIED:"Qualificadas", PROPOSAL:"Proposta", WON:"Ganhas", LOST:"Perdidas", empty:"Nenhum cartão", move:"Mover", note:"Nota", notes:"Notas e histórico", add:"Adicionar", won:"Ganha", lost:"Perdida", reason:"Motivo do encerramento", version:"Versão", updated:"Atualização", success:"Quadro atualizado.", created:"Oportunidade criada.", changed:"Alteração registrada.", badReason:"Informe um motivo.", retry:"O cartão mudou. Atualize o quadro antes de tentar novamente."},
  en: {
    eyebrow:"Runnable example", headline:"Your pipeline, on one board.", intro:"Create opportunities, move cards between stages, and record the result of each deal.", cases:"specified use cases", createTitle:"New opportunity", title:"Title", company:"Company", owner:"Owner", create:"Create card", filter:"Filter by owner", refresh:"Refresh", help:"Drag a card to an adjacent stage or use the selector on the card. Closed stages do not accept cards.", footer:"Local demonstration. Data is saved in the SQLite file configured when starting the server.", NEW:"New", QUALIFIED:"Qualified", PROPOSAL:"Proposal", WON:"Won", LOST:"Lost", empty:"No cards", move:"Move", note:"Note", notes:"Notes and history", add:"Add", won:"Won", lost:"Lost", reason:"Reason for closing", version:"Version", updated:"Updated", success:"Board refreshed.", created:"Opportunity created.", changed:"Change recorded.", badReason:"Enter a reason.", retry:"The card changed. Refresh the board before trying again."}
};
let language = "pt-BR";
const t = key => strings[language][key] || key;
const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function notice(message, success = false) {
  statusElement.textContent = message;
  statusElement.classList.toggle("success", success);
}
async function request(path, method = "GET", body) {
  const options = { method, headers: {} };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error === "conflict" ? t("retry") : (data.message || data.error));
  return data;
}
async function mutate(path, body) {
  try { await request(path, "POST", body); await loadBoard(); notice(t("changed"), true); }
  catch (error) { notice(error.message); }
}
function cardNode(card) {
  const node = el("article", "card");
  node.draggable = ACTIVE.includes(card.stage);
  if (node.draggable) node.addEventListener("dragstart", event => {
    event.dataTransfer.setData("application/json", JSON.stringify({ id: card.id, version: card.version }));
    event.dataTransfer.effectAllowed = "move";
  });
  node.append(el("h3", "", card.title), el("p", "company", card.company));
  const meta = el("div", "card-meta");
  meta.append(el("span", "", card.owner), el("span", "", `${t("version")} ${card.version}`));
  node.append(meta);
  const actions = el("div", "card-actions");
  if (ACTIVE.includes(card.stage)) {
    const nearby = ACTIVE.filter(stage => Math.abs(ACTIVE.indexOf(stage) - ACTIVE.indexOf(card.stage)) === 1);
    const row = el("div", "move-row");
    const selector = el("select");
    selector.setAttribute("aria-label", t("move"));
    for (const stage of nearby) {
      const option = el("option", "", t(stage)); option.value = stage; selector.append(option);
    }
    const button = el("button", "", t("move")); button.type = "button";
    button.addEventListener("click", () => mutate(`/api/opportunities/${encodeURIComponent(card.id)}/move`, {stage: selector.value, expected_version: card.version}));
    row.append(selector, button); actions.append(row);
    const close = el("div", "close-row");
    for (const outcome of (card.stage === "PROPOSAL" ? ["won", "lost"] : ["lost"])) {
      const closeButton = el("button", "", t(outcome)); closeButton.type = "button";
      closeButton.addEventListener("click", () => {
        const reason = window.prompt(t("reason"));
        if (reason === null) return;
        if (!reason.trim()) { notice(t("badReason")); return; }
        mutate(`/api/opportunities/${encodeURIComponent(card.id)}/close-${outcome}`,
               {reason, expected_version: card.version});
      });
      close.append(closeButton);
    }
    actions.append(close);
  }
  node.append(actions);
  const details = el("details");
  details.append(el("summary", "", `${t("notes")} (${card.notes.length} / ${card.history.length})`));
  const noteList = el("ul");
  for (const note of card.notes) noteList.append(el("li", "", note.body));
  details.append(noteList);
  const history = el("p", "", card.history.map(event => `${event.source_stage || "START"} → ${event.destination_stage}`).join(" · "));
  details.append(history);
  const noteForm = el("form", "note-form");
  const input = el("input"); input.maxLength = 500; input.required = true; input.placeholder = t("note");
  input.setAttribute("aria-label", t("note"));
  const add = el("button", "", t("add")); add.type = "submit";
  noteForm.append(input, add);
  noteForm.addEventListener("submit", event => { event.preventDefault(); mutate(`/api/opportunities/${encodeURIComponent(card.id)}/notes`, {body: input.value, expected_version: card.version}); });
  details.append(noteForm); node.append(details);
  return node;
}
function renderBoard(columns) {
  boardElement.replaceChildren();
  for (const stage of STAGES) {
    const column = el("section", "column"); column.dataset.stage = stage;
    const heading = el("div", "column-head"); heading.append(el("h2", "", t(stage)), el("span", "count", String(columns[stage].length))); column.append(heading);
    const cards = el("div", "cards");
    if (columns[stage].length === 0) cards.append(el("p", "empty", t("empty")));
    for (const card of columns[stage]) cards.append(cardNode(card));
    column.append(cards);
    if (ACTIVE.includes(stage)) {
      column.addEventListener("dragover", event => { event.preventDefault(); column.classList.add("active-drop"); });
      column.addEventListener("dragleave", () => column.classList.remove("active-drop"));
      column.addEventListener("drop", event => {
        event.preventDefault(); column.classList.remove("active-drop");
        try {
          const card = JSON.parse(event.dataTransfer.getData("application/json"));
          if (card.id) mutate(`/api/opportunities/${encodeURIComponent(card.id)}/move`, {stage, expected_version: card.version});
        } catch { notice("Invalid drag data"); }
      });
    }
    boardElement.append(column);
  }
}
async function loadBoard() {
  const owner = document.getElementById("owner-filter").value;
  const query = owner ? `?owner=${encodeURIComponent(owner)}` : "";
  const data = await request(`/api/board${query}`);
  renderBoard(data.columns);
}
document.getElementById("create-form").addEventListener("submit", async event => {
  event.preventDefault();
  const values = Object.fromEntries(["title", "company", "owner"].map(id => [id, document.getElementById(id).value]));
  try { await request("/api/opportunities", "POST", values); event.target.reset(); await loadBoard(); notice(t("created"), true); }
  catch (error) { notice(error.message); }
});
document.getElementById("refresh").addEventListener("click", () => loadBoard().then(() => notice(t("success"), true)).catch(error => notice(error.message)));
document.getElementById("owner-filter").addEventListener("change", () => loadBoard().catch(error => notice(error.message)));
document.getElementById("language").addEventListener("click", () => {
  language = language === "pt-BR" ? "en" : "pt-BR";
  document.documentElement.lang = language;
  document.getElementById("language").textContent = language === "pt-BR" ? "English" : "Português";
  document.querySelectorAll("[data-i18n]").forEach(node => { node.textContent = t(node.dataset.i18n); });
  loadBoard().catch(error => notice(error.message));
});
loadBoard().catch(error => notice(error.message));
