(() => {
  "use strict";

  const explanations = {
    impact: "Expected benefit if this work is completed. Higher impact raises priority.",
    urgency: "How time-sensitive the work is. Higher urgency raises priority.",
    effort: "Estimated work required. Higher effort lowers the score.",
    confidence: "Confidence in the estimate and expected outcome. Higher confidence raises priority.",
    risk: "Risk addressed or reduced by this work. Higher risk raises priority."
  };
  const factorNames = {impact: "Impact", urgency: "Urgency", effort: "Effort", confidence: "Confidence", risk: "Risk"};
  const statusNames = {planned: "Planned", ready: "Ready", in_progress: "In progress", blocked: "Blocked"};
  const boundControls = ["search-input", "status-filter", "risk-filter", "sort-control", "export-button", "priority-item", "debug-toggle"];
  const state = {items: [], requestStatus: "pending", requestCount: 0, query: "", status: "all", risk: "all", sortKey: "priority", direction: "desc", selectedId: "", errors: [], debug: false, exportTimer: 0};
  let tooltipSequence = 0;
  const $ = (selector) => document.querySelector(selector);
  const list = $("#priority-list");
  const detail = $("#item-detail");
  const search = $("#search-input");
  const status = $("#status-filter");
  const risk = $("#risk-filter");
  const sort = $("#sort-control");
  const debugPanel = $("#debug-panel");
  const debugToggle = $("#debug-toggle");
  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[char]));
  const score = (item) => Number.isFinite(item.priority) ? item.priority : Math.round((2 * item.impact + 1.5 * item.urgency + item.confidence + .5 * item.risk) / Math.max(item.effort, 1) * 10000) / 10000;
  const fmt = (value) => Number(value).toFixed(4).replace(/0+$/, "").replace(/\.$/, "");

  function recordError(message) {
    state.errors.push(String(message));
    state.errors = state.errors.slice(-5);
    renderDebug();
  }

  function visibleItems() {
    const needle = state.query.trim().toLocaleLowerCase();
    const filtered = state.items.filter((item) =>
      (!needle || `${item.id} ${item.title} ${item.description}`.toLocaleLowerCase().includes(needle)) &&
      (state.status === "all" || item.status === state.status) &&
      (state.risk === "all" || String(item.risk) === state.risk)
    );
    const direction = state.direction === "desc" ? -1 : 1;
    const key = state.sortKey;
    return filtered.slice().sort((a, b) => {
      const av = key === "priority" ? score(a) : a[key];
      const bv = key === "priority" ? score(b) : b[key];
      if (typeof av === "string") return av.localeCompare(bv) * direction;
      if (av !== bv) return (av < bv ? -1 : 1) * direction;
      if (key === "priority") return (b.urgency - a.urgency) || (b.impact - a.impact) || a.id.localeCompare(b.id);
      return a.id.localeCompare(b.id);
    });
  }

  function helpMarkup(factor) {
    const tipId = `tip-${factor}-${++tooltipSequence}`;
    return `<span class="help-wrap"><button class="factor-help" type="button" data-testid="factor-help" data-factor="${factor}" aria-label="What ${factorNames[factor].toLowerCase()} means" aria-describedby="${tipId}">i</button><span class="factor-tooltip" id="${tipId}" role="tooltip" data-testid="factor-tooltip">${explanations[factor]}</span></span>`;
  }

  function factorMarkup(factor, value) {
    return `<span class="factor-chip"><span>${factorNames[factor]}</span>${helpMarkup(factor)}<b>${esc(value)}</b></span>`;
  }

  function renderSummary() {
    const all = state.items;
    $("#summary-total").textContent = all.length;
    $("#summary-ready").textContent = all.filter((item) => item.status === "ready").length;
    $("#summary-progress").textContent = all.filter((item) => item.status === "in_progress").length;
    $("#summary-blocked").textContent = all.filter((item) => item.status === "blocked").length;
    const top = all.slice().sort((a, b) => score(b) - score(a) || b.urgency - a.urgency || b.impact - a.impact || a.id.localeCompare(b.id))[0];
    $("#summary-top").textContent = top ? fmt(score(top)) : "—";
  }

  function renderDetail(item, items) {
    if (!item) {
      detail.innerHTML = `<div class="detail-placeholder"><span class="detail-icon">↗</span><h2>Explore an item</h2><p>Select a ranked item to see its description and scoring breakdown.</p></div>`;
      return;
    }
    const rank = items.findIndex((row) => row.id === item.id) + 1;
    detail.innerHTML = `<div class="detail-topline"><span class="detail-rank">Rank ${rank || "—"}</span><span class="status-badge status-${esc(item.status)}" data-testid="status-badge">${esc(statusNames[item.status] || item.status)}</span></div>
      <h2 class="detail-title">${esc(item.title)}</h2><p class="detail-id">${esc(item.id)} · Priority score <strong>${fmt(score(item))}</strong></p>
      <p class="detail-description">${esc(item.description)}</p><h3>Scoring factors</h3><div class="breakdown">${["impact", "urgency", "effort", "confidence", "risk"].map((factor) => `<div class="breakdown-row"><span class="breakdown-label">${factorNames[factor]} ${helpMarkup(factor)}</span><strong class="breakdown-value">${esc(item[factor])} / 5</strong></div>`).join("")}</div>
      <p class="formula-note">Priority = (2 × impact + 1.5 × urgency + confidence + 0.5 × risk) ÷ effort</p>`;
  }

  function render() {
    const items = visibleItems();
    list.setAttribute("aria-busy", "false");
    $("#result-count").textContent = `${items.length} ${items.length === 1 ? "item" : "items"}`;
    if (state.requestStatus !== "success") {
      const message = state.requestStatus === "pending" ? ["Loading backlog", "Reading the latest backlog data…"] : ["Backlog unavailable", state.requestError || "The backlog data could not be loaded. Check the data file and try again."];
      list.innerHTML = `<div class="empty-state ${state.requestStatus === "error" ? "error-state" : ""}" role="status"><strong>${esc(message[0])}</strong>${esc(message[1])}${state.requestStatus === "error" ? '<br><button class="button button-quiet" type="button" data-action="retry">Try again</button>' : ""}</div>`;
      renderDetail(null, items);
      renderDebug();
      return;
    }
    if (!items.length) {
      const noBacklog = state.items.length === 0;
      list.innerHTML = `<div class="empty-state" role="status"><strong>${noBacklog ? "Your backlog is clear" : "No matching items"}</strong>${noBacklog ? "There are no items in the backlog yet." : "Try changing the search or filters."}</div>`;
      state.selectedId = "";
      renderDetail(null, items);
      renderDebug();
      return;
    }
    if (!items.some((item) => item.id === state.selectedId)) state.selectedId = items[0].id;
    list.innerHTML = items.map((item, index) => `<article class="priority-card" role="group" tabindex="0" data-testid="priority-item" data-item-id="${esc(item.id)}" data-priority-tier="${index < 3 ? "top" : "standard"}" aria-current="${item.id === state.selectedId ? "true" : "false"}" aria-label="${esc(item.title)}, rank ${index + 1}, priority ${fmt(score(item))}">
      <span class="rank-mark">${index + 1}</span><div class="card-main"><div class="card-heading"><h3 class="card-title">${esc(item.title)}</h3><span class="status-badge status-${esc(item.status)}" data-testid="status-badge">${esc(statusNames[item.status] || item.status)}</span></div><p class="card-id">${esc(item.id)}</p><div class="factor-row">${["impact", "urgency", "effort", "confidence", "risk"].map((factor) => factorMarkup(factor, item[factor])).join("")}</div></div>
      <span class="score-block"><span class="score-label">SCORE</span><strong class="score-value" data-testid="priority-score">${fmt(score(item))}</strong></span></article>`).join("");
    renderDetail(items.find((item) => item.id === state.selectedId), items);
    renderDebug();
  }

  function renderDebug() {
    debugPanel.innerHTML = `<h2>Runtime diagnostics</h2>
      <p data-testid="debug-bound-controls">Bound controls: ${boundControls.join(", ")}</p>
      <p data-testid="debug-data-request" data-source="/api/items" data-status="${esc(state.requestStatus)}" data-request-count="${state.requestCount}" data-item-count="${state.items.length}">Data request: source /api/items · status ${esc(state.requestStatus)} · requests ${state.requestCount} · items ${state.items.length}</p>
      <p data-testid="debug-state" data-search="${esc(state.query)}" data-status-filter="${esc(state.status)}" data-risk-filter="${esc(state.risk)}" data-sort="${esc(state.sortKey)}-${esc(state.direction)}" data-selected-id="${esc(state.selectedId)}">State: search “${esc(state.query)}” · status ${esc(state.status)} · risk ${esc(state.risk)} · sort ${esc(state.sortKey)} ${esc(state.direction)} · selected ${esc(state.selectedId || "none")}</p>
      <p data-testid="debug-errors" data-count="${state.errors.length}">Errors: ${state.errors.length ? state.errors.map(esc).join("; ") : "none"}</p>`;
  }

  async function loadItems() {
    state.requestCount += 1;
    state.requestStatus = "pending";
    $("#export-button").disabled = true;
    delete state.requestError;
    render();
    renderDebug();
    try {
      const response = await fetch("/api/items", {headers: {Accept: "application/json"}});
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.error || `Request failed (${response.status})`);
      }
      const body = await response.json();
      if (!body || !Array.isArray(body.items)) throw new Error("Backlog response must contain an items array");
      state.items = body.items;
      state.requestStatus = "success";
      $("#export-button").disabled = false;
      renderSummary();
    } catch (error) {
      state.requestStatus = "error";
      $("#export-button").disabled = true;
      state.requestError = error instanceof Error ? error.message : String(error);
      recordError(state.requestError);
    }
    render();
    renderDebug();
  }

  function setSort(value) {
    const [key, direction] = value.split("-");
    state.sortKey = key;
    state.direction = direction;
  }

  search.addEventListener("input", () => { state.query = search.value; render(); });
  status.addEventListener("change", () => { state.status = status.value; render(); });
  risk.addEventListener("change", () => { state.risk = risk.value; render(); });
  sort.addEventListener("change", () => { setSort(sort.value); render(); });
  list.addEventListener("click", (event) => {
    if (event.target.closest("[data-action=retry]")) { loadItems(); return; }
    const card = event.target.closest("[data-testid=priority-item]");
    if (!card || event.target.closest("[data-testid=factor-help]")) return;
    state.selectedId = card.dataset.itemId;
    render();
  });
  list.addEventListener("keydown", (event) => {
    const card = event.target.closest("[data-testid=priority-item]");
    if (!card || event.target.closest("[data-testid=factor-help]")) return;
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); state.selectedId = card.dataset.itemId; render(); $("[data-testid=priority-item][aria-current=true]")?.focus(); }
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const cards = [...list.querySelectorAll("[data-testid=priority-item]")];
      const next = cards[Math.max(0, Math.min(cards.length - 1, cards.indexOf(card) + (event.key === "ArrowDown" ? 1 : -1)))];
      next?.focus();
    }
  });
  debugToggle.addEventListener("click", () => {
    state.debug = !state.debug;
    debugPanel.hidden = !state.debug;
    debugToggle.setAttribute("aria-expanded", String(state.debug));
    debugToggle.textContent = state.debug ? "Hide debug" : "Show debug";
    renderDebug();
  });
  $("#export-button").addEventListener("click", () => {
    const ordering = visibleItems().map((item) => ({...item, priority: score(item)}));
    const blob = new Blob([`${JSON.stringify(ordering, null, 2)}\n`], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "priority-ordering.json";
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    const statusMessage = $("#export-status");
    statusMessage.textContent = `JSON exported · ${ordering.length} ${ordering.length === 1 ? "item" : "items"} in the current ordering.`;
    statusMessage.hidden = false;
    clearTimeout(state.exportTimer);
    state.exportTimer = setTimeout(() => { statusMessage.hidden = true; }, 12000);
  });

  renderDebug();
  loadItems();
})();
