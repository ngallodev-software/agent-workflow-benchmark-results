(() => {
  "use strict";
  const explanations = {
    impact: "How much value or improvement this work can deliver.",
    urgency: "How time-sensitive the work is and how soon it matters.",
    effort: "The relative work required; higher effort lowers the score.",
    confidence: "How confident we are in the expected outcome.",
    risk: "The delivery or outcome risk associated with this work."
  };
  const factorNames = Object.keys(explanations);
  const state = { items: [], visible: [], selectedId: "", requestStatus: "pending", requestCount: 0, errors: [], debug: false };
  const el = (id) => document.getElementById(id);
  const controls = {
    search: el("search-input"), status: el("status-filter"), risk: el("risk-filter"), sort: el("sort-control"),
    export: document.querySelector('[data-testid="export-button"]'), debug: document.querySelector('[data-testid="debug-toggle"]'),
    list: el("priority-list"), detail: el("item-detail"), debugPanel: el("debug-panel")
  };
  const score = (item) => Math.round(((2 * item.impact + 1.5 * item.urgency + item.confidence + 0.5 * item.risk) / Math.max(item.effort, 1) + Number.EPSILON) * 10000) / 10000;
  const byDefault = (a, b) => score(b) - score(a) || b.urgency - a.urgency || b.impact - a.impact || a.id.localeCompare(b.id);
  const safeText = (value) => String(value);

  function validItems(items) {
    if (!Array.isArray(items)) throw new Error("The backlog response must be a JSON array of items.");
    const seen = new Set();
    for (const [index, item] of items.entries()) {
      if (!item || typeof item !== "object" || Array.isArray(item)) throw new Error(`Item ${index + 1} must be an object.`);
      for (const field of ["id", "title", "impact", "urgency", "effort", "confidence", "risk", "status", "description"]) {
        if (!(field in item)) throw new Error(`Item ${index + 1} is missing required field “${field}”.`);
      }
      if (typeof item.id !== "string" || !item.id.trim() || seen.has(item.id)) throw new Error(`Item ${index + 1} has an empty or duplicate ID.`);
      seen.add(item.id);
      if (typeof item.title !== "string" || !item.title.trim()) throw new Error(`Item ${index + 1} needs a title.`);
      for (const field of ["impact", "urgency", "effort", "confidence", "risk"]) {
        if (typeof item[field] !== "number" || !Number.isFinite(item[field]) || item[field] < 1 || item[field] > 5) throw new Error(`Item ${index + 1} has an invalid ${field} value (expected 1–5).`);
      }
      if (!["planned", "ready", "in_progress", "blocked"].includes(item.status)) throw new Error(`Item ${index + 1} has an unknown status.`);
      if (typeof item.description !== "string") throw new Error(`Item ${index + 1} has an invalid description.`);
    }
    return items.map((item) => ({ ...item }));
  }

  function sortedItems(items) {
    const [key, direction] = controls.sort.value.split("-");
    const sign = direction === "asc" ? 1 : -1;
    return [...items].sort((a, b) => {
      if (key === "priority") return sign * (score(a) - score(b)) || b.urgency - a.urgency || b.impact - a.impact || a.id.localeCompare(b.id);
      let compared;
      if (key === "title") compared = a.title.localeCompare(b.title) || a.id.localeCompare(b.id);
      else compared = a[key] - b[key] || a.id.localeCompare(b.id);
      return sign * compared;
    });
  }

  function filterAndSort() {
    const query = controls.search.value.trim().toLocaleLowerCase();
    const status = controls.status.value;
    const risk = controls.risk.value;
    state.visible = sortedItems(state.items.filter((item) => {
      const matches = !query || `${item.id} ${item.title} ${item.description}`.toLocaleLowerCase().includes(query);
      return matches && (status === "all" || item.status === status) && (risk === "all" || item.risk === Number(risk));
    }));
    render();
    updateDebug();
  }

  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function badge(status) {
    const labels = { planned: "Planned", ready: "Ready", in_progress: "In progress", blocked: "Blocked" };
    const result = node("span", `status-badge status-${status}`, labels[status]);
    result.dataset.testid = "status-badge";
    return result;
  }

  function addFactors(target, item, detailed = false) {
    if (detailed) {
      const grid = node("div", "detail-factors");
      for (const name of factorNames) {
        const part = node("div", "detail-factor");
        part.append(node("span", "", name[0].toUpperCase() + name.slice(1)), node("strong", "", safeText(item[name])));
        grid.append(part);
      }
      target.append(grid);
      return;
    }
    const line = node("div", "factor-line");
    for (const [index, name] of factorNames.entries()) {
      if (index) line.append(document.createTextNode(" · "));
      const part = node("span", "factor");
      part.append(node("span", "", `${name[0].toUpperCase()}:`), node("b", "", safeText(item[name])));
      const help = node("button", "factor-help", "?");
      help.type = "button";
      help.dataset.testid = "factor-help";
      help.dataset.factor = name;
      help.setAttribute("aria-label", `${name[0].toUpperCase() + name.slice(1)}: ${explanations[name]}`);
      const tooltip = node("span", "factor-tooltip", explanations[name]);
      tooltip.setAttribute("role", "tooltip");
      tooltip.dataset.testid = "factor-tooltip";
      part.append(help, tooltip);
      line.append(part);
    }
    target.append(line);
  }

  function renderDetail(item) {
    controls.detail.replaceChildren();
    if (!item) {
      const placeholder = node("div", "detail-placeholder");
      placeholder.append(node("span", "placeholder-icon", "↖"), node("p", "", state.visible.length ? "Select an item to see its details and scoring breakdown." : "Choose an item after adjusting your filters."));
      controls.detail.append(placeholder);
      return;
    }
    const top = node("div", "detail-topline");
    top.append(badge(item.status), node("span", "detail-score", score(item).toFixed(4)));
    controls.detail.append(node("p", "detail-label", `SELECTED ITEM · ${item.id}`), top, node("h3", "", item.title), node("p", "description", item.description));
    controls.detail.append(node("p", "detail-label", "COMPLETE FACTOR BREAKDOWN"));
    addFactors(controls.detail, item, true);
  }

  function render() {
    el("total-count").textContent = safeText(state.items.length);
    el("ready-count").textContent = safeText(state.items.filter((item) => item.status === "ready").length);
    el("top-score").textContent = state.items.length ? score([...state.items].sort(byDefault)[0]).toFixed(2) : "—";
    el("result-count").textContent = `${state.visible.length} of ${state.items.length} items`;
    controls.list.replaceChildren();
    if (!state.visible.length) {
      const message = node("div", "state-message", state.items.length ? "No items match these filters. Try a different search or clear a filter." : "Your backlog is empty. Add items to data/backlog.json to get started.");
      controls.list.append(message);
      renderDetail(null);
      return;
    }
    state.visible.forEach((item, index) => {
      const card = node("article", "priority-card");
      card.dataset.testid = "priority-item";
      card.dataset.rank = String(index + 1);
      if (index < 3) card.dataset.priorityTier = "top";
      if (item.id === state.selectedId) card.classList.add("detail-card-selected");
      card.append(node("span", "rank", String(index + 1)));
      const main = node("div", "card-main");
      const title = node("button", "item-select");
      title.type = "button";
      title.dataset.testid = "item-detail-trigger";
      title.setAttribute("aria-selected", item.id === state.selectedId ? "true" : "false");
      title.setAttribute("aria-controls", "item-detail");
      title.append(node("span", "", item.title), node("span", "item-id", item.id));
      title.addEventListener("click", () => {
        state.selectedId = item.id;
        render();
        updateDebug();
      });
      const meta = node("div", "card-meta");
      meta.append(badge(item.status));
      main.append(title, meta);
      addFactors(main, item);
      const scoreBlock = node("div", "score-block");
      scoreBlock.append(node("span", "score-label", "Priority"));
      const scoreElement = node("strong", "priority-score", score(item).toFixed(2));
      scoreElement.dataset.testid = "priority-score";
      scoreBlock.append(scoreElement);
      card.append(main, scoreBlock);
      controls.list.append(card);
    });
    renderDetail(state.items.find((item) => item.id === state.selectedId) || null);
  }

  function updateDebug() {
    const bound = ["search-input", "status-filter", "risk-filter", "sort-control", "export-button", "item-detail-trigger", "debug-toggle"];
    const boundNode = el("debug-bound-controls");
    boundNode.textContent = bound.join(", ");
    boundNode.dataset.controls = JSON.stringify(bound);
    const request = el("debug-data-request");
    request.dataset.source = "/api/items";
    request.dataset.status = state.requestStatus;
    request.dataset.requestCount = String(state.requestCount);
    request.dataset.itemCount = String(state.items.length);
    request.textContent = `source=/api/items; status=${state.requestStatus}; request count=${state.requestCount}; loaded items=${state.items.length}`;
    const [sortKey, sortDirection] = controls.sort.value.split("-");
    const debugState = el("debug-state");
    debugState.dataset.search = controls.search.value;
    debugState.dataset.statusFilter = controls.status.value;
    debugState.dataset.riskFilter = controls.risk.value;
    debugState.dataset.sort = `${sortKey}:${sortDirection}`;
    debugState.dataset.selectedId = state.selectedId;
    debugState.textContent = `search=${controls.search.value || "(empty)"}; status=${controls.status.value}; risk=${controls.risk.value}; sort=${sortKey}:${sortDirection}; selected item=${state.selectedId || "none"}`;
    const errors = el("debug-errors");
    errors.dataset.count = String(state.errors.length);
    errors.textContent = state.errors.length ? state.errors.slice(-5).join(" | ") : "none";
  }

  function showError(message) {
    state.errors.push(message);
    state.requestStatus = "error";
    controls.list.replaceChildren(Object.assign(node("div", "state-message error", `Unable to load the backlog: ${message}`), { role: "alert" }));
    el("total-count").textContent = "—";
    el("ready-count").textContent = "—";
    el("top-score").textContent = "—";
    renderDetail(null);
    updateDebug();
  }

  async function load() {
    state.requestCount += 1;
    state.requestStatus = "loading";
    updateDebug();
    try {
      const response = await fetch("/api/items", { headers: { Accept: "application/json" } });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.error || `Request failed (${response.status}).`);
      }
      const payload = await response.json();
      state.items = validItems(payload.items);
      state.requestStatus = "success";
      state.visible = [...state.items].sort(byDefault);
      if (state.visible.length) state.selectedId = state.visible[0].id;
      render();
      updateDebug();
    } catch (error) {
      showError(error instanceof Error ? error.message : "Unknown data error.");
    }
  }

  [controls.search, controls.status, controls.risk, controls.sort].forEach((control) => control.addEventListener(control === controls.search ? "input" : "change", filterAndSort));
  controls.debug.addEventListener("click", () => {
    state.debug = !state.debug;
    controls.debugPanel.hidden = !state.debug;
    controls.debug.setAttribute("aria-expanded", String(state.debug));
    controls.debug.textContent = state.debug ? "Hide debug" : "Show debug";
    updateDebug();
  });
  controls.export.addEventListener("click", () => {
    const blob = new Blob([`${JSON.stringify(state.visible, null, 2)}\n`], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "priority-ordering.json";
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    const status = el("export-status");
    status.textContent = `JSON exported · ${state.visible.length} ${state.visible.length === 1 ? "item" : "items"} in the current ordering.`;
    status.hidden = false;
    window.setTimeout(() => { status.hidden = true; }, 8000);
    updateDebug();
  });
  updateDebug();
  load();
})();
