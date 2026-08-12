/* SoD Module Studio: optional local UI over typed DevKit endpoints.
 * No framework and no external requests: all data stays on the loopback
 * service that served this document. */

"use strict";

const state = {
  editor: "atlas",
  plan: null,
  orderPlan: null,
  balancePlan: null,
  presentation: {
    presentationKey: null,
    canvasPayload: null,
    selectedOverlayId: null,
    plan: null,
    drafts: new Map(),
    overlayFilter: "",
  },
  content: {
    packs: [],
    catalogPackIds: new Set(),
    selectedPackId: null,
    draft: null,
    plan: null,
    selectedChangeId: null,
    catalogPlan: null,
    preview: null,
    review: null,
  },
};
const $ = (id) => document.getElementById(id);

function node(tag, properties = {}, children = []) {
  const element = document.createElement(tag);
  for (const [key, value] of Object.entries(properties)) {
    if (key === "class") element.className = value;
    else if (key === "text") element.textContent = value;
    else if (key.startsWith("on")) element.addEventListener(key.slice(2), value);
    else element.setAttribute(key, String(value));
  }
  for (const child of Array.isArray(children) ? children : [children]) {
    if (child !== null && child !== undefined) element.append(child);
  }
  return element;
}

function clear(element) { element.replaceChildren(); return element; }
function json(value) { return JSON.stringify(value, null, 2); }
function short(value, maximum = 180) {
  const text = String(value ?? "").replace(/\s+/g, " ").trim();
  return text.length <= maximum ? text : `${text.slice(0, maximum - 1)}…`;
}
function sourceLabel(source = {}) { return source.path ? `${source.path}:L${source.line ?? "?"}` : "source unavailable"; }
function apiError(message) { return node("div", { class: "result-message error", text: message }); }
function rawPanel(payload) { return node("pre", { class: "source-block", text: json(payload) }); }

async function request(path, options = {}) {
  const response = await fetch(path, { cache: "no-store", ...options });
  let envelope;
  try { envelope = await response.json(); }
  catch { throw new Error(`Studio returned non-JSON HTTP ${response.status}.`); }
  if (!response.ok || !envelope.ok) throw new Error(envelope.error || `Studio request failed (${response.status}).`);
  return envelope.result;
}

function setConnection(label, kind) {
  const item = $("connection");
  item.textContent = label;
  item.className = `status ${kind}`;
}

function metric(label, value, note = "") {
  const card = node("article", { class: "metric" });
  card.append(node("span", { class: "label", text: label }), node("strong", { class: "number", text: String(value) }));
  if (note) card.append(node("span", { class: "label", text: note }));
  return card;
}

function showView(name) {
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === name));
  document.querySelectorAll(".view").forEach((item) => item.classList.toggle("active", item.id === `view-${name}`));
}

async function loadOverview() {
  const cards = clear($("overview-cards"));
  $("overview-json").textContent = "Loading…";
  try {
    const payload = await request("/api/summary");
    const atlas = payload.module_atlas || {};
    const dialogue = payload.dialogue_composer || {};
    const presentations = payload.presentation_layout || {};
    const order = payload.order_control || {};
    const orderContracts = order.contracts || {};
    const doctor = payload.workbench_doctor || {};
    cards.append(
      metric("Atlas entities", atlas.entity_count ?? "?", `${atlas.edge_count ?? "?"} direct edges`),
      metric("Dialogue routes", dialogue.route_count ?? "?", `${dialogue.fallback_route_count ?? "?"} static fallbacks`),
      metric("Presentations", presentations.presentation_count ?? "?", `${presentations.overlay_count ?? "?"} direct overlays`),
      metric("Order contracts", orderContracts.active_blocker_count ?? "?", `${order.source_fragment_order?.fragment_count ?? "?"} ordered source fragments`),
      metric("Workbench", doctor.ready ? "ready" : "review", doctor.ready ? "catalogs and local inputs found" : "inspect doctor evidence")
    );
    $("overview-json").textContent = json(payload);
  } catch (error) {
    cards.append(apiError(error.message));
    $("overview-json").textContent = error.message;
  }
}

function appendDetailSection(parent, title, content) {
  const section = node("section", { class: "detail-section" });
  section.append(node("h4", { text: title }));
  if (typeof content === "string") section.append(node("p", { text: content }));
  else if (content) section.append(content);
  parent.append(section);
}

function chipList(values) {
  const wrapper = node("div");
  for (const value of values || []) wrapper.append(node("span", { class: "chip", text: String(value) }));
  return wrapper;
}

function atlasCard(entity) {
  const button = node("button", { class: "result-card" });
  button.append(
    node("span", { class: "result-title", text: entity.name || entity.entity_id }),
    node("span", { class: "result-meta", text: `${entity.area} · ${entity.kind} · ${sourceLabel(entity.source)}` }),
    node("span", { class: "result-snippet", text: short((entity.fields || []).map((field) => field.value).join(" · ") || (entity.symbols || []).join(" ")) })
  );
  button.addEventListener("click", () => inspectAtlas(entity.entity_id));
  return button;
}

async function atlasSearch(event) {
  event.preventDefault();
  const query = $("atlas-query").value.trim();
  const area = $("atlas-area").value;
  const kind = $("atlas-kind").value.trim();
  const results = clear($("atlas-results"));
  $("atlas-count").textContent = "";
  if (!query && area === "all" && !kind) {
    results.append(apiError("Enter a search term, choose an area, or supply an exact kind to keep the Atlas result bounded."));
    return;
  }
  results.append(node("div", { class: "empty", text: "Searching the Module Atlas…" }));
  try {
    const params = new URLSearchParams({ area, limit: "60" });
    if (query) params.set("query", query);
    if (kind) params.set("kind", kind);
    const payload = await request(`/api/atlas/find?${params}`);
    clear(results);
    $("atlas-count").textContent = `${payload.returned_count}/${payload.match_count}`;
    if (!payload.entities?.length) results.append(node("div", { class: "empty", text: "No matching semantic entities." }));
    else payload.entities.forEach((entity) => results.append(atlasCard(entity)));
  } catch (error) { clear(results).append(apiError(error.message)); }
}

async function inspectAtlas(entityId) {
  const detail = clear($("atlas-detail"));
  detail.append(node("div", { class: "empty", text: "Loading entity context and graph…" }));
  try {
    const [payload, graph] = await Promise.all([
      request(`/api/atlas/entity?id=${encodeURIComponent(entityId)}`),
      request(`/api/atlas/graph?id=${encodeURIComponent(entityId)}&depth=2&max_nodes=80`),
    ]);
    clear(detail);
    const entity = payload.entity || {};
    const header = node("div");
    header.append(node("h3", { text: entity.name || entityId }), node("p", { class: "muted", text: `${entity.area || "?"} · ${entity.kind || "?"} · ${sourceLabel(entity.source)}` }));
    const edit = node("button", { text: "Use in Module Atlas editor" });
    edit.addEventListener("click", () => setEditor("atlas", entity.entity_id, payload.semantic_actions));
    header.append(edit);
    detail.append(header);
    appendDetailSection(detail, "Available semantic actions", chipList(payload.semantic_actions));
    const links = payload.relationships || {};
    appendDetailSection(detail, "Static links", node("ul", { class: "detail-list" }, [
      node("li", { text: `${links.outbound_count ?? 0} outbound direct links` }),
      node("li", { text: `${links.inbound_count ?? 0} inbound direct links` }),
      node("li", { text: `${links.child_count ?? 0} child entities` }),
      node("li", { text: `Bounded graph: ${graph.node_count ?? 0} nodes / ${graph.edge_count ?? 0} edges` }),
    ]));
    if (payload.delegation) appendDetailSection(detail, "Specialist ownership", node("p", { class: "warning", text: payload.delegation }));
    appendDetailSection(detail, "Entity fields and operations", rawPanel({ fields: entity.fields, blocks: entity.blocks, generated_provenance: entity.generated_provenance }));
    appendDetailSection(detail, "Source / generated context", rawPanel(payload.source_context));
    appendDetailSection(detail, "Bounded dependency graph", rawPanel({ nodes: graph.nodes, edges: graph.edges, truncated: graph.truncated }));
  } catch (error) { clear(detail).append(apiError(error.message)); }
}

function dialogueCard(route) {
  const button = node("button", { class: "result-card" });
  button.append(
    node("span", { class: "result-title", text: `${route.input_state} → ${route.output_state}` }),
    node("span", { class: "result-meta", text: `${route.speaker} · ${sourceLabel(route.source)}` }),
    node("span", { class: "result-snippet", text: route.text || "(no static text)" })
  );
  button.addEventListener("click", () => inspectDialogue(route.route_id));
  return button;
}

async function dialogueSearch(event) {
  event.preventDefault();
  const query = $("dialogue-query").value.trim();
  const input = $("dialogue-input").value.trim();
  const output = $("dialogue-output").value.trim();
  const results = clear($("dialogue-results"));
  $("dialogue-count").textContent = "";
  if (!query && !input && !output) {
    results.append(apiError("Supply text, an input state, or an output state to keep route results bounded."));
    return;
  }
  results.append(node("div", { class: "empty", text: "Searching authored dialogue routes…" }));
  try {
    const params = new URLSearchParams({ limit: "60" });
    if (query) params.set("query", query);
    if (input) params.set("input_state", input);
    if (output) params.set("output_state", output);
    const payload = await request(`/api/dialogue/find?${params}`);
    clear(results);
    $("dialogue-count").textContent = `${payload.returned_count}/${payload.match_count}`;
    if (!payload.routes?.length) results.append(node("div", { class: "empty", text: "No matching authored routes." }));
    else payload.routes.forEach((route) => results.append(dialogueCard(route)));
  } catch (error) { clear(results).append(apiError(error.message)); }
}

async function inspectDialogue(routeId) {
  const detail = clear($("dialogue-detail"));
  detail.append(node("div", { class: "empty", text: "Loading route context and first-match analysis…" }));
  try {
    const payload = await request(`/api/dialogue/context?route_id=${encodeURIComponent(routeId)}`);
    clear(detail);
    const route = payload.route || {};
    const header = node("div");
    header.append(node("h3", { text: `${route.input_state || "?"} → ${route.output_state || "?"}` }), node("p", { class: "muted", text: `${route.speaker || "?"} · ${sourceLabel(route.source)}` }));
    const edit = node("button", { text: "Use in Dialogue editor" });
    edit.addEventListener("click", () => setEditor("dialogue", route.route_id, payload.edit_capabilities));
    header.append(edit);
    detail.append(header);
    appendDetailSection(detail, "Route text", node("p", { text: route.text || "(no static text)" }));
    appendDetailSection(detail, "Available semantic actions", chipList(payload.edit_capabilities));
    const analysis = payload.first_match_analysis || {};
    const warnings = analysis.warnings || [];
    appendDetailSection(detail, "First-match analysis", node("div", {}, [
      node("p", { class: warnings.length ? "warning" : "good-text", text: warnings.length ? `${warnings.length} static shadow/fallback warning(s)` : "No static first-match warning for this route." }),
      rawPanel(analysis),
    ]));
    appendDetailSection(detail, "Source / generated context", rawPanel(payload.source_context));
  } catch (error) { clear(detail).append(apiError(error.message)); }
}

function presentationCard(presentation) {
  const button = node("button", { class: "result-card", type: "button", "data-presentation-key": presentation.presentation_key });
  button.append(
    node("span", { class: "result-title", text: presentation.presentation_id || presentation.presentation_key }),
    node("span", { class: "result-meta", text: `${presentation.overlay_count ?? 0} overlays · ${sourceLabel(presentation.source)}` }),
    node("span", { class: "result-snippet", text: short((presentation.overlays || []).map((item) => `${item.identifier}: ${item.content || item.kind}`).join(" · ")) })
  );
  button.addEventListener("click", () => inspectPresentation(presentation.presentation_key));
  return button;
}

async function presentationSearch(event) {
  event.preventDefault();
  const query = $("presentation-query").value.trim();
  await runPresentationSearch(query);
}

async function runPresentationSearch(query) {
  const results = clear($("presentation-results"));
  $("presentation-count").textContent = "";
  if (!query) { results.append(apiError("Supply a presentation ID, overlay identifier, content fragment, or source term.")); return; }
  results.append(node("div", { class: "empty", text: "Searching direct presentation operations…" }));
  try {
    const payload = await request(`/api/presentation/find?${new URLSearchParams({ query, limit: "50" })}`);
    clear(results);
    $("presentation-count").textContent = `${payload.returned_count}/${payload.match_count}`;
    if (!payload.presentations?.length) results.append(node("div", { class: "empty", text: "No matching presentations." }));
    else payload.presentations.forEach((presentation) => results.append(presentationCard(presentation)));
  } catch (error) { clear(results).append(apiError(error.message)); }
}

async function browsePresentations() {
  $("presentation-query").value = "";
  await runPresentationSearch("*");
}

function componentNumber(component) {
  const value = component?.value;
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function refreshPresentationSearchSelection() {
  document.querySelectorAll("#presentation-results .result-card").forEach((item) => {
    item.classList.toggle("selected", item.dataset.presentationKey === state.presentation.presentationKey);
  });
}

function selectedPresentationOverlay() {
  const overlays = state.presentation.canvasPayload?.canvas?.overlays || [];
  return overlays.find((overlay) => overlay.overlay_id === state.presentation.selectedOverlayId) || null;
}

function selectedPresentation() {
  return state.presentation.canvasPayload?.presentation || null;
}

function presentationBasePosition(overlay) {
  return {
    x: componentNumber(overlay?.position?.x),
    y: componentNumber(overlay?.position?.y),
  };
}

function presentationDraftPosition(overlay) {
  return overlay ? state.presentation.drafts.get(overlay.overlay_id) || null : null;
}

function presentationPosition(overlay) {
  const base = presentationBasePosition(overlay);
  const draft = presentationDraftPosition(overlay);
  return { x: draft?.x ?? base.x, y: draft?.y ?? base.y, base, draft };
}

function presentationDraftCount() {
  return state.presentation.drafts.size;
}

function updatePresentationDraftStatus() {
  const count = presentationDraftCount();
  const selectedDraft = presentationDraftPosition(selectedPresentationOverlay());
  const label = $("presentation-draft-status");
  label.textContent = count
    ? `${count} local ${count === 1 ? "draft" : "drafts"}${selectedDraft ? " · selected" : ""}`
    : "No local draft";
  label.className = `status-label ${count ? "draft" : ""}`;
  $("presentation-reset-draft").disabled = !selectedDraft;
}

function setPresentationDraft(overlay, x, y) {
  const base = presentationBasePosition(overlay);
  if (base.x === null || base.y === null) return false;
  if (x === base.x && y === base.y) state.presentation.drafts.delete(overlay.overlay_id);
  else state.presentation.drafts.set(overlay.overlay_id, { x, y });
  updatePresentationDraftStatus();
  return true;
}

function canvasOverlayNode(overlayId) {
  return Array.from(document.querySelectorAll(".presentation-canvas .canvas-overlay"))
    .find((item) => item.dataset.overlayId === overlayId) || null;
}

function presentationOverlayIsTextual(overlay) {
  return ["text", "button", "game_button", "check_box", "combo_button"].includes(overlay?.kind);
}

function presentationOverlayIsMesh(overlay) {
  return ["mesh", "image", "image_button"].includes(overlay?.kind);
}

function setPresentationControlDisabled(ids, disabled) {
  for (const id of ids) $(id).disabled = disabled;
}

function clearPresentationPlan() {
  state.presentation.plan = null;
  $("presentation-plan-summary").className = "empty";
  $("presentation-plan-summary").textContent = "Select an overlay or presentation and review one proposed change.";
  $("presentation-plan-diff").textContent = "";
  setPresentationControlDisabled([
    "presentation-dry-run", "presentation-apply-check", "presentation-apply-confirmation", "presentation-apply-source",
  ], true);
  $("presentation-apply-check").checked = false;
  $("presentation-apply-confirmation").value = "";
  clear($("presentation-apply-result"));
}

function updatePresentationApplyButton() {
  const ready = Boolean(state.presentation.plan?.sha)
    && $("presentation-apply-check").checked
    && $("presentation-apply-confirmation").value === "APPLY SOURCE";
  $("presentation-apply-source").disabled = !ready;
}

function sourceExpression(component) {
  return component?.expression || "not directly anchored";
}

function setPresentationInspector(overlay) {
  const selected = Boolean(overlay);
  const position = presentationPosition(overlay);
  const positionX = position.x;
  const positionY = position.y;
  const sizeX = componentNumber(overlay?.size?.x);
  const sizeY = componentNumber(overlay?.size?.y);
  const moveSupported = selected && position.base.x !== null && position.base.y !== null;
  const resizeSupported = selected && sizeX !== null && sizeY !== null;
  const contentSupported = selected
    && overlay?.content_is_literal === true
    && (presentationOverlayIsTextual(overlay) || presentationOverlayIsMesh(overlay));
  const colorSupported = selected && Boolean(overlay?.color?.expression);
  const alphaSupported = selected && Boolean(overlay?.alpha?.expression);

  $("presentation-selected-status").textContent = selected
    ? `${overlay.kind || "overlay"} ${position.draft ? "local draft" : moveSupported ? "source-bound" : "dynamic"}`
    : "Nothing selected";
  $("presentation-selected-status").className = `status-label ${position.draft ? "draft" : selected && moveSupported ? "good" : selected ? "warning" : ""}`;
  const summary = clear($("presentation-selected-summary"));
  if (!selected) {
    summary.className = "empty";
    summary.textContent = "Click an overlay on the canvas or in the overlay list. Dragging changes only the local draft coordinates; it never writes source.";
  } else {
    summary.className = "selected-overlay-summary";
    summary.append(
      node("strong", { text: overlay.identifier || overlay.overlay_id }),
      node("span", { class: "muted", text: `${overlay.overlay_id} · ${overlay.trigger || "unknown trigger"} · ${sourceLabel(overlay.source)}` }),
      node("span", { class: position.draft ? "draft-note" : moveSupported ? "good-text" : "warning", text: position.draft ? `Local draft position ${positionX}, ${positionY}; source remains ${position.base.x}, ${position.base.y} until you review a move.` : moveSupported ? `Source anchor ${positionX}, ${positionY} via ${overlay.position?.register || "direct anchor"}` : "Position is dynamic or unresolved; inspect source context before attempting a layout move." }),
      node("span", { class: "muted", text: `Position source: x=${sourceExpression(overlay.position?.x)}, y=${sourceExpression(overlay.position?.y)}` }),
      node("span", { class: overlay.content_is_literal ? "muted" : "warning", text: overlay.content_is_literal ? `Direct literal content: ${overlay.content_literal || "(empty)"}` : `Content source expression: ${overlay.content || "none"}${(presentationOverlayIsTextual(overlay) || presentationOverlayIsMesh(overlay)) ? " — preserved; edit it through a source-aware string workflow." : ""}` }),
      node("span", { class: "muted", text: overlay.previous_string_writers?.length ? `Visible-text writer evidence: ${overlay.previous_string_writers.join(", ")}` : "No preceding static string-writer evidence for this overlay." }),
    );
  }

  $("presentation-position-x").value = positionX ?? "";
  $("presentation-position-y").value = positionY ?? "";
  $("presentation-size-x").value = sizeX ?? "";
  $("presentation-size-y").value = sizeY ?? "";
  $("presentation-content").value = overlay?.content_literal || "";
  $("presentation-color").value = overlay?.color?.expression || "";
  $("presentation-alpha").value = overlay?.alpha?.expression || "";
  setPresentationControlDisabled(["presentation-position-x", "presentation-position-y", "presentation-plan-move"], !moveSupported);
  setPresentationControlDisabled(["presentation-size-x", "presentation-size-y", "presentation-plan-resize"], !resizeSupported);
  setPresentationControlDisabled(["presentation-content", "presentation-plan-content"], !contentSupported);
  setPresentationControlDisabled(["presentation-color", "presentation-plan-color"], !colorSupported);
  setPresentationControlDisabled(["presentation-alpha", "presentation-plan-alpha"], !alphaSupported);
  setPresentationControlDisabled(["presentation-plan-remove"], !selected);
  document.querySelectorAll(".presentation-align").forEach((button) => { button.disabled = !moveSupported; });
  updatePresentationDraftStatus();
}

function refreshPresentationSelection() {
  const selectedId = state.presentation.selectedOverlayId;
  document.querySelectorAll(".presentation-canvas .canvas-overlay, #presentation-overlay-list .overlay-row").forEach((item) => {
    item.classList.toggle("selected", item.dataset.overlayId === selectedId);
  });
}

function selectPresentationOverlay(overlayId) {
  const overlay = (state.presentation.canvasPayload?.canvas?.overlays || []).find((item) => item.overlay_id === overlayId);
  if (!overlay) return;
  state.presentation.selectedOverlayId = overlayId;
  clearPresentationPlan();
  setPresentationInspector(overlay);
  refreshPresentationSelection();
}

function syncPresentationDraftFromInputs() {
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  const rawX = $("presentation-position-x").value.trim();
  const rawY = $("presentation-position-y").value.trim();
  if (!rawX || !rawY) return;
  const x = Number(rawX);
  const y = Number(rawY);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return;
  if (!setPresentationDraft(overlay, x, y)) return;
  const overlayNode = canvasOverlayNode(overlay.overlay_id);
  if (overlayNode) {
    applyDraftCanvasPosition(overlayNode, overlay, x, y);
    overlayNode.classList.toggle("drafted", Boolean(presentationDraftPosition(overlay)));
  }
}

function resetSelectedPresentationDraft() {
  const overlay = selectedPresentationOverlay();
  const base = presentationBasePosition(overlay);
  if (!overlay || base.x === null || base.y === null || !presentationDraftPosition(overlay)) return;
  state.presentation.drafts.delete(overlay.overlay_id);
  $("presentation-position-x").value = base.x;
  $("presentation-position-y").value = base.y;
  const overlayNode = canvasOverlayNode(overlay.overlay_id);
  if (overlayNode) {
    applyDraftCanvasPosition(overlayNode, overlay, base.x, base.y);
    overlayNode.classList.remove("drafted");
  }
  clearPresentationPlan();
  refreshSelectedPresentationInspector();
}

function refreshSelectedPresentationInspector() {
  const overlay = selectedPresentationOverlay();
  if (overlay) setPresentationInspector(overlay);
  if (state.presentation.canvasPayload) renderPresentationOverlayList(state.presentation.canvasPayload);
}

function coordinateValue(id, label) {
  const raw = $(id).value.trim();
  const value = Number(raw);
  if (!raw || !Number.isFinite(value)) throw new Error(`${label} must be a finite number.`);
  return value;
}

function applyDraftCanvasPosition(overlayNode, overlay, x, y) {
  const canvas = state.presentation.canvasPayload?.canvas;
  const rect = overlay.canvas_box;
  if (!canvas || !rect) return;
  overlayNode.style.left = `${(x / 1000) * 100}%`;
  overlayNode.style.top = `${100 - (y / 1000) * 100 - (rect.height / canvas.height) * 100}%`;
}

function attachCanvasDrag(overlayNode, overlay) {
  const startX = componentNumber(overlay.position?.x);
  const startY = componentNumber(overlay.position?.y);
  if (startX === null || startY === null) return;
  overlayNode.classList.add("draggable");
  overlayNode.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    event.preventDefault();
    selectPresentationOverlay(overlay.overlay_id);
    const canvasNode = overlayNode.closest(".presentation-canvas");
    if (!canvasNode) return;
    const bounds = canvasNode.getBoundingClientRect();
    const origin = { x: event.clientX, y: event.clientY, startX, startY, bounds };
    overlayNode.classList.add("dragging");
    overlayNode.setPointerCapture(event.pointerId);
    const move = (pointerEvent) => {
      const nextX = Math.round(origin.startX + ((pointerEvent.clientX - origin.x) / origin.bounds.width) * 1000);
      const nextY = Math.round(origin.startY - ((pointerEvent.clientY - origin.y) / origin.bounds.height) * 1000);
      $("presentation-position-x").value = nextX;
      $("presentation-position-y").value = nextY;
      setPresentationDraft(overlay, nextX, nextY);
      applyDraftCanvasPosition(overlayNode, overlay, nextX, nextY);
      overlayNode.classList.toggle("drafted", Boolean(presentationDraftPosition(overlay)));
    };
    const finish = () => {
      overlayNode.classList.remove("dragging");
      overlayNode.dataset.suppressClick = "true";
      overlayNode.removeEventListener("pointermove", move);
      overlayNode.removeEventListener("pointerup", finish);
      overlayNode.removeEventListener("pointercancel", finish);
      refreshSelectedPresentationInspector();
    };
    overlayNode.addEventListener("pointermove", move);
    overlayNode.addEventListener("pointerup", finish);
    overlayNode.addEventListener("pointercancel", finish);
  });
}

function renderPresentationCanvas(canvasPayload) {
  const canvas = canvasPayload.canvas || {};
  const box = node("div", { class: "canvas presentation-canvas", "aria-label": "Static presentation layout canvas" });
  const guide = node("div", { class: "canvas-coordinate-guide", "aria-hidden": "true" }, [
    node("span", { class: "canvas-corner top-left", text: "0 · 1000" }),
    node("span", { class: "canvas-corner top-right", text: "1000 · 1000" }),
    node("span", { class: "canvas-corner bottom-left", text: "0 · 0" }),
    node("span", { class: "canvas-corner bottom-right", text: "1000 · 0" }),
  ]);
  box.append(guide);
  for (const overlay of canvas.overlays || []) {
    const rect = overlay.canvas_box;
    if (!rect) continue;
    const overlayNode = node("button", {
      class: `canvas-overlay ${overlay.kind || "unknown"}`,
      type: "button",
      "data-overlay-id": overlay.overlay_id,
      text: short(`${overlay.identifier}${overlay.content ? ` · ${overlay.content}` : ""}`, 68),
    });
    const draft = presentationDraftPosition(overlay);
    if (draft) applyDraftCanvasPosition(overlayNode, overlay, draft.x, draft.y);
    else {
      overlayNode.style.left = `${(rect.x / canvas.width) * 100}%`;
      overlayNode.style.top = `${(rect.y / canvas.height) * 100}%`;
    }
    overlayNode.style.width = `${Math.max((rect.width / canvas.width) * 100, 2)}%`;
    overlayNode.style.height = `${Math.max((rect.height / canvas.height) * 100, 2)}%`;
    overlayNode.classList.toggle("drafted", Boolean(draft));
    overlayNode.title = `${overlay.identifier}\n${overlay.overlay_id}${draft ? "\nLocal draft: source has not changed." : ""}\nDrag only drafts a move; review a source diff to make it real.`;
    overlayNode.addEventListener("click", () => {
      if (overlayNode.dataset.suppressClick === "true") {
        delete overlayNode.dataset.suppressClick;
        return;
      }
      selectPresentationOverlay(overlay.overlay_id);
    });
    overlayNode.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectPresentationOverlay(overlay.overlay_id);
      }
    });
    attachCanvasDrag(overlayNode, overlay);
    box.append(overlayNode);
  }
  return box;
}

function renderPresentationOverlayList(payload) {
  const list = clear($("presentation-overlay-list"));
  const allOverlays = payload.canvas?.overlays || [];
  const needle = state.presentation.overlayFilter.trim().toLocaleLowerCase();
  const overlays = needle
    ? allOverlays.filter((overlay) => [overlay.identifier, overlay.kind, overlay.content, overlay.trigger, overlay.overlay_id]
      .some((value) => String(value || "").toLocaleLowerCase().includes(needle)))
    : allOverlays;
  $("presentation-overlay-count").textContent = allOverlays.length ? `${overlays.length}/${allOverlays.length}` : "";
  if (!overlays.length) {
    list.className = "overlay-list empty";
    list.textContent = needle ? "No direct overlays match this filter." : "No direct static overlays were returned for this presentation.";
    return;
  }
  list.className = "overlay-list";
  for (const overlay of overlays) {
    const position = overlay.position || {};
    const x = componentNumber(position.x);
    const y = componentNumber(position.y);
    const draft = presentationDraftPosition(overlay);
    const button = node("button", { class: "overlay-row", type: "button", "data-overlay-id": overlay.overlay_id });
    button.append(
      node("span", { class: "overlay-row-heading" }, [
        node("strong", { text: overlay.identifier || overlay.overlay_id }),
        node("span", { class: `overlay-kind ${overlay.kind || "unknown"}`, text: overlay.kind || "unknown" }),
      ]),
      node("span", { class: "muted", text: `${overlay.kind || "unknown"} · ${overlay.trigger || "unknown trigger"}` }),
      node("span", { class: draft ? "draft-note" : x !== null && y !== null ? "good-text" : "warning", text: draft ? `draft x ${draft.x}, y ${draft.y}` : x !== null && y !== null ? `source x ${x}, y ${y}` : "dynamic / unresolved position" }),
    );
    button.addEventListener("click", () => selectPresentationOverlay(overlay.overlay_id));
    list.append(button);
  }
  refreshPresentationSelection();
}

function configurePresentationCreateForm(presentation) {
  const triggers = presentation?.triggers || [];
  const trigger = clear($("presentation-create-trigger"));
  for (const item of triggers) trigger.append(node("option", { value: item.name, text: `${item.name} (${item.operation_count} operations)` }));
  const available = Boolean(presentation && triggers.length);
  setPresentationControlDisabled([
    "presentation-create-kind", "presentation-create-trigger", "presentation-create-destination", "presentation-create-content",
    "presentation-create-register", "presentation-create-x", "presentation-create-y", "presentation-create-size-x",
    "presentation-create-size-y", "presentation-create-minimum", "presentation-create-maximum", "presentation-plan-create",
  ], !available);
  syncPresentationCreateControls();
}

function syncPresentationCreateControls() {
  const kind = $("presentation-create-kind").value;
  const ready = Boolean(selectedPresentation());
  const content = $("presentation-create-content");
  content.placeholder = kind === "mesh" ? "mesh name" : kind === "slider" ? "not used by a slider" : "@Visible text";
  const slider = kind === "slider";
  $("presentation-create-minimum").disabled = !ready || !slider;
  $("presentation-create-maximum").disabled = !ready || !slider;
  content.disabled = !ready || slider;
}

function presentationPlanRequest(action, target, fields = {}) {
  if (!target) throw new Error("Select a presentation or overlay first.");
  return { target, action, ...fields };
}

function renderPresentationPlan(payload, requestPayload) {
  const plan = payload.change_router_plan || {};
  const semantic = payload.semantic_operation || {};
  state.presentation.plan = { request: requestPayload, sha: plan.target?.base_sha256, presentationKey: state.presentation.presentationKey, payload };
  const summary = clear($("presentation-plan-summary"));
  summary.className = "";
  summary.append(
    node("p", { text: `Action: ${semantic.action || requestPayload.action} · target: ${plan.target?.path || "?"}` }),
    node("p", { class: "muted", text: `Base SHA-256: ${plan.target?.base_sha256 || "unavailable"}` }),
  );
  if (semantic.shared_binding_impact?.length) {
    summary.append(node("p", { class: "warning", text: "This edit shares position/size bindings with other overlays. Inspect the returned impact before apply." }), rawPanel(semantic.shared_binding_impact));
  } else if (payload.warnings?.length) {
    summary.append(node("p", { class: "muted", text: payload.warnings.join(" ") }));
  }
  if (requestPayload.action === "move_overlay" && presentationDraftCount() > 1) {
    summary.append(node("p", { class: "draft-note", text: `${presentationDraftCount()} local move drafts are staged. This plan covers only the selected overlay; review each remaining draft separately.` }));
  }
  $("presentation-plan-diff").textContent = plan.unified_diff || "No unified diff was returned.";
  const enabled = Boolean(state.presentation.plan.sha);
  setPresentationControlDisabled(["presentation-dry-run", "presentation-apply-check", "presentation-apply-confirmation"], !enabled);
  updatePresentationApplyButton();
}

async function planPresentationAction(action, target, fields = {}) {
  clearPresentationPlan();
  try {
    const body = presentationPlanRequest(action, target, fields);
    const result = await request("/api/presentation/patch", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    renderPresentationPlan(result, body);
  } catch (error) {
    $("presentation-plan-summary").className = "result-message error";
    $("presentation-plan-summary").textContent = error.message;
  }
}

async function planPresentationMove(event) {
  event.preventDefault();
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  await planPresentationAction("move_overlay", overlay.overlay_id, {
    x: coordinateValue("presentation-position-x", "Position X"),
    y: coordinateValue("presentation-position-y", "Position Y"),
  });
}

async function planPresentationResize() {
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  await planPresentationAction("resize_overlay", overlay.overlay_id, {
    x: coordinateValue("presentation-size-x", "Engine size X"),
    y: coordinateValue("presentation-size-y", "Engine size Y"),
  });
}

async function planPresentationContent() {
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  const action = presentationOverlayIsMesh(overlay) ? "set_mesh" : "set_text";
  await planPresentationAction(action, overlay.overlay_id, { value: $("presentation-content").value });
}

async function planPresentationColor() {
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  const value = $("presentation-color").value.trim();
  if (!value) throw new Error("Color expression is required.");
  await planPresentationAction("set_color", overlay.overlay_id, { value });
}

async function planPresentationAlpha() {
  const overlay = selectedPresentationOverlay();
  if (!overlay) return;
  const value = $("presentation-alpha").value.trim();
  if (!value) throw new Error("Alpha expression is required.");
  await planPresentationAction("set_alpha", overlay.overlay_id, { value });
}

async function planPresentationCreate(event) {
  event.preventDefault();
  const presentation = selectedPresentation();
  if (!presentation) return;
  try {
    const kind = $("presentation-create-kind").value;
    const newOverlay = {
      kind,
      destination: $("presentation-create-destination").value.trim(),
      position_register: $("presentation-create-register").value.trim() || "pos1",
      x: coordinateValue("presentation-create-x", "New overlay position X"),
      y: coordinateValue("presentation-create-y", "New overlay position Y"),
    };
    const sizeX = $("presentation-create-size-x").value.trim();
    const sizeY = $("presentation-create-size-y").value.trim();
    if (sizeX || sizeY) {
      newOverlay.size_x = coordinateValue("presentation-create-size-x", "New overlay size X");
      newOverlay.size_y = coordinateValue("presentation-create-size-y", "New overlay size Y");
    }
    if (kind === "mesh") newOverlay.mesh = $("presentation-create-content").value.trim();
    else if (kind === "slider") {
      newOverlay.minimum = coordinateValue("presentation-create-minimum", "Slider minimum");
      newOverlay.maximum = coordinateValue("presentation-create-maximum", "Slider maximum");
    } else newOverlay.text = $("presentation-create-content").value;
    await planPresentationAction("add_overlay", presentation.presentation_key, {
      trigger: $("presentation-create-trigger").value,
      new_overlay: newOverlay,
    });
  } catch (error) {
    $("presentation-plan-summary").className = "result-message error";
    $("presentation-plan-summary").textContent = error.message;
  }
}

async function runPresentationApply(dryRun) {
  const plan = state.presentation.plan;
  if (!plan) return;
  const result = clear($("presentation-apply-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the current SHA-guarded presentation change..." : "Applying the reviewed presentation source change...";
  try {
    const body = { ...plan.request, expected_sha256: plan.sha, dry_run: dryRun };
    if (!dryRun) body.confirmation = "APPLY SOURCE";
    const payload = await request("/api/presentation/apply", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      setPresentationControlDisabled(["presentation-apply-source", "presentation-apply-check", "presentation-apply-confirmation"], true);
      await inspectPresentation(plan.presentationKey);
      const refreshed = $("presentation-apply-result");
      refreshed.className = "result-message good";
      refreshed.textContent = "Source change applied through the reviewed SHA guard. The static canvas has been refreshed; run the normal reviewed build before in-game validation.";
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function inspectPresentation(presentationId) {
  const detail = clear($("presentation-detail"));
  detail.append(node("div", { class: "empty", text: "Reconstructing the direct static overlay canvas..." }));
  $("presentation-refresh-canvas").disabled = true;
  try {
    const payload = await request(`/api/presentation/canvas?presentation_id=${encodeURIComponent(presentationId)}&width=1024&height=768&overlay_limit=500`);
    state.presentation.presentationKey = payload.presentation?.presentation_key || presentationId;
    state.presentation.canvasPayload = payload;
    state.presentation.selectedOverlayId = null;
    state.presentation.drafts.clear();
    state.presentation.overlayFilter = "";
    $("presentation-overlay-filter").value = "";
    $("presentation-overlay-filter").disabled = false;
    clearPresentationPlan();
    setPresentationInspector(null);
    configurePresentationCreateForm(payload.presentation);
    refreshPresentationSearchSelection();
    $("presentation-stage-title").textContent = payload.presentation?.presentation_id || presentationId;
    const overlays = payload.canvas?.overlays || [];
    const staticCount = overlays.filter((overlay) => overlay.canvas_box).length;
    const unresolvedCount = overlays.length - staticCount;
    const shown = payload.canvas?.returned_overlay_count ?? overlays.length;
    const total = payload.canvas?.overlay_count ?? payload.presentation?.overlay_count ?? overlays.length;
    const scope = shown < total ? `showing ${shown} of ${total}` : `${total} direct overlays`;
    $("presentation-stage-meta").textContent = `${scope} · ${staticCount} static · ${unresolvedCount} unresolved · ${sourceLabel(payload.presentation?.source)}`;
    $("presentation-refresh-canvas").disabled = false;
    clear(detail).append(renderPresentationCanvas(payload));
    const findings = payload.findings || [];
    if (findings.length) appendDetailSection(detail, "Static canvas findings", rawPanel(findings));
    else appendDetailSection(detail, "Static canvas findings", node("p", { class: "good-text", text: "No bounded static canvas finding." }));
    const unresolved = (payload.canvas?.overlays || []).filter((overlay) => !overlay.canvas_box).length;
    if (unresolved) appendDetailSection(detail, "Unresolved overlays", node("p", { class: "warning", text: `${unresolved} overlay(s) have dynamic or unresolved coordinates and are listed below without a guessed canvas box.` }));
    appendDetailSection(detail, "Canvas boundary", node("p", { class: "warning", text: (payload.warnings || []).join(" ") }));
    renderPresentationOverlayList(payload);
  } catch (error) {
    clear(detail).append(apiError(error.message));
    $("presentation-stage-title").textContent = "Static canvas";
    $("presentation-stage-meta").textContent = "Choose a presentation to reconstruct its bounded static canvas.";
  }
}

function cloneJson(value) { return JSON.parse(JSON.stringify(value)); }

function emptyContentPack() {
  return {
    schema: "sod-modern.content-pack.v1",
    id: "new-content-pack",
    title: "New Content Pack",
    status: "draft",
    description: "A typed player-facing content contract awaiting its first review.",
    brief: {
      summary: "Describe the player-facing outcome this pack is responsible for.",
      lore_constraints: [],
      tone: [],
      acceptance_criteria: ["Define at least one observable acceptance criterion before planning."],
    },
    slices: { dialogue: { changes: [], beats: [] } },
    verification: { tests: [], require_blueprint: false, scenarios: [] },
  };
}

function contentLines(id, label, required = false) {
  const values = $(id).value.split(/\r?\n/).map((value) => value.trim()).filter(Boolean);
  if (required && !values.length) throw new Error(`${label} needs at least one line.`);
  const duplicate = values.find((value, index) => values.indexOf(value) !== index);
  if (duplicate) throw new Error(`${label} repeats ${JSON.stringify(duplicate)}.`);
  return values;
}

function contentJsonArray(id, label) {
  const raw = $(id).value.trim();
  if (!raw) return [];
  try {
    const value = JSON.parse(raw);
    if (!Array.isArray(value)) throw new Error("it must be an array");
    return value;
  } catch (error) {
    throw new Error(`${label} must be valid JSON array data: ${error.message}`);
  }
}

function contentField(id, label) {
  const value = $(id).value.trim();
  if (!value) throw new Error(`${label} is required.`);
  return value;
}

function contentDraftFromForm() {
  const draft = {
    schema: "sod-modern.content-pack.v1",
    id: contentField("content-id", "Pack ID"),
    title: contentField("content-title", "Title"),
    status: $("content-status").value,
    description: contentField("content-description", "Ownership / description"),
    brief: {
      summary: contentField("content-brief-summary", "Player-facing summary"),
      lore_constraints: contentLines("content-lore", "Lore constraints"),
      tone: contentLines("content-tone", "Tone"),
      acceptance_criteria: contentLines("content-acceptance", "Acceptance criteria", true),
    },
    slices: {},
    verification: {
      tests: contentLines("content-tests", "Focused tests"),
      require_blueprint: $("content-require-blueprint").checked,
      scenarios: contentLines("content-verification-scenarios", "Verification scenarios"),
    },
  };
  const blueprint = $("content-blueprint").value.trim();
  if (blueprint) draft.blueprint_id = blueprint;
  if ($("content-use-dialogue").checked) {
    draft.slices.dialogue = {
      beats: contentJsonArray("content-dialogue-beats", "Dialogue beats"),
      changes: contentJsonArray("content-dialogue-changes", "Dialogue changes"),
    };
  }
  if ($("content-use-quest").checked) {
    draft.slices.quest_event = {
      timeline: contentJsonArray("content-quest-timeline", "Quest/event timeline"),
      changes: contentJsonArray("content-quest-changes", "Quest/event changes"),
    };
  }
  if ($("content-use-ai").checked) {
    draft.slices.campaign_ai = {
      contracts: contentJsonArray("content-ai-contracts", "Campaign AI contracts"),
      scenarios: contentLines("content-ai-scenarios", "Campaign AI scenarios"),
      changes: contentJsonArray("content-ai-changes", "Campaign AI changes"),
    };
  }
  if ($("content-use-presentation").checked) {
    draft.slices.presentation = {
      screens: contentJsonArray("content-presentation-screens", "Presentation screens"),
      new_presentations: contentJsonArray("content-presentation-new", "New presentation declarations"),
      changes: contentJsonArray("content-presentation-changes", "Presentation changes"),
    };
  }
  if ($("content-use-balance").checked) {
    draft.slices.troop_item = { records: contentJsonArray("content-balance-records", "Troop/item records") };
  }
  if (!Object.keys(draft.slices).length) throw new Error("Select at least one content slice.");
  return draft;
}

function contentFormControlsDisabled(disabled) {
  document.querySelectorAll("#content-pack-form input, #content-pack-form select, #content-pack-form textarea, #content-pack-form button, .content-slices-panel input, .content-slices-panel textarea, #content-raw-pack, #content-use-raw")
    .forEach((element) => { element.disabled = disabled; });
  ["content-validate", "content-plan", "content-preview", "content-review", "content-verify", "content-verify-scenarios", "content-verify-tests", "content-catalog-plan"]
    .forEach((id) => { $(id).disabled = disabled; });
}

function contentDraftMetadata(draft) {
  const slices = Object.keys(draft?.slices || {}).map((value) => value.replace("_", " "));
  return `${draft?.status || "draft"} | ${slices.length ? slices.join(", ") : "no slices"} | local typed draft`;
}

function clearContentPlan() {
  state.content.plan = null;
  state.content.selectedChangeId = null;
  $("content-plan-summary").className = "empty";
  $("content-plan-summary").textContent = "Plan a valid local pack to inspect its independent source/balance changes and current SHA guards.";
  clear($("content-plan-list")).append(node("div", { class: "empty", text: "No content plan is loaded." }));
  clear($("content-change-select"));
  $("content-change-select").disabled = true;
  $("content-change-diff").textContent = "";
  $("content-dry-run").disabled = true;
  $("content-apply-check").checked = false;
  $("content-apply-check").disabled = true;
  $("content-legacy-ack").checked = false;
  $("content-legacy-ack").disabled = true;
  $("content-protected-ack").checked = false;
  $("content-protected-ack").disabled = true;
  $("content-apply-confirmation").value = "";
  $("content-apply-confirmation").disabled = true;
  $("content-apply-source").disabled = true;
  clear($("content-apply-result"));
}

function clearContentCatalogPlan() {
  state.content.catalogPlan = null;
  $("content-catalog-summary").className = "empty";
  $("content-catalog-summary").textContent = "Sync a valid local draft, then review the catalog diff before saving it.";
  $("content-catalog-diff").textContent = "";
  $("content-catalog-dry-run").disabled = true;
  $("content-catalog-apply-check").checked = false;
  $("content-catalog-apply-check").disabled = true;
  $("content-catalog-confirmation").value = "";
  $("content-catalog-confirmation").disabled = true;
  $("content-catalog-apply").disabled = true;
  clear($("content-catalog-result"));
}

function renderContentDraft() {
  const draft = state.content.draft;
  const enabled = Boolean(draft);
  contentFormControlsDisabled(!enabled);
  if (!draft) {
    $("content-draft-title").textContent = "No pack selected";
    $("content-draft-meta").textContent = "Load a checked-in pack or start a new draft. Editing remains local until a strict catalog save plan is reviewed.";
    $("content-pack-status").className = "status-label";
    $("content-pack-status").textContent = "No local draft";
    $("content-raw-pack").value = "";
    return;
  }
  $("content-id").value = draft.id || "";
  $("content-title").value = draft.title || "";
  $("content-status").value = draft.status || "draft";
  $("content-blueprint").value = draft.blueprint_id || "";
  $("content-description").value = draft.description || "";
  $("content-brief-summary").value = draft.brief?.summary || "";
  $("content-lore").value = (draft.brief?.lore_constraints || []).join("\n");
  $("content-tone").value = (draft.brief?.tone || []).join("\n");
  $("content-acceptance").value = (draft.brief?.acceptance_criteria || []).join("\n");
  $("content-tests").value = (draft.verification?.tests || []).join("\n");
  $("content-verification-scenarios").value = (draft.verification?.scenarios || []).join("\n");
  $("content-require-blueprint").checked = Boolean(draft.verification?.require_blueprint);
  const slices = draft.slices || {};
  $("content-use-dialogue").checked = Boolean(slices.dialogue);
  $("content-use-quest").checked = Boolean(slices.quest_event);
  $("content-use-ai").checked = Boolean(slices.campaign_ai);
  $("content-use-presentation").checked = Boolean(slices.presentation);
  $("content-use-balance").checked = Boolean(slices.troop_item);
  $("content-dialogue-beats").value = json(slices.dialogue?.beats || []);
  $("content-dialogue-changes").value = json(slices.dialogue?.changes || []);
  $("content-quest-timeline").value = json(slices.quest_event?.timeline || []);
  $("content-quest-changes").value = json(slices.quest_event?.changes || []);
  $("content-ai-contracts").value = json(slices.campaign_ai?.contracts || []);
  $("content-ai-scenarios").value = (slices.campaign_ai?.scenarios || []).join("\n");
  $("content-ai-changes").value = json(slices.campaign_ai?.changes || []);
  $("content-presentation-screens").value = json(slices.presentation?.screens || []);
  $("content-presentation-new").value = json(slices.presentation?.new_presentations || []);
  $("content-presentation-changes").value = json(slices.presentation?.changes || []);
  $("content-balance-records").value = json(slices.troop_item?.records || []);
  $("content-raw-pack").value = json(draft);
  $("content-draft-title").textContent = draft.title || draft.id;
  $("content-draft-meta").textContent = contentDraftMetadata(draft);
  $("content-pack-status").className = "status-label draft";
  $("content-pack-status").textContent = state.content.catalogPackIds.has(draft.id) ? "Checked-in pack draft" : "Unsaved local draft";
}

function syncContentDraft(event) {
  event?.preventDefault();
  try {
    state.content.draft = contentDraftFromForm();
    state.content.selectedPackId = state.content.catalogPackIds.has(state.content.draft.id) ? state.content.draft.id : null;
    clearContentPlan();
    clearContentCatalogPlan();
    renderContentDraft();
    const result = clear($("content-action-result"));
    result.className = "result-message good";
    result.textContent = "Local strict pack draft synchronized. Validate, preview, or plan it before saving or applying anything.";
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function useContentRawDraft() {
  try {
    const raw = $("content-raw-pack").value.trim();
    if (!raw) throw new Error("Advanced pack JSON is empty.");
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("Advanced pack JSON must be one object.");
    state.content.draft = parsed;
    state.content.selectedPackId = state.content.catalogPackIds.has(parsed.id) ? parsed.id : null;
    clearContentPlan();
    clearContentCatalogPlan();
    renderContentDraft();
    const result = clear($("content-action-result"));
    result.className = "result-message good";
    result.textContent = "Advanced JSON is now a local draft. Validate it before any preview, plan, or catalog save.";
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = `Advanced JSON was not loaded: ${error.message}`;
  }
}

function renderContentPackList() {
  const results = clear($("content-pack-results"));
  const needle = $("content-query").value.trim().toLocaleLowerCase();
  const slice = $("content-slice-filter").value;
  const packs = state.content.packs.filter((pack) => {
    if (slice !== "all" && !pack.slices?.some((item) => item.id === slice)) return false;
    return !needle || JSON.stringify(pack).toLocaleLowerCase().includes(needle);
  });
  $("content-pack-count").textContent = state.content.packs.length ? `${packs.length}/${state.content.packs.length}` : "";
  if (!packs.length) {
    results.append(node("div", { class: "empty", text: "No checked-in content pack matches this filter." }));
    return;
  }
  packs.forEach((pack) => {
    const button = node("button", { class: "result-card", type: "button" });
    button.classList.toggle("selected", state.content.selectedPackId === pack.id);
    button.append(
      node("span", { class: "result-title", text: pack.title || pack.id }),
      node("span", { class: "result-meta", text: `${pack.id} | ${pack.status} | ${(pack.slices || []).map((item) => item.id).join(", ") || "no slices"}` }),
      node("span", { class: "result-snippet", text: short(pack.description || pack.brief?.summary || "") })
    );
    button.addEventListener("click", () => loadContentPack(pack.id));
    results.append(button);
  });
}

async function loadContentSummary() {
  const results = clear($("content-pack-results"));
  results.append(node("div", { class: "empty", text: "Loading checked-in typed content packs..." }));
  try {
    const payload = await request("/api/content/summary?limit=200");
    state.content.packs = payload.packs || [];
    state.content.catalogPackIds = new Set(state.content.packs.map((pack) => pack.id));
    renderContentPackList();
  } catch (error) {
    clear(results).append(apiError(error.message));
  }
}

async function loadContentPack(packId) {
  const result = clear($("content-action-result"));
  result.className = "result-message";
  result.textContent = "Loading the checked-in pack, entrypoint evidence, and strict local draft...";
  try {
    const payload = await request(`/api/content/explain?pack_id=${encodeURIComponent(packId)}&trace_limit=12`);
    state.content.draft = cloneJson(payload.pack_source);
    state.content.selectedPackId = packId;
    state.content.preview = null;
    state.content.review = null;
    clearContentPlan();
    clearContentCatalogPlan();
    renderContentDraft();
    renderContentPackList();
    result.className = "result-message good";
    result.textContent = payload.state === "ready"
      ? "Loaded checked-in pack as a local typed draft. Edit it, then validate/preview/plan before a reviewed catalog save."
      : `Loaded the pack, but its current static evidence is ${payload.state}. Inspect validation before editing.`;
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function newContentPack() {
  state.content.draft = emptyContentPack();
  state.content.selectedPackId = null;
  state.content.preview = null;
  state.content.review = null;
  clearContentPlan();
  clearContentCatalogPlan();
  renderContentDraft();
  renderContentPackList();
  const result = clear($("content-action-result"));
  result.className = "result-message good";
  result.textContent = "New local draft created. Give it a stable ID, player-facing brief, at least one slice, and reviewable acceptance criteria.";
  $("content-id").focus();
}

function currentContentDraft() {
  const draft = contentDraftFromForm();
  state.content.draft = draft;
  return draft;
}

function renderContentAction(payload, title) {
  const result = clear($("content-action-result"));
  result.className = payload.state === "blocked" || payload.state === "failed" ? "result-message error" : "result-message good";
  const errors = payload.errors || payload.validation?.errors || [];
  const warnings = payload.warnings || [];
  result.append(
    node("strong", { text: `${title}: ${payload.state || "ready"}` }),
    node("p", { text: errors.length ? `${errors.length} blocking evidence item(s).` : "No returned blocking evidence." })
  );
  if (errors.length) result.append(rawPanel(errors));
  else if (warnings.length) result.append(node("p", { class: "muted", text: short(warnings.join(" "), 520) }));
}

async function validateContentDraft() {
  try {
    const draft = currentContentDraft();
    const payload = await request("/api/content/validate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack: draft }) });
    renderContentAction(payload, "Content contract validation");
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function contentPlanDiff(change) {
  if (change.backend === "feature_authoring") return change.source_plan?.change_router_plan?.unified_diff || "No specialist source diff was returned.";
  if (change.backend === "troop_item_balance") return change.balance_plan?.unified_diff || "No Balance Lab diff was returned.";
  return "No supported specialist diff was returned.";
}

function selectedContentChange() {
  return state.content.plan?.payload?.changes?.find((change) => change.change_id === state.content.selectedChangeId) || null;
}

function contentChangeProtection(change) {
  const balance = change?.balance_plan || {};
  return {
    legacy: change?.backend === "troop_item_balance",
    protected: Boolean(balance.entity?.protected_legacy_record),
  };
}

function updateContentApplyButton() {
  const change = selectedContentChange();
  const protection = contentChangeProtection(change);
  const ready = Boolean(change?.apply_available && change?.expected_sha256)
    && $("content-apply-check").checked
    && $("content-apply-confirmation").value === "APPLY SOURCE"
    && (!protection.legacy || $("content-legacy-ack").checked)
    && (!protection.protected || $("content-protected-ack").checked);
  $("content-apply-source").disabled = !ready;
}

function selectContentChange(changeId) {
  state.content.selectedChangeId = changeId || null;
  const change = selectedContentChange();
  $("content-change-select").value = state.content.selectedChangeId || "";
  document.querySelectorAll("#content-plan-list .content-change-row").forEach((row) => row.classList.toggle("selected", row.dataset.changeId === state.content.selectedChangeId));
  $("content-change-diff").textContent = change ? contentPlanDiff(change) : "";
  const usable = Boolean(change?.apply_available && change?.expected_sha256);
  const protection = contentChangeProtection(change);
  $("content-dry-run").disabled = !usable;
  $("content-apply-check").checked = false;
  $("content-apply-check").disabled = !usable;
  $("content-legacy-ack").checked = false;
  $("content-legacy-ack").disabled = !usable || !protection.legacy;
  $("content-protected-ack").checked = false;
  $("content-protected-ack").disabled = !usable || !protection.protected;
  $("content-apply-confirmation").value = "";
  $("content-apply-confirmation").disabled = !usable;
  updateContentApplyButton();
}

function renderContentPlan(payload, draft) {
  state.content.plan = { payload, draft: cloneJson(draft) };
  state.content.selectedChangeId = null;
  const summary = clear($("content-plan-summary"));
  summary.className = "";
  summary.append(
    node("p", { text: `Plan: ${payload.plan_id || "unavailable"} | ${payload.change_count ?? 0} named specialist change(s) | ${payload.state || "unknown"}` }),
    node("p", { class: payload.state === "ready_for_review" ? "good-text" : "warning", text: payload.state === "ready_for_review" ? "Every listed apply is independent. Re-plan after each non-dry change." : "This pack is blocked. Resolve the returned structural/entrypoint/AI evidence before apply." })
  );
  if (payload.errors?.length) summary.append(rawPanel(payload.errors));
  const list = clear($("content-plan-list"));
  const select = clear($("content-change-select"));
  const changes = payload.changes || [];
  if (!changes.length) {
    list.append(node("div", { class: "empty", text: "This pack has no source or direct balance changes. Its narrative and review surfaces can still be saved and previewed." }));
    select.disabled = true;
    select.append(node("option", { value: "", text: "No source change" }));
    selectContentChange(null);
    return;
  }
  select.disabled = false;
  select.append(node("option", { value: "", text: "Select a named change" }));
  changes.forEach((change) => {
    select.append(node("option", { value: change.change_id, text: `${change.sequence}. ${change.slice} | ${change.target || change.entity_id || change.change_id}` }));
    const button = node("button", { class: "content-change-row", type: "button", "data-change-id": change.change_id });
    button.append(
      node("span", { class: "change-sequence", text: String(change.sequence || "?") }),
      node("span", {}, [
        node("strong", { text: `${change.slice || "slice"} | ${change.action || change.record_id || "record"}` }),
        node("span", { class: "change-meta", text: `${change.backend || "specialist"} | ${change.target || change.entity_id || "?"} | ${change.state || "unknown"}` }),
      ])
    );
    button.addEventListener("click", () => selectContentChange(change.change_id));
    list.append(button);
  });
  const first = changes.find((change) => change.apply_available) || changes[0];
  selectContentChange(first.change_id);
}

async function planContentDraft() {
  try {
    const draft = currentContentDraft();
    const payload = await request("/api/content/plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack: draft, trace_limit: 12 }) });
    renderContentPlan(payload, draft);
    renderContentAction(payload, "Content plan");
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function staticContentPresentationCanvas(payload) {
  const canvas = payload.canvas || {};
  const box = node("div", { class: "canvas content-static-canvas", "aria-label": "Static Content Forge presentation canvas" });
  for (const overlay of canvas.overlays || []) {
    const rect = overlay.canvas_box;
    if (!rect || !canvas.width || !canvas.height) continue;
    const overlayNode = node("span", { class: `canvas-overlay ${overlay.kind || "unknown"}`, text: short(`${overlay.identifier}${overlay.content ? ` | ${overlay.content}` : ""}`, 55) });
    overlayNode.style.left = `${(rect.x / canvas.width) * 100}%`;
    overlayNode.style.top = `${(rect.y / canvas.height) * 100}%`;
    overlayNode.style.width = `${Math.max((rect.width / canvas.width) * 100, 2)}%`;
    overlayNode.style.height = `${Math.max((rect.height / canvas.height) * 100, 2)}%`;
    overlayNode.title = `${overlay.identifier || "overlay"}\n${overlay.content || overlay.kind || ""}`;
    box.append(overlayNode);
  }
  return box;
}

function contentPreviewSection(title, content) {
  const section = node("section", { class: "content-preview-section" });
  section.append(node("h4", { text: title }));
  if (content) section.append(content);
  return section;
}

function renderContentPreview(payload) {
  state.content.preview = payload;
  const target = clear($("content-preview-result"));
  target.className = "content-preview-grid";
  const narrative = payload.narrative_preview || {};
  const beats = narrative.dialogue_beats || [];
  const beatList = node("div", { class: "content-beat-list" });
  if (!beats.length) beatList.append(node("p", { class: "empty", text: "No declared dialogue beats in this draft." }));
  beats.forEach((beat) => beatList.append(node("article", { class: "content-beat" }, [
    node("strong", { text: beat.title || beat.id || "Dialogue beat" }),
    node("span", { text: beat.purpose || beat.description || "No player-facing purpose declared." }),
    node("span", { class: "muted", text: beat.entrypoint || "No entrypoint linked yet" }),
  ])));
  target.append(contentPreviewSection("Dialogue the player can encounter", beatList));
  const timeline = narrative.quest_event_timeline || [];
  const timelineList = node("ol", { class: "content-timeline" });
  if (!timeline.length) timelineList.append(node("li", { class: "empty", text: "No quest/event timeline is declared." }));
  timeline.forEach((step) => timelineList.append(node("li", {}, [
    node("strong", { text: `${step.phase ? `${step.phase}: ` : ""}${step.title || step.id || "Event step"}` }),
    node("span", { text: step.description || "No player-facing event description." }),
  ])));
  target.append(contentPreviewSection("Quest / event progression", timelineList));
  const ai = payload.campaign_ai_preview || {};
  const contracts = ai.contracts || [];
  const contractList = node("div", { class: "content-contract-list" });
  if (!contracts.length) contractList.append(node("p", { class: "empty", text: "No campaign AI contract is declared." }));
  contracts.forEach((contract) => contractList.append(node("article", { class: "content-contract" }, [
    node("strong", { text: `${contract.intent || "AI intent"} | ${contract.id || "contract"}` }),
    node("span", { class: contract.state === "passed" ? "good-text" : "warning", text: `${contract.state || "unproven"} | ${contract.entrypoint || "no entrypoint"}` }),
    node("span", { text: `${(contract.required_markers || []).filter((marker) => marker.found).length}/${(contract.required_markers || []).length} required markers found` }),
  ])));
  target.append(contentPreviewSection("Campaign behavior the player should feel", contractList));
  const presentation = payload.presentation_preview || {};
  const screenList = node("div", { class: "content-screen-list" });
  if (!presentation.canvases?.length && !presentation.planned_new_presentations?.length) screenList.append(node("p", { class: "empty", text: "No presentation screen is declared." }));
  (presentation.canvases || []).forEach((item) => {
    const canvasPayload = item.canvas || {};
    const title = canvasPayload.presentation?.presentation_id || item.entrypoint || "Presentation";
    const article = node("article", { class: "content-screen" });
    article.append(node("strong", { text: title }), node("span", { text: item.entrypoint || "" }), staticContentPresentationCanvas(canvasPayload));
    screenList.append(article);
  });
  (presentation.planned_new_presentations || []).forEach((item) => screenList.append(node("article", { class: "content-screen" }, [
    node("strong", { text: item.id || "New presentation" }),
    node("span", { text: `${item.canvas_state || "planned"} | anchor ${item.anchor || "?"}` }),
    node("span", { text: item.description || "No description." }),
  ])));
  target.append(contentPreviewSection("Player-facing presentation screens", screenList));
  const balance = payload.troop_item_preview || [];
  const balanceList = node("div", { class: "content-contract-list" });
  if (!balance.length) balanceList.append(node("p", { class: "empty", text: "No troop/item record change is declared." }));
  balance.forEach((item) => balanceList.append(node("article", { class: "content-contract" }, [
    node("strong", { text: item.entity_id || item.record_id || "Balance record" }),
    node("span", { class: item.state === "ready_for_review" ? "good-text" : "warning", text: item.state || "unplanned" }),
    node("span", { text: item.rationale || "No player-facing rationale." }),
  ])));
  target.append(contentPreviewSection("Troop / item intent", balanceList));
}

function renderContentReview(payload) {
  state.content.review = payload;
  const target = clear($("content-review-result"));
  const canvas = payload.review_canvas || {};
  const flow = node("div", { class: "content-flow" });
  const nodeNames = new Map();
  (canvas.nodes || []).forEach((item) => {
    nodeNames.set(item.id, item.title || item.id);
    const itemNode = node("article", { class: "content-flow-node", "data-kind": item.kind || "unknown", "data-status": item.status || "unknown" });
    itemNode.append(
      node("strong", { text: item.title || item.id }),
      node("span", { text: `${item.kind || "node"} | ${item.status || "declared"}` }),
      node("span", { text: short(typeof item.detail === "string" ? item.detail : json(item.detail || {}), 220) })
    );
    flow.append(itemNode);
  });
  if (!(canvas.nodes || []).length) flow.append(node("p", { class: "empty", text: "No review-canvas nodes were returned." }));
  target.append(flow);
  const edges = canvas.edges || [];
  if (edges.length) {
    const edgeList = node("div", { class: "content-flow" });
    edges.forEach((edge) => edgeList.append(node("div", { class: "content-flow-edge", text: `${nodeNames.get(edge.from) || edge.from} -> ${nodeNames.get(edge.to) || edge.to} | ${edge.kind || "links"}` })));
    appendDetailSection(target, "Typed relationships", edgeList);
  }
  const acceptance = canvas.acceptance_review || [];
  if (acceptance.length) appendDetailSection(target, "Acceptance review", node("ul", { class: "detail-list" }, acceptance.map((item) => node("li", { text: `${item.state || "review"}: ${item.criterion}` }))));
  if (canvas.mermaid) {
    const details = node("details", { class: "panel" });
    details.append(node("summary", { text: "Mermaid source for this review canvas" }), node("pre", { text: canvas.mermaid }));
    target.append(details);
  }
}

async function previewContentDraft() {
  try {
    const draft = currentContentDraft();
    const payload = await request("/api/content/preview", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack: draft, trace_limit: 12 }) });
    renderContentPreview(payload);
    renderContentReview(payload);
    renderContentAction(payload, "Content preview");
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function reviewContentDraft() {
  try {
    const draft = currentContentDraft();
    const payload = await request("/api/content/review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack: draft, trace_limit: 12 }) });
    renderContentReview(payload);
    renderContentAction(payload, "Content dependency review");
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function verifyContentDraft() {
  try {
    const draft = currentContentDraft();
    const payload = await request("/api/content/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pack: draft,
        run_scenarios: $("content-verify-scenarios").checked,
        run_tests: $("content-verify-tests").checked,
        stage_build_check: false,
        scenario_iterations: 8,
        scenario_seed: 1,
        timeout_seconds: 90,
      }),
    });
    renderContentAction(payload, "Content verification");
  } catch (error) {
    const result = clear($("content-action-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function runContentApply(dryRun) {
  const plan = state.content.plan;
  const change = selectedContentChange();
  if (!plan || !change) return;
  const result = clear($("content-apply-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the selected independent Content Forge change..." : "Applying one reviewed specialist source/record change...";
  try {
    const protection = contentChangeProtection(change);
    const body = {
      pack: plan.draft,
      change_id: change.change_id,
      expected_content_plan_id: plan.payload.plan_id,
      expected_sha256: change.expected_sha256,
      dry_run: dryRun,
    };
    if (change.expected_balance_plan_sha256) body.expected_balance_plan_sha256 = change.expected_balance_plan_sha256;
    if (!dryRun) {
      if (protection.legacy && !$("content-legacy-ack").checked) throw new Error("This direct legacy balance record needs its explicit acknowledgement.");
      if (protection.protected && !$("content-protected-ack").checked) throw new Error("This protected legacy balance record needs its extra acknowledgement.");
      body.confirmation = "APPLY SOURCE";
      body.allow_legacy_compile_authoring = protection.legacy && $("content-legacy-ack").checked;
      body.allow_protected_legacy_record_change = protection.protected && $("content-protected-ack").checked;
    }
    const payload = await request("/api/content/apply", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      clearContentPlan();
      const action = clear($("content-action-result"));
      action.className = "result-message good";
      action.textContent = "One named content change applied through its specialist SHA gate. Re-plan the pack, verify it, then use the ordinary reviewed build and in-game smoke path.";
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function updateContentCatalogApplyButton() {
  const ready = Boolean(state.content.catalogPlan)
    && $("content-catalog-apply-check").checked
    && $("content-catalog-confirmation").value === "SAVE CONTENT PACK";
  $("content-catalog-apply").disabled = !ready;
}

function contentCatalogMode(draft) {
  return state.content.catalogPackIds.has(draft.id) ? "replace" : "create";
}

function renderContentCatalogPlan(payload, draft, mode) {
  state.content.catalogPlan = { payload, draft: cloneJson(draft), mode };
  const summary = clear($("content-catalog-summary"));
  summary.className = "";
  summary.append(
    node("p", { text: `${payload.operation || mode} pack ${payload.pack?.id || draft.id} in ${payload.catalog_target?.path || "packs.json"}` }),
    node("p", { class: "muted", text: `Catalog SHA-256: ${payload.catalog_target?.base_sha256 || "unavailable"}` })
  );
  $("content-catalog-diff").textContent = payload.unified_diff || "No catalog diff was returned.";
  $("content-catalog-dry-run").disabled = false;
  $("content-catalog-apply-check").disabled = false;
  $("content-catalog-confirmation").disabled = false;
  updateContentCatalogApplyButton();
}

async function planContentCatalogSave() {
  try {
    const draft = currentContentDraft();
    const mode = contentCatalogMode(draft);
    const payload = await request("/api/content/catalog-plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack: draft, mode }) });
    renderContentCatalogPlan(payload, draft, mode);
    const action = clear($("content-action-result"));
    action.className = "result-message good";
    action.textContent = "Catalog save plan is ready. It affects only the strict Content Forge pack contract, never module source or exports.";
  } catch (error) {
    const result = clear($("content-catalog-result"));
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function runContentCatalogApply(dryRun) {
  const catalogPlan = state.content.catalogPlan;
  if (!catalogPlan) return;
  const result = clear($("content-catalog-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the exact catalog SHA and strict pack contract..." : "Saving the reviewed strict Content Forge pack contract...";
  try {
    const body = {
      pack: catalogPlan.draft,
      mode: catalogPlan.mode,
      expected_catalog_plan_id: catalogPlan.payload.catalog_plan_id,
      expected_catalog_sha256: catalogPlan.payload.catalog_target.base_sha256,
      dry_run: dryRun,
    };
    if (!dryRun) body.confirmation = "SAVE CONTENT PACK";
    const payload = await request("/api/content/catalog-apply", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      state.content.selectedPackId = catalogPlan.draft.id;
      clearContentCatalogPlan();
      await loadContentSummary();
      await loadContentPack(catalogPlan.draft.id);
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function textLint(event) {
  event.preventDefault();
  const results = clear($("text-results"));
  results.append(node("div", { class: "empty", text: "Reading bounded generated/source text evidence…" }));
  try {
    const params = new URLSearchParams({ severity: $("text-severity").value, limit: "80" });
    const query = $("text-query").value.trim();
    if (query) params.set("query", query);
    const payload = await request(`/api/workbench/text-lint?${params}`);
    clear(results);
    const summary = node("p", { class: "muted", text: `${payload.returned_finding_count}/${payload.finding_count} findings · ${payload.summary?.text_sink_count ?? "?"} text sinks` });
    results.append(summary);
    if (!payload.findings?.length) results.append(node("p", { class: "good-text", text: "No findings at this severity/filter." }));
    else for (const finding of payload.findings) {
      const item = node("article", { class: "panel" });
      const severity = String(finding.severity || "unknown").toLowerCase();
      item.append(node("h3", { class: severity === "error" ? "danger-text" : severity === "warning" ? "warning" : "", text: `${finding.code || "TEXT FINDING"} · ${finding.severity || "unknown"}` }), node("p", { text: finding.message || short(json(finding)) }));
      item.append(rawPanel(finding));
      results.append(item);
    }
  } catch (error) { clear(results).append(apiError(error.message)); }
}

function orderRecordTarget(record) {
  return record.fragment_id || record.entity_id || record.source_fragment_id || record.route_id || record.symbol || "";
}

function orderRecordTitle(record) {
  return record.path || record.name || record.symbol || record.source_path || record.entity_id || record.fragment_id || "Order evidence";
}

function orderRecordMeta(record) {
  if (record.source_order) return `${record.area || "?"} Â· source position ${record.source_order.position ?? "?"}`;
  if (record.source) return `${record.area || "?"} Â· ${sourceLabel(record.source)} Â· position ${record.position ?? "?"}`;
  if (record.table) return `${record.table} Â· generated ID ${record.value ?? "?"}`;
  if (record.compile_path) return `${record.compile_path}:L${record.compile_line_start ?? "?"}`;
  return short(json(record), 120);
}

function orderCard(record) {
  const target = orderRecordTarget(record);
  const button = node("button", { class: "result-card", type: "button" });
  button.append(
    node("span", { class: "result-title", text: orderRecordTitle(record) }),
    node("span", { class: "result-meta", text: orderRecordMeta(record) }),
    node("span", { class: "result-snippet", text: target || "Static evidence with no direct target" })
  );
  if (target) button.addEventListener("click", () => inspectOrder(target));
  else button.disabled = true;
  return button;
}

async function orderSearch(event) {
  event.preventDefault();
  const query = $("order-query").value.trim();
  const area = $("order-area").value;
  const domain = $("order-domain").value;
  const results = clear($("order-results"));
  $("order-count").textContent = "";
  if (!query && area === "all" && domain === "all") {
    results.append(apiError("Enter a search term, choose an area, or select one order domain to keep this map bounded."));
    return;
  }
  results.append(node("div", { class: "empty", text: "Mapping bounded order evidenceâ€¦" }));
  try {
    const params = new URLSearchParams({ area, domain, limit: "80" });
    if (query) params.set("query", query);
    const payload = await request(`/api/order/map?${params}`);
    const records = (payload.groups || []).flatMap((group) => group.records || []);
    clear(results);
    $("order-count").textContent = `${payload.returned_count ?? records.length}/${payload.match_count ?? records.length}`;
    if (!records.length) results.append(node("div", { class: "empty", text: "No order evidence matched that bounded query." }));
    else records.forEach((record) => results.append(orderCard(record)));
  } catch (error) { clear(results).append(apiError(error.message)); }
}

async function inspectOrder(target) {
  const detail = clear($("order-detail"));
  detail.append(node("div", { class: "empty", text: "Loading order provenance and protected contractsâ€¦" }));
  try {
    const payload = await request(`/api/order/explain?${new URLSearchParams({ target, related_limit: "30" })}`);
    clear(detail);
    const fragment = payload.fragment || {};
    const route = payload.route || {};
    const entity = payload.entity || {};
    const title = fragment.path || route.route_id || entity.name || payload.id_entry?.symbol || target;
    const header = node("div");
    header.append(node("h3", { text: title }), node("p", { class: "muted", text: `${payload.target_kind || "order target"} Â· ${target}` }));
    const movable = (payload.safe_moves || []).length > 0;
    if (movable) {
      const move = node("button", { text: "Use as anchored move target" });
      move.addEventListener("click", () => {
        $("order-move-target").value = target;
        $("order-move-target").focus();
      });
      header.append(move);
    }
    detail.append(header);
    appendDetailSection(detail, "Supported safe move paths", movable ? chipList(payload.safe_moves) : node("p", { class: "muted", text: "No automatic move path for this target type." }));
    appendDetailSection(detail, "Protected order contracts", (payload.contracts || []).length ? rawPanel(payload.contracts) : node("p", { class: "good-text", text: "No target-specific protected contract was returned." }));
    appendDetailSection(detail, "Order evidence", rawPanel(payload));
  } catch (error) { clear(detail).append(apiError(error.message)); }
}

function clearOrderPlan() {
  state.orderPlan = null;
  $("order-plan-summary").className = "empty";
  $("order-plan-summary").textContent = "Generate an anchored move plan to inspect its diff and risk.";
  $("order-plan-diff").textContent = "";
  $("order-dry-run").disabled = true;
  $("order-apply-check").checked = false;
  $("order-apply-check").disabled = true;
  $("order-apply-confirmation").value = "";
  $("order-apply-confirmation").disabled = true;
  $("order-apply-source").disabled = true;
  clear($("order-apply-result"));
}

function updateOrderApplyButton() {
  const ready = Boolean(state.orderPlan?.sha) && $("order-apply-check").checked && $("order-apply-confirmation").value === "APPLY SOURCE";
  $("order-apply-source").disabled = !ready;
}

async function planOrderMove(event) {
  event.preventDefault();
  clearOrderPlan();
  const requestPayload = {
    target: $("order-move-target").value.trim(),
    anchor: $("order-move-anchor").value.trim(),
    position: $("order-move-position").value,
  };
  if (!requestPayload.target || !requestPayload.anchor) {
    $("order-plan-summary").className = "result-message error";
    $("order-plan-summary").textContent = "Target and anchor IDs are both required.";
    return;
  }
  try {
    const payload = await request("/api/order/plan-move", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(requestPayload) });
    const plan = payload.order_manifest_plan || payload.change_router_plan || {};
    const sha = plan.base_sha256 || plan.target?.base_sha256;
    state.orderPlan = { request: requestPayload, sha, plan, payload };
    const summary = clear($("order-plan-summary"));
    summary.className = "";
    summary.append(
      node("p", { text: `Move type: ${payload.plan_kind || "?"}` }),
      node("p", { class: "muted", text: `Base SHA-256: ${sha || "unavailable"}` }),
      node("p", { class: payload.risk?.level === "critical" || payload.risk?.level === "high" ? "warning" : "muted", text: `Risk: ${payload.risk?.level || "unknown"} Â· ${(payload.risk?.reasons || []).join(" ")}` })
    );
    $("order-plan-diff").textContent = plan.unified_diff || "No unified diff was returned.";
    $("order-dry-run").disabled = !sha;
    $("order-apply-check").disabled = !sha;
    $("order-apply-confirmation").disabled = !sha;
    updateOrderApplyButton();
  } catch (error) {
    $("order-plan-summary").className = "result-message error";
    $("order-plan-summary").textContent = error.message;
  }
}

async function runOrderApply(dryRun) {
  if (!state.orderPlan) return;
  const result = clear($("order-apply-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the current SHA-guarded order moveâ€¦" : "Applying one reviewed order source changeâ€¦";
  try {
    const body = { ...state.orderPlan.request, expected_sha256: state.orderPlan.sha, dry_run: dryRun };
    if (!dryRun) body.confirmation = "APPLY SOURCE";
    if (!dryRun && $("order-allow-protected").checked) body.allow_protected_contract_change = true;
    const payload = await request("/api/order/apply-move", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      $("order-apply-source").disabled = true;
      $("order-apply-check").disabled = true;
      $("order-apply-confirmation").disabled = true;
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

async function runWorkbench(kind) {
  const container = clear($("workbench-result"));
  container.append(node("div", { class: "empty", text: "Collecting fixed Workbench evidence…" }));
  try {
    let path;
    if (kind === "impact") {
      const target = $("impact-target").value.trim();
      if (!target) throw new Error("Enter an impact target first.");
      path = `/api/workbench/impact?${new URLSearchParams({ target, limit: "16" })}`;
    } else if (kind === "order") path = "/api/workbench/order-report";
    else if (kind === "readiness") path = "/api/workbench/release-readiness";
    else path = "/api/workbench/summary";
    const payload = await request(path);
    clear(container).append(rawPanel(payload));
  } catch (error) { clear(container).append(apiError(error.message)); }
}

async function loadBalanceSummary() {
  const cards = clear($("balance-cards"));
  try {
    const payload = await request("/api/balance/summary");
    const items = payload.items || {};
    const troops = payload.troops || {};
    const authoring = payload.authoring || {};
    cards.append(
      metric("Items", items.count ?? "?", `${items.merchandise_count ?? "?"} shop-available`),
      metric("Troops", troops.count ?? "?", `${troops.hero_count ?? "?"} heroes`),
      metric("Upgrade edges", troops.upgrade_edge_count ?? "?", `${troops.derived_upgrade_variant_count ?? "?"} derived variants`),
      metric("ID parity", items.id_contract?.passed && troops.id_contract?.passed ? "pass" : "review", authoring.confirmed ? "legacy authoring route confirmed" : "build route needs review")
    );
    if (!authoring.confirmed) cards.append(apiError("The current build route did not confirm legacy troop/item authoring. Balance plans may be viewed, but non-dry apply is blocked."));
  } catch (error) {
    cards.append(apiError(error.message));
  }
}

function balanceCard(row, mode) {
  const button = node("button", { class: "result-card", type: "button" });
  if (mode === "items") {
    button.append(
      node("span", { class: "result-title", text: row.item_id || row.entity_id }),
      node("span", { class: "result-meta", text: `${row.type || "?"} · price ${row.price ?? "?"} · score ${row.combat_score ?? "?"}` }),
      node("span", { class: "result-snippet", text: `${row.name || ""} · ${row.troop_use_count ?? 0} regular troop users · ${sourceLabel(row.source)}` })
    );
    button.addEventListener("click", () => inspectBalanceItem(row.item_id || row.entity_id));
  } else if (mode === "troops") {
    button.append(
      node("span", { class: "result-title", text: row.troop_id || row.entity_id }),
      node("span", { class: "result-meta", text: `${row.faction || "?"} · ${row.role || "?"} · level ${row.level ?? "?"}` }),
      node("span", { class: "result-snippet", text: `${row.name || ""} · kit ${row.kit_score ?? "?"} · ${row.kit_status || "?"} · ${sourceLabel(row.source)}` })
    );
    button.addEventListener("click", () => inspectBalanceTroop(row.troop_id || row.entity_id));
  } else {
    const evidence = row.evidence || {};
    button.append(
      node("span", { class: "result-title", text: `${row.severity || "?"} · ${row.code || "?"}` }),
      node("span", { class: "result-meta", text: row.entity_id || "no exact entity" }),
      node("span", { class: "result-snippet", text: row.message || "Static balance review candidate." })
    );
    if (String(row.entity_id || "").startsWith("item:")) button.addEventListener("click", () => inspectBalanceItem(row.entity_id));
    else if (String(row.entity_id || "").startsWith("troop:")) button.addEventListener("click", () => inspectBalanceTroop(row.entity_id));
    else button.addEventListener("click", () => { clear($("balance-detail")).append(rawPanel({ finding: row, evidence })); });
  }
  return button;
}

async function balanceSearch(event) {
  event.preventDefault();
  const mode = $("balance-mode").value;
  const query = $("balance-query").value.trim();
  const results = clear($("balance-results"));
  const detail = clear($("balance-detail"));
  $("balance-count").textContent = "";
  results.append(node("div", { class: "empty", text: "Collecting bounded balance evidence…" }));
  detail.append(node("div", { class: "empty", text: "Choose an exact item, troop, or outlier to inspect evidence." }));
  try {
    let payload;
    if (mode === "items") {
      const params = new URLSearchParams({ limit: "60" });
      if (query) params.set("query", query);
      payload = await request(`/api/balance/items?${params}`);
      clear(results);
      $("balance-count").textContent = `${payload.returned_count}/${payload.match_count}`;
      if (!payload.items?.length) results.append(node("div", { class: "empty", text: "No matching evaluated items." }));
      else payload.items.forEach((row) => results.append(balanceCard(row, "items")));
    } else if (mode === "troops") {
      const params = new URLSearchParams({ limit: "60", include_heroes: $("balance-include-heroes").checked ? "true" : "false" });
      if (query) params.set("query", query);
      payload = await request(`/api/balance/troops?${params}`);
      clear(results);
      $("balance-count").textContent = `${payload.returned_count}/${payload.match_count}`;
      if (!payload.troops?.length) results.append(node("div", { class: "empty", text: "No matching evaluated troops." }));
      else payload.troops.forEach((row) => results.append(balanceCard(row, "troops")));
    } else {
      const domain = ["all", "items", "troops"].includes(query.toLowerCase()) ? query.toLowerCase() : "all";
      const params = new URLSearchParams({ domain, include_heroes: $("balance-include-heroes").checked ? "true" : "false", limit: "80" });
      payload = await request(`/api/balance/outliers?${params}`);
      clear(results);
      $("balance-count").textContent = `${payload.returned_count}/${payload.finding_count}`;
      if (!payload.findings?.length) results.append(node("div", { class: "empty", text: "No static outliers under the selected model." }));
      else payload.findings.forEach((row) => results.append(balanceCard(row, "outliers")));
    }
  } catch (error) {
    clear(results).append(apiError(error.message));
  }
}

async function inspectBalanceItem(itemId) {
  const detail = clear($("balance-detail"));
  detail.append(node("div", { class: "empty", text: "Decoding evaluated item stats and users…" }));
  try {
    const payload = await request(`/api/balance/item?${new URLSearchParams({ item_id: itemId, troop_limit: "40" })}`);
    clear(detail);
    const item = payload.item || {};
    const header = node("div");
    header.append(node("h3", { text: `${item.item_id || itemId} · ${item.name || ""}` }), node("p", { class: "muted", text: `${item.type || "?"} · price ${item.price ?? "?"} · score ${item.combat_score ?? "?"} · ${sourceLabel(item.source)}` }));
    const edit = node("button", { text: "Use in Balance editor" });
    edit.addEventListener("click", () => {
      $("balance-edit-kind").value = "item";
      $("balance-edit-id").value = item.item_id || itemId;
      $("balance-changes").focus();
    });
    header.append(edit);
    detail.append(header);
    appendDetailSection(detail, "Decoded balance stats", rawPanel(item.stats));
    appendDetailSection(detail, "Editable direct stat constructors", chipList(item.editable_stat_calls || []));
    appendDetailSection(detail, `Troop inventory users (${payload.troop_user_count ?? 0})`, rawPanel(payload.troop_users));
    appendDetailSection(detail, "Record provenance and flags", rawPanel({ source: item.source, flags: item.flags, capabilities_raw_bits: item.capabilities_raw_bits, modifier_bits_raw: item.modifier_bits_raw }));
  } catch (error) { clear(detail).append(apiError(error.message)); }
}

async function inspectBalanceTroop(troopId) {
  const detail = clear($("balance-detail"));
  detail.append(node("div", { class: "empty", text: "Reading evaluated troop, inventory pool, and direct upgrade evidence…" }));
  try {
    const [payload, tree] = await Promise.all([
      request(`/api/balance/troop?${new URLSearchParams({ troop_id: troopId, item_limit: "60" })}`),
      request(`/api/balance/upgrade-tree?${new URLSearchParams({ troop_id: troopId, depth: "2", limit: "80" })}`),
    ]);
    clear(detail);
    const troop = payload.troop || {};
    const header = node("div");
    header.append(node("h3", { text: `${troop.troop_id || troopId} · ${troop.name || ""}` }), node("p", { class: "muted", text: `${troop.faction || "?"} · ${troop.role || "?"} · level ${troop.level ?? "?"} · kit ${troop.kit_score ?? "?"} · ${sourceLabel(troop.source)}` }));
    const edit = node("button", { text: "Use in Balance editor" });
    edit.addEventListener("click", () => {
      $("balance-edit-kind").value = "troop";
      $("balance-edit-id").value = troop.troop_id || troopId;
      $("balance-changes").focus();
    });
    header.append(edit);
    detail.append(header);
    appendDetailSection(detail, "Attributes, proficiencies, and skills", rawPanel({ attributes: troop.attributes, proficiencies: troop.proficiencies, skills: troop.skills }));
    appendDetailSection(detail, "Static kit analysis", rawPanel(troop.kit_analysis));
    appendDetailSection(detail, `Random inventory pool (${payload.inventory_count ?? 0})`, rawPanel(payload.inventory));
    appendDetailSection(detail, "Direct upgrade neighborhood", rawPanel({ nodes: tree.nodes, edges: tree.edges, truncated: tree.truncated }));
    appendDetailSection(detail, "Record provenance and guarantees", rawPanel({ source: troop.source, flags: troop.flags, unknown_inventory_indices: payload.unknown_inventory_indices }));
  } catch (error) { clear(detail).append(apiError(error.message)); }
}

function clearBalancePlan() {
  state.balancePlan = null;
  $("balance-plan-summary").className = "empty";
  $("balance-plan-summary").textContent = "Generate a record-local plan to inspect its diff, source SHA, and plan SHA.";
  $("balance-plan-diff").textContent = "";
  ["balance-dry-run", "balance-apply-check", "balance-legacy-ack", "balance-protected-ack", "balance-apply-confirmation", "balance-apply-source"].forEach((id) => { $(id).disabled = true; });
  $("balance-apply-check").checked = false;
  $("balance-legacy-ack").checked = false;
  $("balance-protected-ack").checked = false;
  $("balance-apply-confirmation").value = "";
  clear($("balance-apply-result"));
}

function parseBalanceChanges() {
  const raw = $("balance-changes").value.trim();
  if (!raw) throw new Error("Bounded changes JSON is required.");
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("Changes must be a JSON object.");
    return parsed;
  } catch (error) { throw new Error(`Changes JSON is invalid: ${error.message}`); }
}

function balanceEditRequest() {
  const entity_kind = $("balance-edit-kind").value;
  const entity_id = $("balance-edit-id").value.trim();
  if (!entity_id) throw new Error("Item / troop ID is required.");
  return { entity_kind, entity_id, changes: parseBalanceChanges() };
}

function updateBalanceApplyButton() {
  const protectedRequired = Boolean(state.balancePlan?.protected);
  const ready = Boolean(state.balancePlan?.sourceSha && state.balancePlan?.planSha)
    && $("balance-apply-check").checked
    && $("balance-legacy-ack").checked
    && (!protectedRequired || $("balance-protected-ack").checked)
    && $("balance-apply-confirmation").value === "APPLY SOURCE";
  $("balance-apply-source").disabled = !ready;
}

function renderBalancePlan(payload, requestPayload) {
  const sourceSha = payload.target?.base_sha256;
  const planSha = payload.plan_sha256;
  const protectedRequired = Boolean(payload.apply_contract?.allow_protected_legacy_record_change_required_for_non_dry);
  state.balancePlan = { request: requestPayload, sourceSha, planSha, protected: protectedRequired, payload };
  const summary = clear($("balance-plan-summary"));
  summary.className = "";
  summary.append(
    node("p", { text: `Target: ${payload.target?.path || "?"}` }),
    node("p", { class: "muted", text: `Source SHA-256: ${sourceSha || "unavailable"}` }),
    node("p", { class: "muted", text: `Plan SHA-256: ${planSha || "unavailable"}` }),
    node("p", { class: protectedRequired ? "warning" : "muted", text: protectedRequired ? "Hardwired legacy record: protected acknowledgement is required for real apply." : (payload.warnings || []).join(" ") })
  );
  $("balance-plan-diff").textContent = payload.unified_diff || "No unified diff was returned.";
  const enabled = Boolean(sourceSha && planSha);
  $("balance-dry-run").disabled = !enabled;
  $("balance-apply-check").disabled = !enabled;
  $("balance-legacy-ack").disabled = !enabled;
  $("balance-protected-ack").disabled = !enabled || !protectedRequired;
  $("balance-apply-confirmation").disabled = !enabled;
  updateBalanceApplyButton();
}

async function planBalanceEdit(event) {
  event.preventDefault();
  clearBalancePlan();
  try {
    const payload = balanceEditRequest();
    const result = await request("/api/balance/patch", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    renderBalancePlan(result, payload);
  } catch (error) {
    $("balance-plan-summary").className = "result-message error";
    $("balance-plan-summary").textContent = error.message;
  }
}

async function runBalanceApply(dryRun) {
  if (!state.balancePlan) return;
  const result = clear($("balance-apply-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the current source and plan SHA contract…" : "Applying one reviewed legacy authoring record patch…";
  try {
    const body = {
      ...state.balancePlan.request,
      expected_sha256: state.balancePlan.sourceSha,
      expected_plan_sha256: state.balancePlan.planSha,
      dry_run: dryRun,
    };
    if (!dryRun) {
      if (!$("balance-legacy-ack").checked) throw new Error("A real balance apply requires the legacy compile-authoring acknowledgement.");
      if (state.balancePlan.protected && !$("balance-protected-ack").checked) throw new Error("A hardwired record requires the protected-record acknowledgement.");
      body.confirmation = "APPLY SOURCE";
      body.allow_legacy_compile_authoring = $("balance-legacy-ack").checked;
      if (state.balancePlan.protected) body.allow_protected_legacy_record_change = $("balance-protected-ack").checked;
    }
    const payload = await request("/api/balance/apply", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      $("balance-apply-source").disabled = true;
      $("balance-apply-check").disabled = true;
      $("balance-legacy-ack").disabled = true;
      $("balance-protected-ack").disabled = true;
      $("balance-apply-confirmation").disabled = true;
      await loadBalanceSummary();
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function editorFields() {
  const action = $("edit-action").value.trim();
  const value = $("edit-value").value;
  const output = {};
  const optional = [
    ["field", "edit-field"], ["block", "edit-block"], ["operation", "edit-operation"],
    ["alignment", "edit-alignment"], ["trigger", "edit-trigger"], ["anchor_route_id", "edit-anchor-route"],
  ];
  for (const [key, id] of optional) if ($(id).value.trim()) output[key] = $(id).value.trim();
  if (value !== "" || /^(set_text|replace_text|set_mesh|set_color|set_alpha|set_expression|replace_operations|replace_trigger_operations)$/.test(action)) output.value = value;
  if ($("edit-operation-index").value !== "") output.operation_index = Number($("edit-operation-index").value);
  if ($("edit-x").value !== "") output.x = Number($("edit-x").value);
  if ($("edit-y").value !== "") output.y = Number($("edit-y").value);
  return output;
}

function parseNewItem() {
  const raw = $("edit-new-item").value.trim();
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("The value must be an object.");
    return parsed;
  } catch (error) { throw new Error(`New-item JSON is invalid: ${error.message}`); }
}

function editorPayload() {
  const domain = state.editor;
  const target = $("edit-target").value.trim();
  const action = $("edit-action").value.trim();
  if (!target || !action) throw new Error("Target ID and semantic action are required.");
  const values = editorFields();
  const newItem = parseNewItem();
  if (domain === "atlas") {
    const payload = { entity_id: target, action };
    ["field", "block", "value", "operation", "position", "operation_index"].forEach((key) => { if (key in values) payload[key] = values[key]; });
    payload.position = $("edit-position").value;
    if (newItem) payload.new_item = newItem;
    if ($("edit-allow-referenced-removal").checked) {
      payload.allow_referenced_removal = true;
      payload.removal_acknowledgement = $("edit-removal-ack").value;
    }
    return payload;
  }
  if (domain === "dialogue") {
    const payload = { route_id: target, action, position: $("edit-position").value };
    ["value", "operation", "operation_index", "anchor_route_id"].forEach((key) => { if (key in values) payload[key] = values[key]; });
    if (newItem) payload.new_route = newItem;
    return payload;
  }
  const payload = { target, action };
  ["x", "y", "value", "alignment", "trigger"].forEach((key) => { if (key in values) payload[key] = values[key]; });
  if (newItem) {
    if (action === "add_overlay") payload.new_overlay = newItem;
    else if (action === "add_trigger") payload.new_trigger = newItem;
    else throw new Error("New JSON is only accepted for add_overlay or add_trigger presentation actions.");
  }
  return payload;
}

function clearPlan() {
  state.plan = null;
  $("plan-summary").className = "empty";
  $("plan-summary").textContent = "Generate a plan to see the unified diff and its apply contract.";
  $("plan-diff").textContent = "";
  $("dry-run").disabled = true;
  $("apply-check").checked = false;
  $("apply-check").disabled = true;
  $("apply-confirmation").value = "";
  $("apply-confirmation").disabled = true;
  $("apply-source").disabled = true;
  clear($("apply-result"));
}

function renderPlan(payload, requestPayload) {
  const plan = payload.change_router_plan || {};
  state.plan = { domain: state.editor, request: requestPayload, sha: plan.target?.base_sha256, plan };
  const summary = clear($("plan-summary"));
  summary.className = "";
  summary.append(
    node("p", { text: `Target: ${plan.target?.path || "?"}` }),
    node("p", { class: "muted", text: `Base SHA-256: ${plan.target?.base_sha256 || "unavailable"}` }),
    node("p", { class: "muted", text: (payload.warnings || []).join(" ") })
  );
  $("plan-diff").textContent = plan.unified_diff || "No unified diff was returned.";
  $("dry-run").disabled = !state.plan.sha;
  $("apply-check").disabled = !state.plan.sha;
  $("apply-confirmation").disabled = !state.plan.sha;
  updateApplyButton();
}

async function planSemanticEdit(event) {
  event.preventDefault();
  clearPlan();
  try {
    const payload = editorPayload();
    const result = await request(`/api/${state.editor}/patch`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    renderPlan(result, payload);
  } catch (error) {
    $("plan-summary").className = "result-message error";
    $("plan-summary").textContent = error.message;
  }
}

function updateApplyButton() {
  const ready = Boolean(state.plan?.sha) && $("apply-check").checked && $("apply-confirmation").value === "APPLY SOURCE";
  $("apply-source").disabled = !ready;
}

async function runApply(dryRun) {
  if (!state.plan) return;
  const result = clear($("apply-result"));
  result.className = "result-message";
  result.textContent = dryRun ? "Rehearsing the current SHA-guarded source change…" : "Applying source only through the current SHA guard…";
  try {
    const body = { ...state.plan.request, expected_sha256: state.plan.sha, dry_run: dryRun };
    if (!dryRun) body.confirmation = "APPLY SOURCE";
    const payload = await request(`/api/${state.plan.domain}/apply`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    result.className = "result-message good";
    result.textContent = json(payload);
    if (!dryRun) {
      $("apply-source").disabled = true;
      $("apply-check").disabled = true;
      $("apply-confirmation").disabled = true;
    }
  } catch (error) {
    result.className = "result-message error";
    result.textContent = error.message;
  }
}

function setEditor(domain, target, actions = []) {
  state.editor = domain;
  document.querySelectorAll(".editor-tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.editor === domain));
  $("edit-target").value = target || "";
  const usable = (actions || []).find((action) => !String(action).startsWith("delegate_"));
  $("edit-action").value = usable || "";
  clearPlan();
  showView("editor");
  $("edit-target").focus();
}

function reportPresentationPlanError(error) {
  $("presentation-plan-summary").className = "result-message error";
  $("presentation-plan-summary").textContent = error?.message || String(error);
}

function wireEvents() {
  document.querySelectorAll(".nav-item").forEach((item) => item.addEventListener("click", () => {
    showView(item.dataset.view);
    if (item.dataset.view === "balance") loadBalanceSummary();
    if (item.dataset.view === "content" && !state.content.packs.length) loadContentSummary();
  }));
  $("refresh-summary").addEventListener("click", loadOverview);
  $("atlas-search").addEventListener("submit", atlasSearch);
  $("dialogue-search").addEventListener("submit", dialogueSearch);
  $("presentation-search").addEventListener("submit", presentationSearch);
  $("presentation-browse").addEventListener("click", () => browsePresentations().catch(reportPresentationPlanError));
  $("presentation-refresh-canvas").addEventListener("click", () => {
    if (state.presentation.presentationKey) inspectPresentation(state.presentation.presentationKey);
  });
  $("presentation-reset-draft").addEventListener("click", resetSelectedPresentationDraft);
  $("presentation-overlay-filter").addEventListener("input", (event) => {
    state.presentation.overlayFilter = event.target.value;
    if (state.presentation.canvasPayload) renderPresentationOverlayList(state.presentation.canvasPayload);
  });
  $("presentation-position-x").addEventListener("input", syncPresentationDraftFromInputs);
  $("presentation-position-y").addEventListener("input", syncPresentationDraftFromInputs);
  $("presentation-position-x").addEventListener("change", refreshSelectedPresentationInspector);
  $("presentation-position-y").addEventListener("change", refreshSelectedPresentationInspector);
  $("presentation-layout-form").addEventListener("submit", (event) => { planPresentationMove(event).catch(reportPresentationPlanError); });
  $("presentation-plan-resize").addEventListener("click", () => { planPresentationResize().catch(reportPresentationPlanError); });
  $("presentation-plan-content").addEventListener("click", () => { planPresentationContent().catch(reportPresentationPlanError); });
  $("presentation-plan-color").addEventListener("click", () => { planPresentationColor().catch(reportPresentationPlanError); });
  $("presentation-plan-alpha").addEventListener("click", () => { planPresentationAlpha().catch(reportPresentationPlanError); });
  $("presentation-plan-remove").addEventListener("click", () => {
    const overlay = selectedPresentationOverlay();
    if (!overlay) return;
    planPresentationAction("remove_overlay", overlay.overlay_id).catch(reportPresentationPlanError);
  });
  document.querySelectorAll(".presentation-align").forEach((button) => button.addEventListener("click", () => {
    const overlay = selectedPresentationOverlay();
    if (!overlay) return;
    planPresentationAction("align_overlay", overlay.overlay_id, { alignment: button.dataset.alignment }).catch(reportPresentationPlanError);
  }));
  $("presentation-create-form").addEventListener("submit", (event) => { planPresentationCreate(event).catch(reportPresentationPlanError); });
  $("presentation-create-kind").addEventListener("change", syncPresentationCreateControls);
  $("presentation-dry-run").addEventListener("click", () => runPresentationApply(true));
  $("presentation-apply-source").addEventListener("click", () => runPresentationApply(false));
  $("presentation-apply-check").addEventListener("change", updatePresentationApplyButton);
  $("presentation-apply-confirmation").addEventListener("input", updatePresentationApplyButton);
  $("content-search-form").addEventListener("submit", (event) => { event.preventDefault(); renderContentPackList(); });
  $("content-query").addEventListener("input", renderContentPackList);
  $("content-slice-filter").addEventListener("change", renderContentPackList);
  $("content-new-pack").addEventListener("click", newContentPack);
  $("content-pack-form").addEventListener("submit", syncContentDraft);
  $("content-use-raw").addEventListener("click", useContentRawDraft);
  $("content-validate").addEventListener("click", validateContentDraft);
  $("content-plan").addEventListener("click", planContentDraft);
  $("content-preview").addEventListener("click", previewContentDraft);
  $("content-review").addEventListener("click", reviewContentDraft);
  $("content-verify").addEventListener("click", verifyContentDraft);
  $("content-change-select").addEventListener("change", (event) => selectContentChange(event.target.value));
  $("content-dry-run").addEventListener("click", () => runContentApply(true));
  $("content-apply-source").addEventListener("click", () => runContentApply(false));
  $("content-apply-check").addEventListener("change", updateContentApplyButton);
  $("content-legacy-ack").addEventListener("change", updateContentApplyButton);
  $("content-protected-ack").addEventListener("change", updateContentApplyButton);
  $("content-apply-confirmation").addEventListener("input", updateContentApplyButton);
  $("content-catalog-plan").addEventListener("click", planContentCatalogSave);
  $("content-catalog-dry-run").addEventListener("click", () => runContentCatalogApply(true));
  $("content-catalog-apply").addEventListener("click", () => runContentCatalogApply(false));
  $("content-catalog-apply-check").addEventListener("change", updateContentCatalogApplyButton);
  $("content-catalog-confirmation").addEventListener("input", updateContentCatalogApplyButton);
  $("text-lint").addEventListener("submit", textLint);
  $("order-search").addEventListener("submit", orderSearch);
  $("order-move-form").addEventListener("submit", planOrderMove);
  $("order-dry-run").addEventListener("click", () => runOrderApply(true));
  $("order-apply-source").addEventListener("click", () => runOrderApply(false));
  $("order-apply-check").addEventListener("change", updateOrderApplyButton);
  $("order-apply-confirmation").addEventListener("input", updateOrderApplyButton);
  $("balance-search").addEventListener("submit", balanceSearch);
  $("balance-summary-run").addEventListener("click", loadBalanceSummary);
  $("balance-editor").addEventListener("submit", planBalanceEdit);
  $("balance-dry-run").addEventListener("click", () => runBalanceApply(true));
  $("balance-apply-source").addEventListener("click", () => runBalanceApply(false));
  $("balance-apply-check").addEventListener("change", updateBalanceApplyButton);
  $("balance-legacy-ack").addEventListener("change", updateBalanceApplyButton);
  $("balance-protected-ack").addEventListener("change", updateBalanceApplyButton);
  $("balance-apply-confirmation").addEventListener("input", updateBalanceApplyButton);
  $("impact-run").addEventListener("click", () => runWorkbench("impact"));
  $("order-report-run").addEventListener("click", () => runWorkbench("order"));
  $("readiness-run").addEventListener("click", () => runWorkbench("readiness"));
  $("workbench-summary-run").addEventListener("click", () => runWorkbench("summary"));
  document.querySelectorAll(".editor-tab").forEach((tab) => tab.addEventListener("click", () => setEditor(tab.dataset.editor, "", [])));
  $("semantic-editor").addEventListener("submit", planSemanticEdit);
  $("dry-run").addEventListener("click", () => runApply(true));
  $("apply-source").addEventListener("click", () => runApply(false));
  $("apply-check").addEventListener("change", updateApplyButton);
  $("apply-confirmation").addEventListener("input", updateApplyButton);
}

async function start() {
  wireEvents();
  clearPlan();
  clearOrderPlan();
  clearBalancePlan();
  clearPresentationPlan();
  clearContentPlan();
  clearContentCatalogPlan();
  renderContentDraft();
  setPresentationInspector(null);
  updatePresentationDraftStatus();
  try {
    const health = await request("/api/health");
    setConnection(`Local Studio · ${health.status}`, "good");
  } catch (error) { setConnection("Studio unavailable", "bad"); }
  await loadOverview();
}

start();
