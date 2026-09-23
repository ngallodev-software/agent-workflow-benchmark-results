(() => {
  const factors = ["impact", "urgency", "effort", "confidence", "risk"];
  const labels = { impact: "Impact", urgency: "Urgency", effort: "Effort", confidence: "Confidence", risk: "Risk" };
  const list = document.querySelector("#priority-list");
  const message = document.querySelector("#message");
  const count = document.querySelector("#result-count");
  const search = document.querySelector("#search-input");
  const status = document.querySelector("#status-filter");
  const risk = document.querySelector("#risk-filter");
  const sort = document.querySelector("#sort-control");
  const exportButton = document.querySelector('[data-testid="export-button"]');
  let items = [];
  let ordering = [];
  let openId = null;
  const compareId = (a, b) => {
    const left = Array.from(a, char => char.codePointAt(0));
    const right = Array.from(b, char => char.codePointAt(0));
    for (let i = 0; i < Math.min(left.length, right.length); i++) if (left[i] !== right[i]) return left[i] - right[i];
    return left.length - right.length;
  };
  const score = item => {
    const values = [item.impact, item.urgency, item.confidence, item.risk, item.effort].map(value => {
      const [whole, fraction = ""] = String(value).split(".");
      return { digits: BigInt(whole + fraction), scale: fraction.length };
    });
    const scale = Math.max(...values.map(value => value.scale));
    const [impact, urgency, confidence, risk, effort] = values.map(value => value.digits * 10n ** BigInt(scale - value.scale));
    const numerator = (4n * impact + 3n * urgency + 2n * confidence + risk) * 5000n;
    const denominator = effort * 10n ** BigInt(scale);
    let rounded = numerator / denominator;
    const remainder = numerator % denominator;
    if (2n * remainder > denominator || (2n * remainder === denominator && rounded % 2n)) rounded++;
    return Number(rounded) / 10000;
  };
  const valid = item => item && typeof item.id === "string" && item.id.trim() && typeof item.title === "string" && item.title.trim() &&
    factors.every(key => typeof item[key] === "number" && Number.isFinite(item[key]) && item[key] >= 1 && item[key] <= 5) &&
    ["planned", "ready", "in_progress", "blocked"].includes(item.status) && typeof item.description === "string";
  const escape = value => String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
  const statusName = value => ({ in_progress: "In progress" })[value] || value[0].toUpperCase() + value.slice(1);

  function updateSummary() {
    document.querySelector("#count-total").textContent = items.length;
    document.querySelector("#count-ready").textContent = items.filter(x => x.status === "ready").length;
    document.querySelector("#count-progress").textContent = items.filter(x => x.status === "in_progress").length;
    document.querySelector("#count-blocked").textContent = items.filter(x => x.status === "blocked").length;
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    const [key, direction] = sort.value.split("-");
    ordering = items.filter(item => (!query || `${item.id} ${item.title} ${item.description}`.toLocaleLowerCase().includes(query)) &&
      (status.value === "all" || item.status === status.value) && (risk.value === "all" || item.risk === Number(risk.value)));
    ordering.sort((a, b) => {
      const av = key === "priority" ? score(a) : key === "title" ? a.title.toLocaleLowerCase() : a[key];
      const bv = key === "priority" ? score(b) : key === "title" ? b.title.toLocaleLowerCase() : b[key];
      const primary = (av < bv ? -1 : av > bv ? 1 : 0) * (direction === "desc" ? -1 : 1);
      if (primary) return primary;
      if (key === "priority" && direction === "desc") return b.urgency - a.urgency || b.impact - a.impact || compareId(a.id, b.id);
      return compareId(a.id, b.id);
    });
    count.textContent = `${ordering.length} ${ordering.length === 1 ? "item" : "items"}`;
    message.hidden = ordering.length !== 0;
    message.className = "message empty";
    message.textContent = items.length ? "No backlog items match these filters. Try changing your search or filters." : "The backlog is valid and currently empty.";
    list.innerHTML = ordering.map((item, index) => {
      const details = item.id === openId;
      return `<article class="priority-item${details ? " is-open" : ""}" data-testid="priority-item">
        <span class="rank" aria-label="Rank ${index + 1}">${String(index + 1).padStart(2, "0")}</span>
        <div class="item-main"><div class="item-title-row"><h3>${escape(item.title)}</h3><span class="badge ${escape(item.status)}">${escape(statusName(item.status))}</span></div>
        <p class="item-id">${escape(item.id)}</p><div class="factors" aria-label="Scoring factors">${factors.map(key => `<span>${labels[key]} <b>${item[key]}</b></span>`).join("")}</div>
        ${details ? `<section class="detail" data-testid="item-detail" aria-label="Details for ${escape(item.title)}"><h4>Why it matters</h4><p>${escape(item.description)}</p><h4>Factor breakdown</h4><div class="breakdown">${factors.map(key => `<span>${labels[key]}<b>${item[key]} / 5</b></span>`).join("")}</div><p class="formula">Score = (2 × impact + 1.5 × urgency + confidence + 0.5 × risk) ÷ effort</p></section>` : ""}</div>
        <div class="score"><span>PRIORITY SCORE</span><strong>${score(item).toFixed(4)}</strong><button class="detail-toggle" type="button" aria-expanded="${details}" aria-label="${details ? "Hide" : "Show"} details for ${escape(item.title)}" data-id="${escape(item.id)}">${details ? "Close details" : "View details"}<span aria-hidden="true">${details ? "−" : "+"}</span></button></div>
      </article>`;
    }).join("");
    exportButton.disabled = false;
  }

  [search, status, risk, sort].forEach(control => control.addEventListener("input", render));
  list.addEventListener("click", event => {
    const button = event.target.closest("button[data-id]");
    if (!button) return;
    openId = openId === button.dataset.id ? null : button.dataset.id;
    render();
    list.querySelector("button[aria-expanded='true']")?.focus();
  });
  exportButton.addEventListener("click", () => {
    const file = new Blob([JSON.stringify(ordering, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(file);
    link.download = "priority-ordering.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  });

  fetch("/api/items").then(async response => {
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `Server returned ${response.status}`);
    if (!data || !Array.isArray(data.items) || data.items.some(item => !valid(item)) || new Set(data.items.map(item => item.id)).size !== data.items.length) {
      throw new Error("The backlog data is invalid. Check that every item has valid fields and a unique ID.");
    }
    items = data.items;
    updateSummary();
    render();
  }).catch(error => {
    exportButton.disabled = true;
    count.textContent = "";
    list.replaceChildren();
    message.hidden = false;
    message.className = "message error";
    message.textContent = `Unable to load backlog: ${error.message}`;
  });
})();
