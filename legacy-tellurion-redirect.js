// Keep published demo navigation working after repository consolidation.
(() => {
  if (location.pathname === '/tellurion-demos/demos/'
      || location.pathname === '/tellurion-demos/demos') {
    location.replace('https://ccancellieri.github.io/tellurion/' + location.search + location.hash);
    return;
  }

  const routes = [
    ['/tellurion-demos/', '/tellurion/'],
    ['/tellurion-italy-demo/', '/tellurion/italy/'],
  ];
  for (const [oldRoot, newRoot] of routes) {
    if (location.pathname.startsWith(oldRoot)) {
      location.replace('https://ccancellieri.github.io' + newRoot
        + location.pathname.slice(oldRoot.length) + location.search + location.hash);
      break;
    }
  }
})();
