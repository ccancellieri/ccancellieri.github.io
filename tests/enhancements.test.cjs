const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

function element(dataset = {}) {
  const listeners = {};
  const classes = new Set();
  return { dataset, hidden: true, disabled: false, textContent: '', attrs: {}, style: {},
    classList: { toggle(name, enabled) { enabled ? classes.add(name) : classes.delete(name); }, contains(name) { return classes.has(name); } },
    addEventListener(type, callback) { (listeners[type] ||= []).push(callback); },
    fire(type, event = {}) { for (const callback of listeners[type] || []) callback(event); },
    setAttribute(key, value) { this.attrs[key] = String(value); },
    removeAttribute(key) { delete this.attrs[key]; },
    getAttribute(key) { return this.attrs[key]; },
    focus() { this.focused = true; },
    scrollIntoView(options) { this.scrolledIntoView = options; },
    closest() { return null; },
    querySelector() { return null; }, querySelectorAll() { return []; },
  };
}

function fixture() {
  const start = element(), controls = element(), previous = element(), next = element(), exit = element(), status = element();
  const sections = ['problem', 'architecture', 'decisions', 'outcomes', 'learning'].map(id => ({ ...element(), id, hidden: false }));
  const pathLink = element(); pathLink.attrs.href = '#path-cloud';
  const pathItems = [element({ paths: 'architecture cloud' }), element({ paths: 'security' })];
  for (const item of pathItems) item.hidden = false;
  const pathStatus = element(), reset = element();
  const diagram = element(), zoomIn = element({ zoom: 'in' }), zoomOut = element({ zoom: 'out' }), zoomReset = element({ zoom: 'reset' }), flow = element();
  const canvas = element(), viewport = element(), zoomStatus = element(), diagramControls = element();
  diagram.id = 'diagram-sample-architecture-1';
  diagram.closest = selector => selector === '[data-case-section]' ? sections[1] : null;
  viewport.closest = selector => selector === '.diagram-viewport' ? viewport : null;
  diagram.querySelector = selector => ({ '.diagram-canvas': canvas, '.diagram-viewport': viewport, '[data-diagram-controls]': diagramControls, '[data-zoom-status]': zoomStatus, '[data-flow-toggle]': flow })[selector] || null;
  diagram.querySelectorAll = selector => selector === '[data-zoom]' ? [zoomIn, zoomOut, zoomReset] : [];
  const singles = { '[data-presenter-start]': start, '[data-presenter-controls]': controls, '[data-presenter-prev]': previous, '[data-presenter-next]': next, '[data-presenter-exit]': exit, '[data-presenter-status]': status, '[data-path-status]': pathStatus, '[data-path-reset]': reset };
  const doc = element(); doc.body = element(); doc.activeElement = start;
  doc.querySelector = selector => singles[selector] || null;
  doc.getElementById = id => id === diagram.id ? diagram : sections.find(section => section.id === id) || null;
  doc.querySelectorAll = selector => ({ '[data-case-section]': sections, '[data-paths]': pathItems, '[data-path-choice]': [pathLink], '[data-path]': [], '[data-diagram]': [diagram] })[selector] || [];
  const win = element(); win.location = { hash: '#paths' }; win.scrollY = 150;
  win.scrollTo = (_, y) => { win.restoredScroll = y; };
  win.history = { replaceState(_, __, hash) { win.location.hash = hash; } };
  viewport.clientWidth = 350;
  const file = path.join(__dirname, '../portfolio-enhancements.js');
  assert.ok(fs.existsSync(file), 'Progressive enhancement script is missing');
  vm.runInNewContext(fs.readFileSync(file, 'utf8'), { document: doc, window: win });
  return { doc, win, start, controls, previous, next, exit, status, sections, pathLink, pathItems, reset, pathStatus, zoomIn, zoomOut, zoomReset, flow, canvas, viewport, zoomStatus, diagramControls, diagram };
}

test('path selection highlights overlapping projects while leaving every project visible', () => {
  const f = fixture();
  f.win.location.hash = '#path-cloud'; f.win.fire('hashchange');
  assert.equal(f.pathItems[0].dataset.pathMatch, 'true');
  assert.equal(f.pathItems[1].dataset.pathMatch, 'false');
  assert.equal(f.pathItems[0].hidden, false);
  assert.equal(f.pathItems[1].hidden, false);
  assert.match(f.pathStatus.textContent, /cloud/i);
  f.reset.fire('click');
  assert.equal(f.pathItems[0].dataset.pathMatch, undefined);
  assert.equal(f.pathItems[1].dataset.pathMatch, undefined);
});

test('enhanced path clicks update the URL without scrolling the connection map away', () => {
  const f = fixture(); let prevented = false;
  f.pathLink.fire('click', { preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(f.win.location.hash, '#path-cloud');
  assert.equal(f.pathItems[0].dataset.pathMatch, 'true');
  assert.equal(f.win.restoredScroll, undefined);
});

test('presentation responds to keyboard, stops at boundaries, and restores the reading page on Escape', () => {
  const f = fixture();
  f.start.fire('click');
  assert.equal(f.controls.hidden, false);
  assert.equal(f.previous.disabled, true);
  assert.equal(f.sections[0].hidden, false);
  assert.equal(f.sections[1].hidden, true);
  let prevented = false;
  f.doc.fire('keydown', { key: 'ArrowRight', preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(f.sections[0].hidden, true);
  assert.equal(f.sections[1].hidden, false);
  assert.equal(f.sections[1].focused, true);
  f.doc.fire('keydown', { key: 'End', preventDefault() {} });
  assert.equal(f.next.disabled, true);
  assert.equal(f.sections[4].hidden, false);
  f.doc.fire('keydown', { key: 'Escape', preventDefault() {} });
  assert.ok(f.sections.every(section => section.hidden === false));
  assert.equal(f.controls.hidden, true);
  assert.equal(f.start.focused, true);
  assert.equal(f.win.restoredScroll, 150);
});

test('architecture view fragments retain presentation and focus the requested figure', () => {
  const f = fixture(); f.start.fire('click'); f.next.fire('click');
  f.win.location.hash = '#diagram-sample-architecture-1'; f.win.fire('hashchange');
  assert.equal(f.doc.body.dataset.presenting, 'true');
  assert.equal(f.controls.hidden, false);
  assert.equal(f.sections[1].hidden, false);
  assert.equal(f.sections[0].hidden, true);
  assert.equal(f.sections[2].hidden, true);
  assert.equal(f.diagram.focused, true);
  assert.equal(f.diagram.attrs.tabindex, '-1');
  assert.equal(f.diagram.scrolledIntoView?.block, 'start');
  assert.notEqual(f.win.restoredScroll, 150, 'A diagram link must not restore the old reading scroll position');
});

test('diagram keyboard panning keeps the architecture section active, while Escape exits', () => {
  const f = fixture(); f.start.fire('click'); f.next.fire('click');
  for (const key of ['ArrowRight', 'ArrowLeft', 'Home', 'End', 'PageDown', 'PageUp']) {
    let prevented = false;
    f.doc.fire('keydown', { key, target: f.viewport, preventDefault() { prevented = true; } });
    assert.equal(prevented, false, `${key} must remain available to the diagram scroll region`);
    assert.equal(f.sections[1].hidden, false);
    assert.equal(f.sections[2].hidden, true);
  }
  f.doc.fire('keydown', { key: 'Escape', target: f.viewport, preventDefault() {} });
  assert.equal(f.controls.hidden, true);
  assert.ok(f.sections.every(section => !section.hidden));
});

test('presentation does not consume typing keys in interactive fields', () => {
  const f = fixture(); f.start.fire('click');
  f.doc.fire('keydown', { key: 'ArrowRight', target: { tagName: 'INPUT' }, preventDefault() { throw new Error('Typing intercepted'); } });
  assert.equal(f.sections[0].hidden, false);
});

test('diagram zoom uses bounded scrollable canvas and reset removes flow emphasis', () => {
  const f = fixture();
  assert.equal(f.diagramControls.hidden, false);
  f.zoomIn.fire('click');
  assert.equal(f.canvas.style.width, '125%');
  assert.equal(f.canvas.style.minWidth, '1450px', 'Zoom must expand the minimum readable width even on a 350px viewport');
  f.flow.fire('click');
  assert.equal(f.diagram.dataset.highlightFlows, 'true');
  assert.equal(f.flow.attrs['aria-pressed'], 'true');
  for (let i = 0; i < 20; i++) f.zoomIn.fire('click');
  assert.equal(f.canvas.style.width, '250%');
  f.zoomReset.fire('click');
  assert.equal(f.canvas.style.width, '100%');
  assert.equal(f.diagram.dataset.highlightFlows, 'false');
  assert.equal(f.zoomStatus.textContent, '100%');
});
