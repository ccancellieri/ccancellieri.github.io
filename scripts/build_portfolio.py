#!/usr/bin/env python3
"""Build public case studies and library pages from plain-text JSON."""
import argparse
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

SECTIONS = ('problem', 'architecture', 'decisions', 'outcomes', 'learning')
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NS)


def esc(value):
    return html.escape(str(value), quote=True)


def read_json(path, fallback=None):
    return json.loads(path.read_text()) if path.exists() else fallback


def public_url(value):
    """Accept HTTPS sources or root-relative public routes, never local paths."""
    if not isinstance(value, str) or any(c.isspace() for c in value):
        raise ValueError(f'Expected a public URL: {value!r}')
    decoded = unquote(value)
    parsed = urlsplit(value)
    if '\\' in decoded or any(p == '..' for p in decoded.split('/')):
        raise ValueError(f'Expected a public URL: {value!r}')
    if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password:
        return value
    if value.startswith('/') and not value.startswith('//') and not parsed.scheme and not parsed.netloc and not decoded.startswith(('/Users/', '/private/', '/tmp/', '/home/')):
        return value
    raise ValueError(f'Expected a public URL: {value!r}')


def safe_id(value, label):
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        raise ValueError(f'Invalid {label}: {value!r}')
    return value


def local_file(root, url):
    value = public_url(url)
    if value.startswith('/'):
        target = (root / urlsplit(value).path.lstrip('/')).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError(f'Expected a public URL: {value!r}')
        return target
    return None


def svg_markup(root, diagram, check):
    src = public_url(diagram['src'])
    file = local_file(root, src)
    if not file or file.suffix != '.svg':
        raise ValueError('Diagram src must be a local public SVG URL')
    if not file.exists():
        if check:
            raise ValueError(f'Missing public diagram: {src}')
        return f'<img src="{esc(src)}" alt="{esc(diagram["description"])}" loading="lazy">'
    markup = file.read_text()
    tree = ET.fromstring(markup)
    if tree.tag.split('}')[-1] != 'svg':
        raise ValueError(f'Diagram is not SVG: {src}')
    for node in tree.iter():
        tag = node.tag.split('}')[-1]
        if tag in ('script', 'foreignObject', 'image', 'use', 'iframe'):
            raise ValueError(f'Unsupported SVG element in {src}: {tag}')
        for key, value in node.attrib.items():
            key = key.split('}')[-1]
            if key.lower().startswith('on') or key in ('href', 'src'):
                raise ValueError(f'Unsupported SVG reference in {src}')
            if 'url(' in value and not re.fullmatch(r'url\(#[a-zA-Z0-9_-]+\)', value):
                raise ValueError(f'Unsupported SVG style reference in {src}')
    if '<!DOCTYPE' in markup or '<!ENTITY' in markup:
        raise ValueError(f'Unsupported SVG declaration in {src}')
    # Prefix identifiers so figures using common marker names cannot collide.
    prefix = safe_id(file.stem, 'diagram filename') + '-'
    identifiers = re.findall(r'\bid="([^"]+)"', markup)
    for identifier in identifiers:
        markup = markup.replace(f'id="{identifier}"', f'id="{prefix}{identifier}"')
        markup = markup.replace(f'url(#{identifier})', f'url(#{prefix}{identifier})')
    markup = re.sub(r'aria-labelledby="([^"]+)"', lambda m: 'aria-labelledby="' + ' '.join(prefix + i for i in m[1].split()) + '"', markup)
    root_id = prefix + 'root'
    markup = re.sub(r'<svg\b([^>]*)>', lambda m: '<svg' + re.sub(r'\s+id="[^"]*"', '', m[1]) + ' id="' + root_id + '">', markup, count=1)
    def scope_style(match):
        css = match[1]
        if re.search(r'@|expression\s*\(|javascript:', css, re.I) or re.search(r'url\((?!#[a-zA-Z0-9_-]+\))', css):
            raise ValueError(f'Unsupported SVG style in {src}')
        scoped = re.sub(r'([^{}]+)\{([^{}]*)\}', lambda rule: ','.join('#' + root_id + ' ' + selector.strip() for selector in rule[1].split(',')) + '{' + rule[2] + '}', css)
        return '<style>' + scoped + '</style>'
    markup = re.sub(r'<style[^>]*>([\s\S]*?)</style>', scope_style, markup)
    return re.sub(r'<\?xml[^>]*\?>', '', markup).strip()


def render_template(root, name, values):
    source = (root / 'templates' / name).read_text()
    for asset in ('portfolio.css', 'portfolio.js', 'portfolio-enhancements.js', 'writing-feed.mjs'):
        slot = '{{' + asset + '_version}}'
        if slot in source:
            digest = hashlib.sha256(local_file(root, '/' + asset).read_bytes()).hexdigest()[:16]
            source = source.replace(slot, digest)
    for key, value in values.items():
        source = source.replace('{{' + key + '}}', str(value))
    if re.search(r'\{\{[^}]+\}\}', source):
        raise ValueError(f'Unresolved template slot in {name}')
    return source


def link(url, title, css=''):
    return f'<a{(" class=" + chr(34) + esc(css) + chr(34)) if css else ""} href="{esc(url if url.startswith("#") and SLUG.fullmatch(url[1:]) else public_url(url))}">{esc(title)}</a>'


def prose(section):
    paragraphs = ''.join(f'<p>{esc(p)}</p>' for p in section.get('paragraphs', []))
    bullets = section.get('bullets', [])
    if bullets:
        paragraphs += '<ul>' + ''.join(f'<li>{esc(p)}</li>' for p in bullets) + '</ul>'
    return paragraphs


def document_entry(doc, projects):
    project = doc.get('project')
    related = f'<p>{link("/projects/" + project + "/", "Read the related case study")}</p>' if project in projects else ''
    return f'<article class="library-document" id="document-{esc(doc["id"])}"><div><p class="case-meta">{esc(doc.get("type", "Document"))} · {esc(doc.get("year", ""))}</p><h2>{link(doc["url"], doc["title"])}</h2></div><div><p>{esc(doc["description"])}</p><p class="source-note">{esc(doc.get("attribution", ""))}</p>{related}</div></article>'


def case_page(root, project, site, paths, projects, library, check):
    slug = project['slug']
    canonical = site['url'].rstrip('/') + '/projects/' + slug + '/'
    title = project['title']
    path_links = ' '.join(link('/#path-' + p, paths[p]['title'], 'path-label') for p in project['paths'])
    top = f'<div class="case-heading container"><nav class="breadcrumbs" aria-label="Breadcrumb">{link("/", "Home")} / {link("/#projects", "Projects")} / <span aria-current="page">{esc(title)}</span></nav><p class="case-meta">{esc(project["kind"].replace("-", " ").title())} · {esc(project.get("period", ""))}</p><h1>{esc(title)}</h1><p class="case-role">{esc(project["role"])}</p><p class="case-summary">{esc(project["summary"])}</p><div class="path-labels">{path_links}</div><div class="case-actions"><button type="button" class="btn btn-primary" hidden data-presenter-start>Present this case</button>{link("#sources", "Sources & scope", "btn btn-secondary")}{link("/library/", "Document library", "btn btn-secondary")}</div></div>'
    toc = '<nav class="case-toc container" aria-label="Case sections">' + ''.join(link('#' + s['id'], s['title']) for s in project['sections']) + '</nav>'
    controls = '<div class="presenter-controls" hidden data-presenter-controls><button type="button" data-presenter-prev>Previous</button><span data-presenter-status aria-live="polite"></span><button type="button" data-presenter-next>Next</button><button type="button" data-presenter-exit>Exit presentation</button></div>'
    content = ''
    for section in project['sections']:
        diagrams = section.get('diagrams', [])
        navigation = f'<nav class="diagram-view-nav" data-view-count="{len(diagrams)}" aria-label="Architecture views">' + ''.join(link('#diagram-' + slug + '-' + section['id'] + '-' + str(i), d.get('view', d['title'])) for i, d in enumerate(diagrams)) + '</nav>' if diagrams else ''
        figures = ''
        for i, diagram in enumerate(diagrams):
            identifier = 'diagram-' + slug + '-' + section['id'] + '-' + str(i)
            markup = svg_markup(root, diagram, check)
            figures += f'<figure class="architecture-diagram" id="{identifier}" data-diagram><figcaption><h3>{esc(diagram["title"])}</h3><p>{esc(diagram["description"])}</p></figcaption><div class="diagram-actions">{link(diagram["src"], "Open full-size SVG", "diagram-open")}<div class="diagram-controls" hidden data-diagram-controls><button type="button" data-zoom="out" aria-label="Zoom out diagram">−</button><button type="button" data-zoom="in" aria-label="Zoom in diagram">+</button><button type="button" data-zoom="reset">Reset view</button><button type="button" data-flow-toggle aria-pressed="false">Highlight flows</button><span data-zoom-status aria-live="polite">100%</span></div></div><div class="diagram-viewport" tabindex="0" role="region" aria-label="{esc(diagram["title"])}; scroll to explore"><div class="diagram-canvas">{markup}</div></div></figure>'
        content += f'<section class="case-section" id="{section["id"]}" tabindex="-1" data-case-section><div class="container"><h2>{esc(section["title"])}</h2><div class="case-prose">{prose(section)}</div>{navigation}{figures}</div></section>'
    questions = project.get('questions', [])
    qa = '<section class="case-support"><div class="container"><h2>Questions &amp; discussion</h2>' + ''.join(f'<details class="case-question"><summary>{esc(q["question"])}</summary><p>{esc(q["answer"])}</p>{link("#" + q.get("section", "decisions"), "Read the relevant section")}</details>' for q in questions) + '</div></section>' if questions else ''
    sources = '<section class="case-support" id="sources"><div class="container"><h2>Sources &amp; scope</h2><ul class="source-list">'
    for source in project.get('sources', []):
        metadata = '; '.join(str(source[k]) for k in ('version', 'attribution') if source.get(k))
        sources += f'<li id="source-{esc(source["id"])}">{link(source["url"], source["title"])}<p class="source-note">{esc(metadata)}</p></li>'
    sources += '</ul></div></section>'
    docs = [d for d in library['documents'] if d['id'] in project.get('documents', []) or d.get('project') == slug]
    if docs:
        sources += '<section class="case-support"><div class="container"><h2>Related documents</h2>' + ''.join(document_entry(d, projects) for d in docs) + '</div></section>'
    related = [projects[s] for s in project.get('related', []) if s in projects]
    if related:
        sources += '<nav class="related-cases container" aria-label="Related case studies"><h2>Continue exploring</h2>' + ''.join(link('/projects/' + p['slug'] + '/', p['title']) for p in related) + '</nav>'
    structured = {'@context': 'https://schema.org', '@graph': [{'@type': 'CreativeWork', 'name': title, 'description': project['description'], 'url': canonical, 'author': {'@type': 'Person', 'name': site['name'], 'url': site['url']}, 'inLanguage': 'en'}, {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': site['url'] + '/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Projects', 'item': site['url'] + '/#projects'}, {'@type': 'ListItem', 'position': 3, 'name': title, 'item': canonical}]}]}
    return page(root, site, title, project['description'], canonical, structured, top + toc + controls + '<div data-case-content>' + content + '</div>' + qa + sources)


def page(root, site, title, description, canonical, structured, body):
    return render_template(root, 'page.html', {'title': esc(title), 'name': esc(site['name']), 'description': esc(description), 'canonical': esc(canonical), 'base': esc(site['url'].rstrip('/')), 'structured_data': json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c'), 'body': body, 'header': (root / 'templates/header.html').read_text(), 'footer': (root / 'templates/footer.html').read_text()})


def library_page(root, site, library, projects):
    canonical = site['url'].rstrip('/') + '/library/'
    body = '<div class="case-heading container"><nav class="breadcrumbs" aria-label="Breadcrumb">' + link('/', 'Home') + ' / <span aria-current="page">Library</span></nav><h1>Document library</h1><p class="case-summary">Thesis, presentations and research notes, with source context and related case studies.</p></div><div class="container library-list">'
    body += ''.join(document_entry(d, projects) for d in library['documents'])
    body += '</div>'
    for note in library.get('notes', []):
        body += f'<section class="case-support"><div class="container"><h2>{esc(note["title"])}</h2><div class="case-prose">{prose(note)}</div></div></section>'
    body += '<section class="case-support"><div class="container"><h2>Recent publications</h2><p class="case-prose">The homepage includes an automatically updated WordPress publication list and a readable selection when updates are unavailable.</p>' + link('/#latest-publications', 'Read recent publications') + '</div></section>'
    body += '<section class="case-support"><div class="container"><h2>Selected engineering notes</h2>'
    selected = library.get('selected_notes', [])
    if selected:
        body += '<div class="writing-list">' + ''.join('<article class="writing-item"><h3>' + link(note['url'], note['title']) + '</h3><p>' + esc(note['description']) + '</p></article>' for note in selected) + '</div>'
    else:
        body += link('/#writing', 'Browse selected engineering notes on the homepage')
    body += '</div></section>'
    structured = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Document library', 'url': canonical, 'author': {'@type': 'Person', 'name': site['name']}}
    return page(root, site, 'Document library', 'Thesis, presentations and research notes by Carlo Cancellieri.', canonical, structured, body)


def path_map(paths, projects, map_titles=None):
    labels = '<nav class="path-navigation" aria-label="Choose a portfolio path">' + ''.join(link('#path-' + p['id'], p['title'], 'path-choice').replace('<a ', '<a data-path-choice ') for p in paths) + '</nav>'
    path_rows = ''
    for p in paths:
        selected = [x for x in projects.values() if p['id'] in x['paths']]
        links = ''.join(f'<li>{link("/projects/" + x["slug"] + "/", x["title"])}</li>' for x in selected)
        path_rows += f'<div id="path-{p["id"]}" class="path-route" data-path="{p["id"]}"><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><ul>{links}</ul></div>'
    rows = list(projects.values())
    height = max(530, len(rows) * 76 + 90)
    svg = f'<svg class="portfolio-map" viewBox="0 0 1100 {height}" role="img" aria-labelledby="map-title map-description"><title id="map-title">Connected work</title><desc id="map-description">Six professional paths connect to related case studies. Projects can belong to several paths; all remain available when a path is highlighted. The text index below provides the same links.</desc>'
    positions = {}
    for i, p in enumerate(paths):
        y = 48 + i * (height - 95) / max(1, len(paths) - 1)
        positions[p['id']] = y
        svg += f'<a href="#path-{p["id"]}" data-map-path="{p["id"]}"><rect class="map-path-node" x="16" y="{y-25:.1f}" width="326" height="50" rx="5"/><text x="32" y="{y+6:.1f}">{esc(p["title"])}</text></a>'
    connections = ''
    nodes = ''
    for i, project in enumerate(rows):
        y = 48 + i * 76
        for p in project['paths']:
            connections += f'<path class="map-connection" data-paths="{p}" d="M 342 {positions[p]:.1f} C 460 {positions[p]:.1f}, 555 {y}, 674 {y}"/>'
        title = project['title']
        short = (map_titles or {}).get(project['slug'], title)
        short = short if len(short) < 42 else short[:39] + '…'
        nodes += f'<a href="/projects/{project["slug"]}/" data-paths="{" ".join(project["paths"])}"><title>{esc(title)}</title><rect class="map-project-node" x="674" y="{y-25}" width="410" height="50" rx="5"/><text x="692" y="{y+6}">{esc(short)}</text></a>'
    svg += connections + nodes + '</svg>'
    return f'<section id="paths"><div class="container"><div class="paths-heading"><h2 class="section-title">Different paths. Connected work.</h2><p class="section-intro">Explore by the decisions and disciplines that interest you. Each path connects projects across a broader engineering career.</p></div>{labels}<p class="path-status" data-path-status aria-live="polite">All paths and projects are shown.</p><div class="map-viewport">{svg}</div><button type="button" class="btn btn-secondary path-reset-button" hidden data-path-reset>Show all connections</button><div class="path-index">{path_rows}</div></div></section>'


def home_page(root, manifest, projects):
    paths = manifest['paths']
    directory = '<div class="case-directory"><h3>Explore the case studies</h3><p>Read the problem, architecture, decisions, outcomes and learning behind the work.</p><ul>' + ''.join(f'<li>{link("/projects/" + p["slug"] + "/", p["title"])}<span>{esc(p["kind"].replace("-", " "))}</span></li>' for p in projects.values()) + '</ul>' + link('/library/', 'Browse thesis, presentations and research notes') + '</div>'
    header = (root / 'templates/header.html').read_text().replace('href="/#', 'href="#')
    output = render_template(root, 'home.html', {'header': header, 'path_map': path_map(paths, projects, manifest.get("mapTitles")), 'case_directory': directory})
    # Enhance each existing project in place; its original description and evidence remain intact.
    entries = {p['title']: p for p in manifest.get('homepageProjects', [])}
    parts = re.split(r'(<(?:article|div) class="project-card[^\"]*"[^>]*>)', output)
    for i in range(1, len(parts), 2):
        match = re.search(r'<h3 class="project-title">([^<]+)</h3>', parts[i + 1])
        entry = entries.get(html.unescape(match[1])) if match else None
        if not entry:
            continue
        parts[i] = parts[i][:-1] + ' data-paths="' + esc(' '.join(entry['paths'])) + '">'
        slug = entry.get('slug')
        if slug in projects:
            target = match[0]
            parts[i + 1] = parts[i + 1].replace(target, target + '<p class="case-entry-link">' + link('/projects/' + slug + '/', 'Read case study') + '</p>', 1)
    return ''.join(parts)


def update_sitemap(root, site, routes, changed):
    file = root / 'sitemap.xml'
    tree = ET.parse(file) if file.exists() else ET.ElementTree(ET.Element(f'{{{NS}}}urlset'))
    entries = {u.findtext(f'{{{NS}}}loc'): u for u in tree.getroot()}
    for route in routes:
        url = site['url'].rstrip('/') + route
        item = entries.get(url)
        if item is None:
            item = ET.SubElement(tree.getroot(), f'{{{NS}}}url')
            ET.SubElement(item, f'{{{NS}}}loc').text = url
        date = item.find(f'{{{NS}}}lastmod')
        if date is None:
            date = ET.SubElement(item, f'{{{NS}}}lastmod')
        if route in changed or not date.text:
            date.text = site['updated']
    ET.indent(tree, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree.getroot(), encoding='unicode') + '\n'


def write_if_changed(file, output):
    if file.exists() and file.read_text() == output:
        return
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(output)


class PageReferences(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                raise ValueError(f'Duplicate HTML identifier: {attrs["id"]}')
            self.ids.add(attrs['id'])
        for attribute in ('href', 'src'):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])


def validate_references(root, outputs):
    """Check links against planned pages as well as retained static files."""
    pages = {file: PageReferences(source) for file, source in outputs.items() if file.suffix == '.html'}
    for file, page_refs in list(pages.items()):
        for value in page_refs.links:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            if not parsed.path:
                target = file
            else:
                target = (root / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else file.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root.resolve()):
                    raise ValueError(f'Reference escapes public root: {value}')
                if parsed.path.endswith('/') or target.is_dir() or not target.suffix:
                    target /= 'index.html'
            if target not in outputs and not target.is_file():
                raise ValueError(f'Missing public reference in {file.relative_to(root)}: {value}')
            if parsed.fragment and target.suffix == '.html':
                if target not in pages:
                    pages[target] = PageReferences(outputs.get(target) or target.read_text())
                if unquote(parsed.fragment) not in pages[target].ids:
                    raise ValueError(f'Missing section reference in {file.relative_to(root)}: {value}')


def build(root, check=False):
    root = root.resolve()
    manifest = read_json(root / 'content/portfolio.json')
    site = manifest['site']
    public_url(site['url'])
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', site['updated']):
        raise ValueError('Site updated date must use YYYY-MM-DD')
    paths = {safe_id(p['id'], 'path'): p for p in manifest['paths']}
    projects = {}
    for file in sorted((root / 'content/projects').glob('*.json')):
        project = read_json(file)
        slug = safe_id(project['slug'], 'project slug')
        if slug in projects:
            raise ValueError(f'Duplicate project slug: {slug}')
        if [s['id'] for s in project['sections']] != list(SECTIONS):
            raise ValueError(f'Case {slug} must have the five reading sections in order')
        if any(p not in paths for p in project['paths']):
            raise ValueError(f'Unknown path in {slug}')
        for source in project.get('sources', []):
            target = local_file(root, source['url'])
            if check and target and not target.exists():
                raise ValueError(f'Missing public source: {source["url"]}')
            safe_id(source['id'], 'source id')
        for related in project.get('related', []):
            safe_id(related, 'related slug')
        projects[slug] = project
    library = read_json(root / 'content/library.json', {'documents': [], 'notes': []})
    for doc in library['documents']:
        safe_id(doc['id'], 'document id')
        if doc.get('verification') not in ('document-inspected', 'source-inspected'):
            raise ValueError(f'Document {doc["id"]} needs inspected verification')
        target = local_file(root, doc['url'])
        if check and target and not target.exists():
            raise ValueError(f'Missing public document: {doc["url"]}')
        if doc.get('project'):
            safe_id(doc['project'], 'document project')
    if check:
        for project in projects.values():
            for slug in project.get('related', []):
                if slug not in projects:
                    raise ValueError(f'Missing related project: {slug}')
            for identifier in project.get('documents', []):
                if identifier not in {d['id'] for d in library['documents']}:
                    raise ValueError(f'Missing related document: {identifier}')
    outputs = {}
    for slug, project in projects.items():
        outputs[root / 'projects' / slug / 'index.html'] = case_page(root, project, site, paths, projects, library, check)
    outputs[root / 'library/index.html'] = library_page(root, site, library, projects)
    routes = ['/library/'] + ['/projects/' + slug + '/' for slug in projects]
    if (root / 'templates/home.html').exists():
        outputs[root / 'index.html'] = home_page(root, manifest, projects)
        routes.insert(0, '/')
    changed = {('/' if file == root / 'index.html' else '/' + file.parent.relative_to(root).as_posix() + '/') for file, output in outputs.items() if not file.exists() or file.read_text() != output}
    outputs[root / 'sitemap.xml'] = update_sitemap(root, site, routes, changed)
    if check:
        validate_references(root, outputs)
        print(f'Validated {len(projects)} case studies and {len(library["documents"])} documents.')
        return
    for file, output in outputs.items():
        write_if_changed(file, output)
    print(f'Built {len(projects)} case studies and {len(library["documents"])} documents.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true', help='Validate all references without writing outputs')
    args = parser.parse_args()
    try:
        build(args.root, args.check)
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        print(f'Build error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
