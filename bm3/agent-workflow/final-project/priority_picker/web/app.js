(() => {
  "use strict";

  const state = { items: [], visible: [], selected: null };
  const $ = (id) => document.getElementById(id);
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
  const score = (item) => Number(((2 * item.impact + 1.5 * item.urgency + item.confidence + 0.5 * item.risk) / Math.max(item.effort, 1)).toFixed(4));
  const factorLabels = { impact: "Impact", urgency: "Urgency", effort: "Effort", confidence: "Confidence", risk: "Risk" };
  const validItem = (item) => item && typeof item.id === "string" && item.id.trim() && typeof item.title === "string" && item.title.trim() && typeof item.description === "string" && ["impact", "urgency", "effort", "confidence", "risk"].every((key) => Number.isFinite(item[key]) && item[key] >= 1 && item[key] <= 5) && ["planned", "ready", "in_progress", "blocked"].includes(item.status);

  function showMessage(title, text, kind = "empty") {
    $("priority-list").innerHTML = `<div class="state state-${kind}"><div class="state-icon">${kind === "error" ? "!" : "∅"}</div><h3>${escapeHtml(title)}</h3><p>${escapeHtml(text)}</p></div>`;
    $("visible-count").textContent = kind === "error" ? "Unavailable" : "0 items";
    $("item-detail").innerHTML = `<div class="detail-empty"><span class="detail-kicker">DETAIL VIEW</span><h2>No item selected</h2><p>${kind === "error" ? "Fix the data problem and reload the page." : "Select a backlog item to inspect its trade-offs."}</p></div>`;
  }

  function renderDetail() {
    const item = state.selected;
    if (!item) {
      $("item-detail").innerHTML = '<div class="detail-empty"><span class="detail-kicker">DETAIL VIEW</span><h2>No item selected</h2><p>Select a backlog item to inspect its trade-offs.</p></div>';
      return;
    }
    const factors = ["impact", "urgency", "effort", "confidence", "risk"].map((key) => `<div class="detail-factor"><span>${factorLabels[key]}</span><strong>${item[key]}<small> / 5</small></strong></div>`).join("");
    $("item-detail").innerHTML = `<div class="detail-top"><span class="detail-kicker">ITEM DETAIL</span><button type="button" class="icon-button" id="close-detail" aria-label="Close item details">×</button></div><span class="item-id">${escapeHtml(item.id)}</span><h2>${escapeHtml(item.title)}</h2><span class="status status-${escapeHtml(item.status)}">${escapeHtml(item.status.replace("_", " "))}</span><p class="description">${escapeHtml(item.description)}</p><div class="detail-score"><span>Priority score</span><strong>${score(item).toFixed(4)}</strong></div><div class="factor-grid">${factors}</div>`;
    $("close-detail").addEventListener("click", () => { state.selected = null; renderDetail(); renderList(); });
  }

  function renderList() {
    const list = $("priority-list");
    $("visible-count").textContent = `${state.visible.length} ${state.visible.length === 1 ? "item" : "items"}`;
    if (!state.visible.length) {
      showMessage("Nothing matches these filters", "Try a broader search or reset one of the filters.");
      return;
    }
    list.innerHTML = state.visible.map((item, index) => {
      const selected = state.selected && state.selected.id === item.id;
      const factors = ["impact", "urgency", "effort", "confidence", "risk"].map((key) => `<span class="factor"><b>${item[key]}</b><small>${factorLabels[key].slice(0, 3)}</small></span>`).join("");
      return `<article data-testid="priority-item" class="priority-item${selected ? " is-selected" : ""}"><button type="button" class="item-button" data-item-id="${escapeHtml(item.id)}" aria-expanded="${selected}"><span class="rank" aria-label="Rank ${index + 1}">${String(index + 1).padStart(2, "0")}</span><span class="item-copy"><strong>${escapeHtml(item.title)}</strong><span class="item-meta"><span class="status status-${escapeHtml(item.status)}">${escapeHtml(item.status.replace("_", " "))}</span><span>${escapeHtml(item.id)}</span></span></span><span class="item-factors">${factors}</span><span class="score"><b>${score(item).toFixed(2)}</b><small>score</small></span><span class="chevron" aria-hidden="true">→</span></button></article>`;
    }).join("");
    list.querySelectorAll("[data-item-id]").forEach((button) => button.addEventListener("click", () => {
      state.selected = state.items.find((item) => item.id === button.dataset.itemId) || null;
      renderList();
      renderDetail();
    }));
  }

  function update() {
    const query = $("search-input").value.trim().toLowerCase();
    const status = $("status-filter").value;
    const risk = $("risk-filter").value;
    const [sortKey, direction] = $("sort-control").value.split("-");
    state.visible = state.items.filter((item) => (!query || `${item.id} ${item.title} ${item.description}`.toLowerCase().includes(query)) && (status === "all" || item.status === status) && (risk === "all" || String(item.risk) === risk));
    state.visible.sort((a, b) => {
      const left = sortKey === "priority" ? score(a) : sortKey === "title" ? a.title.toLowerCase() : a[sortKey];
      const right = sortKey === "priority" ? score(b) : sortKey === "title" ? b.title.toLowerCase() : b[sortKey];
      if (left !== right) return direction === "asc" ? (left < right ? -1 : 1) : (left > right ? -1 : 1);
      if (sortKey === "priority" && direction === "desc") {
        if (a.urgency !== b.urgency) return b.urgency - a.urgency;
        if (a.impact !== b.impact) return b.impact - a.impact;
      }
      return a.id.localeCompare(b.id);
    });
    renderList();
    renderDetail();
  }

  function renderSummary() {
    $("total-count").textContent = state.items.length;
    $("ready-count").textContent = state.items.filter((item) => item.status === "ready").length;
    $("blocked-count").textContent = state.items.filter((item) => item.status === "blocked").length;
    $("average-score").textContent = state.items.length ? (state.items.reduce((sum, item) => sum + score(item), 0) / state.items.length).toFixed(2) : "0.00";
  }

  function exportOrdering() {
    const blob = new Blob([JSON.stringify(state.visible, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "priority-ordering.json";
    link.click();
    URL.revokeObjectURL(link.href);
  }

  async function load() {
    try {
      const response = await fetch("/api/items", { headers: { Accept: "application/json" } });
      const payload = await response.json();
      if (!response.ok || !payload || !Array.isArray(payload.items) || !payload.items.every(validItem)) throw new Error(payload && payload.error ? payload.error : "The backlog response was invalid.");
      state.items = payload.items;
      renderSummary();
      update();
    } catch (error) {
      $("total-count").textContent = "—";
      $("ready-count").textContent = "—";
      $("blocked-count").textContent = "—";
      $("average-score").textContent = "—";
      showMessage("Backlog unavailable", error.message || "Could not load the backlog.", "error");
    }
  }

  ["search-input", "status-filter", "risk-filter", "sort-control"].forEach((id) => $(id).addEventListener("input", update));
  $("export-button").addEventListener("click", exportOrdering);
  load();
})();
