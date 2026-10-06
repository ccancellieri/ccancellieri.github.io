const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

function element() {
  const listeners = {};
  return { dataset: {}, hidden: false, textContent: '', attributes: {}, focused: false,
    setAttribute(name, value) { this.attributes[name] = String(value); },
    getAttribute(name) { return this.attributes[name]; },
    addEventListener(name, handler) { listeners[name] = handler; },
    fire(name, event = {}) { listeners[name]?.(event); },
    focus() { this.focused = true; },
    contains(node) { return node === this; }
  };
}

function run({ blockedStorage = false, hash = '#projects' } = {}) {
  const elements = Object.fromEntries(['theme-toggle', 'menu-toggle', 'primary-navigation', 'projects', 'language-select'].map(id => [id, element()]));
  elements.firstLink = element();
  elements['primary-navigation'].querySelector = () => elements.firstLink;
  const document = element();
  document.documentElement = element();
  document.getElementById = id => elements[id] || null;
  document.querySelectorAll = () => [];
  const window = element();
  window.location = { hash };
  const media = element();
  media.matches = false;
  window.matchMedia = () => media;
  const localStorage = { getItem() { if (blockedStorage) throw new Error('blocked'); return null; }, setItem() { if (blockedStorage) throw new Error('blocked'); } };
  const file = path.join(root, 'portfolio.js');
  const script = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1]).join('\n');
  vm.runInNewContext(script, { document, window, localStorage, decodeURIComponent, requestAnimationFrame: callback => callback(), navigator: { language: 'en' }, IntersectionObserver: class { observe() {} } });
  return { elements, document, window };
}

test('blocked preference storage still permits theme changes', () => {
  const { elements, document } = run({ blockedStorage: true });
  elements['theme-toggle'].fire('click');
  assert.equal(document.documentElement.dataset.theme, 'dark');
  assert.equal(elements['theme-toggle'].attributes['aria-label'], 'Switch to light theme');
});

test('menu opens and Escape closes it with focus returned to its button', () => {
  const { elements, document } = run();
  elements['menu-toggle'].fire('click');
  assert.equal(elements['menu-toggle'].attributes['aria-expanded'], 'true');
  document.fire('keydown', { key: 'Escape' });
  assert.equal(elements['menu-toggle'].attributes['aria-expanded'], 'false');
  assert.equal(elements['menu-toggle'].focused, true);
});

test('deep links focus their destination while keeping native navigation', () => {
  const { elements, window } = run();
  assert.equal(elements.projects.focused, true);
  assert.equal(window.location.hash, '#projects');
  elements.projects.focused = false;
  window.fire('hashchange');
  assert.equal(elements.projects.focused, true);
});

test('opening the mobile menu moves keyboard focus into its links', () => {
  const { elements } = run();
  elements['menu-toggle'].fire('click');
  assert.equal(elements.firstLink.focused, true);
});

test('every internal navigation destination exists in the document', () => {
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]));
  const markup = html.replace(/<script[\s\S]*?<\/script>/g, '');
  for (const match of markup.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.has(match[1]), `Missing destination ${match[1]}`);
});

test('project evidence disclosures have balanced native details boundaries', () => {
  let open = 0;
  for (const tag of html.matchAll(/<\/?details\b[^>]*>/g)) {
    open += tag[0].startsWith('</') ? -1 : 1;
    assert.ok(open >= 0, 'A disclosure closes before it opens');
  }
  assert.equal(open, 0, 'A disclosure remains unclosed');
});
