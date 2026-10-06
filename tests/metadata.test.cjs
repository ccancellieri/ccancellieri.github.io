const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const html = () => fs.readFileSync(path.join(root, 'index.html'), 'utf8');

test('search and sharing titles describe the person rather than one product', () => {
  const source = html();
  const title = 'Carlo Cancellieri | Software Engineering &amp; Architecture';
  assert.ok(source.includes(`<title>${title}</title>`));
  assert.ok(source.includes(`property="og:title" content="${title}"`));
  assert.ok(source.includes(`name="twitter:title" content="${title}"`));
  assert.match(source, /name="description" content="[^"]*DevOps[^"]*geospatial/i);
});

test('person metadata uses supported current title and cross-platform breadth', () => {
  const json = html().match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  assert.ok(json);
  const person = JSON.parse(json[1]);
  assert.equal(person.jobTitle, 'Lead Software Engineer');
  assert.ok(person.knowsAbout.includes('Distributed and Grid Computing'));
  assert.ok(person.knowsAbout.includes('Linux'));
  assert.ok(person.sameAs.includes('https://x.com/cancellieric'));
  assert.ok(person.sameAs.includes('https://ccancellieri.wordpress.com/'));
  assert.equal(person.email, undefined);
  assert.equal(person.telephone, undefined);
});

test('homepage sitemap has current revision date', () => {
  const xml = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
  assert.match(xml, /<loc>https:\/\/ccancellieri.github.io\/<\/loc>\s*<lastmod>2026-10-06<\/lastmod>/);
});

test('public presence and research writing remain visible without scripts', () => {
  const body = html().replace(/<script[\s\S]*?<\/script>/g, '');
  assert.match(body, /href="https:\/\/x.com\/cancellieric"/);
  assert.match(body, /href="https:\/\/ccancellieri.wordpress.com\/"/);
  assert.match(body, /href="https:\/\/www.linkedin.com\/pulse\/55-fewer-tokens-one-wrong-source-why-i-paused-visual-cancellieri-r3zwe\/"/);
});

test('technical foundations are distinct from employment tenure', () => {
  const source = html();
  assert.match(source, /Linux user since 1997/);
  assert.match(source, /Linux, macOS and Windows/);
  assert.match(source, /C99/);
  assert.match(source, /Feb 2020–Present/);
  assert.doesNotMatch(source, /As I conclude my FAO chapter|20\+ years|20 years architecting/i);
});
