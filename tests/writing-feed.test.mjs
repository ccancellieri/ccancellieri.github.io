import test from 'node:test';
import assert from 'node:assert/strict';
import { publicationUrl, selectPublications, enhancePublications } from '../writing-feed.mjs';

const post = (slug, date = '2026-09-01T12:00:00Z') => ({ URL: `https://ccancellieri.wordpress.com/${slug}/`, date, title: slug, excerpt: 'Summary' });
const identity = value => value;

test('accepts only HTTPS links on the exact public host without credentials', () => {
  for (const value of ['javascript:alert(1)', 'http://ccancellieri.wordpress.com/a', 'https://ccancellieri.wordpress.com.evil.test/a', 'https://user@ccancellieri.wordpress.com/a', 'https://ccancellieri.wordpress.com:444/a', null]) {
    assert.equal(publicationUrl(value), null);
  }
  assert.equal(publicationUrl('https://ccancellieri.wordpress.com/a/?ref=x#part'), 'https://ccancellieri.wordpress.com/a/');
});

test('rejects malformed posts, sorts newest first, removes duplicates and curated URLs', () => {
  const result = selectPublications({ posts: [post('old'), post('new', '2026-10-01'), post('new'), post('curated'), null, { ...post('bad'), date: 'invalid' }, { ...post('empty'), title: '' }] }, [post('curated').URL], identity);
  assert.deepEqual(result.map(item => item.title), ['new', 'old']);
  assert.deepEqual(selectPublications({ posts: {} }, [], identity), []);
  assert.equal(selectPublications({ posts: Array.from({ length: 20 }, (_, i) => post(String(i))) }, [], identity).length, 8);
});

function fixture() {
  const list = { children: ['fallback'], replaceChildren(fragment) { this.children = fragment.children; } };
  const status = { textContent: '' };
  const create = () => ({ children: [], append(...nodes) { this.children.push(...nodes); } });
  const doc = {
    querySelector: () => list,
    getElementById: () => status,
    querySelectorAll: () => [],
    createDocumentFragment: create,
    createElement: create,
  };
  return { doc, list, status };
}

test('network, HTTP, malformed and empty responses preserve fallback children', async () => {
  for (const fetchPosts of [async () => { throw new Error('Offline'); }, async () => ({ ok: false }), async () => ({ ok: true, json: async () => ({ posts: [] }) }), async () => ({ ok: true, json: async () => ({ posts: [null] }) })]) {
    const { doc, list, status } = fixture();
    await enhancePublications(doc, fetchPosts, identity);
    assert.deepEqual(list.children, ['fallback']);
    assert.match(status.textContent, /temporarily unavailable/);
  }
});

test('renders untrusted content only as text and omits credentials', async () => {
  const { doc, list, status } = fixture();
  const title = '<img src=x onerror=alert(1)>';
  await enhancePublications(doc, async (_, options) => {
    assert.equal(options.credentials, 'omit');
    assert.ok(options.signal instanceof AbortSignal);
    return { ok: true, json: async () => ({ posts: [{ ...post('safe'), title }] }) };
  }, identity);
  assert.equal(list.children[0].children[0].children[0].textContent, title);
  assert.equal(list.children[0].children[0].children[0].innerHTML, undefined);
  assert.equal(status.textContent, 'Latest from WordPress');
});
