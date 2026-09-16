const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const root = path.resolve(__dirname, '..');

test('legacy demo navigation preserves route, query and fragment', () => {
  const script = fs.readFileSync(path.join(root, 'legacy-tellurion-redirect.js'), 'utf8');
  for (const [pathname, expected] of [
    ['/tellurion-demos/', '/tellurion/'],
    ['/tellurion-demos/demos/zarr/', '/tellurion/demos/zarr/'],
    ['/tellurion-demos/snapshots/2026-09-15/demos/maps/', '/tellurion/snapshots/2026-09-15/demos/maps/'],
    ['/tellurion-italy-demo/articles/tools-have-different-jobs/', '/tellurion/italy/articles/tools-have-different-jobs/'],
  ]) {
    let destination;
    const location = { pathname, search: '?view=map', hash: '#evidence', replace: value => { destination = value; } };
    vm.runInNewContext(script, { location });
    assert.equal(destination, 'https://ccancellieri.github.io' + expected + '?view=map#evidence');
    const page = fs.readFileSync(path.join(root, pathname, 'index.html'), 'utf8');
    assert.ok(page.includes('href="https://ccancellieri.github.io' + expected + '"'));
    assert.ok(page.includes('src="/legacy-tellurion-redirect.js"'));
  }
});

test('unrelated portfolio routes are not redirected', () => {
  const script = fs.readFileSync(path.join(root, 'legacy-tellurion-redirect.js'), 'utf8');
  let called = false;
  vm.runInNewContext(script, { location: { pathname: '/privacy-policy.html', replace: () => { called = true; } } });
  assert.equal(called, false);
});
