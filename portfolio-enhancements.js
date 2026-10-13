(() => {
  const pathLinks = [...document.querySelectorAll('[data-path-choice]')];
  const pathItems = [...document.querySelectorAll('[data-paths]')];
  const pathRoutes = [...document.querySelectorAll('[data-path]')];
  const pathStatus = document.querySelector('[data-path-status]');
  const pathReset = document.querySelector('[data-path-reset]');
  function selectPath(path) {
    for (const item of pathItems) {
      if (path) item.dataset.pathMatch = String(item.dataset.paths.split(' ').includes(path));
      else delete item.dataset.pathMatch;
    }
    for (const route of pathRoutes) route.dataset.selected = String(route.dataset.path === path);
    for (const anchor of pathLinks) {
      if (anchor.getAttribute('href') === '#path-' + path) anchor.setAttribute('aria-current', 'location');
      else anchor.removeAttribute('aria-current');
    }
    const selected = pathLinks.find(anchor => anchor.getAttribute('href') === '#path-' + path);
    if (pathStatus) pathStatus.textContent = path ? `Highlighted: ${selected?.textContent || path}. All projects remain visible.` : 'All paths and projects are shown.';
    if (pathReset) pathReset.hidden = !path;
  }
  function pathFromHash() {
    const match = window.location.hash.match(/^#path-([a-z0-9-]+)$/);
    const path = match?.[1] || '';
    selectPath(pathLinks.some(anchor => anchor.getAttribute('href') === '#path-' + path) ? path : '');
  }
  for (const anchor of [...pathLinks, ...document.querySelectorAll('[data-map-path]')]) {
    anchor.addEventListener('click', event => {
      if (!window.history?.replaceState || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button > 0) return;
      const hash = anchor.getAttribute('href');
      const path = hash?.match(/^#path-([a-z0-9-]+)$/)?.[1];
      if (!path) return;
      try { window.history.replaceState(null, '', hash); } catch (_) { return; }
      event.preventDefault();
      selectPath(path);
    });
  }
  window.addEventListener('hashchange', pathFromHash);
  pathFromHash();
  pathReset?.addEventListener('click', () => {
    selectPath('');
    window.location.hash = '#paths';
  });

  const start = document.querySelector('[data-presenter-start]');
  const sections = [...document.querySelectorAll('[data-case-section]')];
  const controls = document.querySelector('[data-presenter-controls]');
  const previous = document.querySelector('[data-presenter-prev]');
  const next = document.querySelector('[data-presenter-next]');
  const exit = document.querySelector('[data-presenter-exit]');
  const status = document.querySelector('[data-presenter-status]');
  if (start && sections.length && controls) {
    let presenting = false;
    let current = 0;
    let savedScroll = 0;
    let savedFocus;
    function showSection(index) {
      current = Math.max(0, Math.min(sections.length - 1, index));
      sections.forEach((section, position) => { section.hidden = position !== current; });
      previous.disabled = current === 0;
      next.disabled = current === sections.length - 1;
      status.textContent = `${current + 1} of ${sections.length}: ${sections[current].querySelector('h2')?.textContent || sections[current].id}`;
      sections[current].focus({ preventScroll: true });
      window.scrollTo(0, 0);
    }
    function exitPresentation() {
      presenting = false;
      delete document.body.dataset.presenting;
      sections.forEach(section => { section.hidden = false; });
      controls.hidden = true;
      (savedFocus || start).focus({ preventScroll: true });
      window.scrollTo(0, savedScroll);
    }
    start.hidden = false;
    start.addEventListener('click', () => {
      savedScroll = window.scrollY;
      savedFocus = document.activeElement;
      presenting = true;
      document.body.dataset.presenting = 'true';
      controls.hidden = false;
      const destination = sections.findIndex(section => '#' + section.id === window.location.hash);
      showSection(destination >= 0 ? destination : 0);
    });
    previous.addEventListener('click', () => showSection(current - 1));
    next.addEventListener('click', () => showSection(current + 1));
    exit.addEventListener('click', exitPresentation);
    document.addEventListener('keydown', event => {
      if (!presenting) return;
      if (event.key === 'Escape') { event.preventDefault(); exitPresentation(); return; }
      if (event.target?.closest?.('.diagram-viewport') || event.target?.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(event.target?.tagName)) return;
      const movement = { ArrowRight: current + 1, PageDown: current + 1, ArrowLeft: current - 1, PageUp: current - 1, Home: 0, End: sections.length - 1 };
      if (Object.hasOwn(movement, event.key)) { event.preventDefault(); showSection(movement[event.key]); }
    });
    // A native section link should also be useful while presenting.
    window.addEventListener('hashchange', () => {
      if (!presenting) return;
      const destination = sections.findIndex(section => '#' + section.id === window.location.hash);
      if (destination >= 0) { showSection(destination); return; }
      const target = document.getElementById(window.location.hash.slice(1));
      const owner = target?.closest('[data-case-section]');
      const ownerIndex = sections.indexOf(owner);
      if (ownerIndex < 0) { exitPresentation(); return; }
      showSection(ownerIndex);
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
      target.scrollIntoView({ block: 'start', behavior: 'auto' });
    });
  }

  for (const diagram of document.querySelectorAll('[data-diagram]')) {
    const canvas = diagram.querySelector('.diagram-canvas');
    const viewport = diagram.querySelector('.diagram-viewport');
    const toolbar = diagram.querySelector('[data-diagram-controls]');
    const zoomStatus = diagram.querySelector('[data-zoom-status]');
    const flow = diagram.querySelector('[data-flow-toggle]');
    if (!canvas || !viewport || !toolbar) continue;
    toolbar.hidden = false;
    let zoom = 100;
    const readableWidth = parseFloat(window.getComputedStyle?.(canvas).minWidth) || 1160;
    function setFlow(active) {
      diagram.dataset.highlightFlows = String(active);
      flow?.setAttribute('aria-pressed', String(active));
    }
    for (const button of diagram.querySelectorAll('[data-zoom]')) {
      button.addEventListener('click', () => {
        if (button.dataset.zoom === 'reset') {
          zoom = 100;
          viewport.scrollLeft = viewport.scrollTop = 0;
          setFlow(false);
        } else zoom = Math.max(100, Math.min(250, zoom + (button.dataset.zoom === 'in' ? 25 : -25)));
        canvas.style.width = zoom + '%';
        canvas.style.minWidth = (readableWidth * zoom / 100) + 'px';
        if (zoomStatus) zoomStatus.textContent = zoom + '%';
      });
    }
    flow?.addEventListener('click', () => setFlow(diagram.dataset.highlightFlows !== 'true'));
  }
})();
