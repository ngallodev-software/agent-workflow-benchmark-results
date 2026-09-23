(() => {
  const factorNames = { impact: "Impact", urgency: "Urgency", effort: "Effort", confidence: "Confidence", risk: "Risk" };
  const list = document.querySelector("#priority-list");
  const message = document.querySelector("#message");
  const empty = document.querySelector("#empty-state");
  const search = document.querySelector("#search-input");
  const status = document.querySelector("#status-filter");
  const risk = document.querySelector("#risk-filter");
  const sort = document.querySelector("#sort-control");
  const exportButton = document.querySelector("#export-button");
  let allItems = [];
  let visibleItems = [];

  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
  const score = (item) => Number(item.priority ?? ((2 * item.impact + 1.5 * item.urgency + item.confidence + 0.5 * item.risk) / Math.max(item.effort, 1))).toFixed(4);
  const statusLabel = (value) => ({ planned: "Planned", ready: "Ready", in_progress: "In progress", blocked: "Blocked" })[value] || value;

  function updateSummary(items) {
    document.querySelector("#total-count").textContent = allItems.length;
    document.querySelector("#ready-count").textContent = allItems.filter((item) => item.status === "ready").length;
    document.querySelector("#blocked-count").textContent = allItems.filter((item) => item.status === "blocked").length;
    document.querySelector("#visible-count").textContent = items.length;
  }

  function applyControls() {
    const needle = search.value.trim().toLocaleLowerCase();
    const state = status.value;
    const riskValue = risk.value;
    const [key, direction] = sort.value.split("-");
    visibleItems = allItems.filter((item) =>
      (!needle || `${item.title} ${item.description}`.toLocaleLowerCase().includes(needle)) &&
      (state === "all" || item.status === state) &&
      (riskValue === "all" || String(item.risk) === riskValue)
    );
    const fields = { priority: (item) => Number(score(item)), urgency: (item) => Number(item.urgency), impact: (item) => Number(item.impact), effort: (item) => Number(item.effort), title: (item) => item.title.toLocaleLowerCase() };
    visibleItems.sort((a, b) => {
      const first = fields[key](a), second = fields[key](b);
      let delta = first < second ? -1 : first > second ? 1 : 0;
      if (direction === "desc") delta *= -1;
      if (delta) return delta;
      if (key === "priority" && direction === "desc") {
        delta = Number(b.urgency) - Number(a.urgency) || Number(b.impact) - Number(a.impact);
      }
      return delta || a.id.localeCompare(b.id);
    });
    render();
  }

  function render() {
    updateSummary(visibleItems);
    exportButton.disabled = false;
    empty.hidden = visibleItems.length !== 0;
    list.innerHTML = visibleItems.map((item, index) => {
      const detailId = `detail-${index}`;
      const factors = Object.entries(factorNames).map(([key, label]) => `<span class="factor"><span>${label}</span><b>${esc(item[key])}</b></span>`).join("");
      const detailFactors = Object.entries(factorNames).map(([key, label]) => `<div><dt>${label}</dt><dd>${esc(item[key])}<span> / 5</span></dd></div>`).join("");
      return `<article class="priority-item" data-testid="priority-item">
        <button class="item-toggle" type="button" aria-expanded="false" aria-controls="${detailId}">
          <span class="rank">${String(index + 1).padStart(2, "0")}</span>
          <span class="item-main"><span class="item-title">${esc(item.title)}</span><span class="item-id">${esc(item.id)}</span></span>
          <span class="score-block"><b>${score(item)}</b><span>PRIORITY</span></span>
          <span class="status-badge status-${esc(item.status)}"><i></i>${esc(statusLabel(item.status))}</span>
          <span class="factor-strip">${factors}</span><span class="chevron" aria-hidden="true">⌄</span>
        </button>
        <section class="item-detail" data-testid="item-detail" id="${detailId}" hidden>
          <p class="description">${esc(item.description) || "No description provided."}</p>
          <div class="breakdown"><div class="breakdown-head"><h3>Scoring factors</h3><span>Higher impact, urgency, confidence and risk raise priority; effort reduces it.</span></div><dl>${detailFactors}</dl></div>
        </section>
      </article>`;
    }).join("");
  }

  list.addEventListener("click", (event) => {
    const button = event.target.closest(".item-toggle");
    if (!button) return;
    const detail = document.getElementById(button.getAttribute("aria-controls"));
    const opening = button.getAttribute("aria-expanded") !== "true";
    button.setAttribute("aria-expanded", String(opening));
    detail.hidden = !opening;
  });
  [search, status, risk, sort].forEach((control) => control.addEventListener("input", applyControls));
  [status, risk, sort].forEach((control) => control.addEventListener("change", applyControls));
  exportButton.addEventListener("click", () => {
    const blob = new Blob([`${JSON.stringify(visibleItems, null, 2)}\n`], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "priority-ordering.json";
    anchor.click();
    URL.revokeObjectURL(url);
  });

  fetch("/api/items").then(async (response) => {
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "The backlog could not be loaded.");
    allItems = Array.isArray(body.items) ? body.items : [];
    message.hidden = true;
    applyControls();
  }).catch((error) => {
    allItems = [];
    updateSummary([]);
    list.innerHTML = "";
    empty.hidden = true;
    exportButton.disabled = true;
    message.textContent = `Unable to load backlog: ${error.message}`;
    message.hidden = false;
  });
})();
