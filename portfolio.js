(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById('theme-toggle');
  const menuButton = document.getElementById('menu-toggle');
  const navigation = document.getElementById('primary-navigation');
  const preference = window.matchMedia('(prefers-color-scheme: dark)');
  let explicitTheme;
  try { explicitTheme = localStorage.getItem('cc-theme'); } catch (_) { /* Preferences are optional. */ }
  if (!['light', 'dark'].includes(explicitTheme)) explicitTheme = null;
  function applyTheme(theme) {
    root.dataset.theme = theme;
    themeButton.textContent = theme === 'dark' ? 'Light theme' : 'Dark theme';
    themeButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }
  applyTheme(explicitTheme || (preference.matches ? 'dark' : 'light'));
  themeButton.hidden = false;
  themeButton.addEventListener('click', () => {
    explicitTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(explicitTheme);
    try { localStorage.setItem('cc-theme', explicitTheme); } catch (_) { /* Keep the choice for this visit. */ }
  });
  preference.addEventListener('change', event => {
    if (!explicitTheme) applyTheme(event.matches ? 'dark' : 'light');
  });

  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.dataset.open = String(open);
  }
  root.dataset.enhanced = 'true';
  menuButton.hidden = false;
  setMenu(false);
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    setMenu(open);
    if (open) navigation.querySelector('a')?.focus();
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menuButton.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!navigation.contains(event.target) && !menuButton.contains(event.target)) setMenu(false);
  });

  function focusDestination() {
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { return; }
    const destination = document.getElementById(id);
    if (!destination) return;
    destination.setAttribute('tabindex', '-1');
    destination.focus({ preventScroll: true });
  }
  window.addEventListener('hashchange', focusDestination);
  if (window.location.hash) requestAnimationFrame(focusDestination);
})();
