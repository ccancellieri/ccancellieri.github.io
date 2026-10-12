const endpoint = 'https://public-api.wordpress.com/rest/v1.1/sites/ccancellieri.wordpress.com/posts/?number=8&order=DESC&order_by=date&fields=ID,title,URL,date,excerpt&status=publish';
const unavailable = 'Recent publications are temporarily unavailable. Browse all articles on WordPress.';

export function plainText(html) {
  const parsed = new DOMParser().parseFromString(html, 'text/html');
  parsed.querySelectorAll('script, style').forEach(node => node.remove());
  return (parsed.body.textContent || '').replace(/\s+/g, ' ').trim();
}

export function publicationUrl(value) {
  if (typeof value !== 'string') return null;
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.hostname !== 'ccancellieri.wordpress.com' || url.username || url.password || url.port) return null;
    url.hash = '';
    url.search = '';
    return url.href;
  } catch (_) { return null; }
}

export function selectPublications(payload, excluded = [], decode = plainText) {
  if (!Array.isArray(payload?.posts)) return [];
  const seen = new Set(excluded.map(publicationUrl).filter(Boolean));
  return payload.posts.map(post => {
    if (!post || typeof post.title !== 'string' || typeof post.date !== 'string') return null;
    const url = publicationUrl(post.URL);
    const timestamp = Date.parse(post.date);
    const title = decode(post.title);
    if (!url || !Number.isFinite(timestamp) || !title) return null;
    return { url, title, timestamp, excerpt: typeof post.excerpt === 'string' ? decode(post.excerpt).slice(0, 260) : '' };
  }).filter(Boolean).sort((a, b) => b.timestamp - a.timestamp).filter(post => {
    if (seen.has(post.url)) return false;
    seen.add(post.url);
    return true;
  }).slice(0, 8);
}

export async function enhancePublications(doc = document, fetchPosts = fetch, decode = plainText) {
  const list = doc.querySelector('#latest-publications .writing-list');
  const status = doc.getElementById('publications-status');
  if (!list || !status) return;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetchPosts(endpoint, { signal: controller.signal, credentials: 'omit' });
    if (!response.ok) throw new Error('Unavailable');
    const curated = Array.from(doc.querySelectorAll('#writing > .container > .writing-list a'), link => link.href);
    const publications = selectPublications(await response.json(), curated, decode);
    if (!publications.length) throw new Error('No publications');
    const fragment = doc.createDocumentFragment();
    for (const post of publications) {
      const article = doc.createElement('article');
      article.className = 'writing-item';
      const heading = doc.createElement('h3');
      const link = doc.createElement('a');
      link.href = post.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = post.title;
      heading.append(link);
      const summary = doc.createElement('p');
      const date = new Date(post.timestamp).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
      summary.textContent = `${date}${post.excerpt ? ` · ${post.excerpt}` : ''}`;
      article.append(heading, summary);
      fragment.append(article);
    }
    list.replaceChildren(fragment);
    status.textContent = 'Latest from WordPress';
  } catch (_) {
    status.textContent = unavailable;
  } finally {
    clearTimeout(timeout);
  }
}

if (typeof document !== 'undefined') enhancePublications();
