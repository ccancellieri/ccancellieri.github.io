"""Acceptance checks for generated routes and the public reference boundary."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / 'scripts' / 'build_portfolio.py'


class PortfolioBuild(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'content/projects').mkdir(parents=True)
        (self.root / 'knowledge').mkdir()
        (self.root / 'knowledge/index.html').write_text('<!doctype html><html><body><main id="main-content">Engineering notebook</main></body></html>')
        if (REPO / 'templates').exists():
            shutil.copytree(REPO / 'templates', self.root / 'templates')
            (self.root / 'templates/home.html').write_text('<!doctype html><html><body>{{header}}<main id="main-content"><div id="home"></div><div id="about"></div><div id="projects">{{case_directory}}</div><div id="experience"></div><div id="contact"></div><div id="writing"></div><div id="latest-publications"></div>{{path_map}}</main></body></html>')
        for filename in ['portfolio.css', 'portfolio.js', 'portfolio-enhancements.js', 'writing-feed.mjs']:
            if (REPO / filename).exists():
                shutil.copy(REPO / filename, self.root / filename)
        self.site = {'site': {'url': 'https://portfolio.example', 'name': 'Sample Person', 'updated': '2026-10-13'}, 'paths': [{'id': 'architecture', 'title': 'Architecture', 'description': 'How systems fit.'}], 'homepageProjects': []}
        self.project = {'slug': 'sample-case', 'title': '<Systems & judgment>', 'description': 'A public case.', 'period': '2024', 'role': 'Developer', 'kind': 'independent', 'paths': ['architecture'], 'summary': 'A static summary.', 'sections': [{'id': section, 'title': section.title(), 'paragraphs': ['Read <this> & that.'], 'bullets': [], 'diagrams': []} for section in ['problem', 'architecture', 'decisions', 'outcomes', 'learning']], 'questions': [{'question': 'Why?', 'answer': 'A reason.', 'section': 'decisions'}], 'sources': [{'id': 'public', 'title': 'Documentation', 'url': 'https://example.org/docs/', 'verification': 'source-inspected'}], 'related': [], 'documents': []}
        self.library = {'documents': [], 'notes': []}
        (self.root / 'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://portfolio.example/legacy/</loc><lastmod>2020-01-01</lastmod></url></urlset>')

    def tearDown(self):
        self.temp.cleanup()

    def build(self, *args):
        (self.root / 'content/portfolio.json').write_text(json.dumps(self.site))
        (self.root / 'content/projects/sample-case.json').write_text(json.dumps(self.project))
        (self.root / 'content/library.json').write_text(json.dumps(self.library))
        self.assertTrue(SCRIPT.exists(), 'The portfolio generator is missing')
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), *args], text=True, capture_output=True)

    def test_static_case_has_escaped_text_seo_and_all_reading_sections(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / 'projects/sample-case/index.html').read_text()
        self.assertIn('&lt;Systems &amp; judgment&gt;', html)
        self.assertNotIn('<Systems & judgment>', html)
        self.assertIn('Read &lt;this&gt; &amp; that.', html)
        self.assertIn('rel="canonical" href="https://portfolio.example/projects/sample-case/"', html)
        self.assertIn('property="og:url" content="https://portfolio.example/projects/sample-case/"', html)
        self.assertIn('BreadcrumbList', html)
        self.assertIn('CreativeWork', html)
        for section in ['problem', 'architecture', 'decisions', 'outcomes', 'learning']:
            self.assertIn(f'id="{section}"', html)
        self.assertIn('A reason.', html)
        self.assertIn('https://example.org/docs/', html)
        self.assertIn('hidden data-presenter-controls', html)

    def test_build_preserves_legacy_sitemap_and_is_idempotent(self):
        self.assertEqual(self.build().returncode, 0)
        page = self.root / 'projects/sample-case/index.html'
        first = page.read_bytes(), page.stat().st_mtime_ns
        sitemap = (self.root / 'sitemap.xml').read_bytes()
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(first, (page.read_bytes(), page.stat().st_mtime_ns))
        self.assertEqual(sitemap, (self.root / 'sitemap.xml').read_bytes())
        self.assertIn(b'https://portfolio.example/legacy/', sitemap)
        self.assertIn(b'2020-01-01', sitemap)
        self.assertIn(b'https://portfolio.example/library/', sitemap)

    def test_asset_byte_changes_invalidate_urls_and_stable_rebuilds_are_idempotent(self):
        assets = {'portfolio.css', 'portfolio.js', 'portfolio-enhancements.js', 'writing-feed.mjs'}
        home = self.root / 'templates/home.html'
        references = ''.join(match[0] for match in re.finditer(r'<(?:link|script)\b[^>]*(?:href|src)="([^"]+)"[^>]*>(?:</script>)?', (REPO / 'templates/home.html').read_text()) if urlsplit(match[1]).path in assets)
        home.write_text(home.read_text().replace('</body>', references + '</body>'))
        pages = [self.root / 'index.html', self.root / 'projects/sample-case/index.html', self.root / 'library/index.html']

        def urls():
            result = {}
            for page in pages:
                result[page] = {urlsplit(value).path.lstrip('/'): value for value in re.findall(r'(?:href|src)="([^"]+)"', page.read_text()) if urlsplit(value).path.lstrip('/') in assets}
                expected = assets if page == pages[0] else assets - {'writing-feed.mjs'}
                self.assertEqual(set(result[page]), expected)
                for value in result[page].values():
                    self.assertTrue(parse_qs(urlsplit(value).query).get('v'), f'Missing cache version: {value}')
            return result

        self.assertEqual(self.build().returncode, 0)
        previous = urls()
        for asset in sorted(assets):
            with self.subTest(asset=asset):
                file = self.root / asset
                original = file.read_bytes()
                file.write_bytes(original + b'\n/* Cache invalidation probe. */\n')
                result = self.build()
                self.assertEqual(result.returncode, 0, result.stderr)
                current = urls()
                for page in pages:
                    for name, value in current[page].items():
                        self.assertEqual(urlsplit(value).path, urlsplit(previous[page][name]).path)
                        if name == asset:
                            self.assertNotEqual(value, previous[page][name])
                        else:
                            self.assertEqual(value, previous[page][name])
                outputs = pages + [self.root / 'sitemap.xml']
                snapshot = {page: (page.read_bytes(), page.stat().st_mtime_ns) for page in outputs}
                result = self.build()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(snapshot, {page: (page.read_bytes(), page.stat().st_mtime_ns) for page in outputs})
                file.write_bytes(original)
                result = self.build()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(previous, urls(), 'Restoring asset bytes must restore their URL versions')
        result = self.build('--check')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_revision_only_updates_sitemap_dates_for_changed_pages(self):
        self.assertEqual(self.build().returncode, 0)
        self.site['site']['updated'] = '2026-10-14'
        self.project['summary'] = 'An updated case summary.'
        self.assertEqual(self.build().returncode, 0)
        import xml.etree.ElementTree as ET
        tree = ET.parse(self.root / 'sitemap.xml')
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        dates = {u.findtext('s:loc', namespaces=ns): u.findtext('s:lastmod', namespaces=ns) for u in tree.getroot()}
        self.assertEqual(dates['https://portfolio.example/projects/sample-case/'], '2026-10-14')
        self.assertEqual(dates['https://portfolio.example/library/'], '2026-10-13')

    def test_strict_check_follows_generated_template_links_and_fragments(self):
        template = self.root / 'templates/page.html'
        template.write_text(template.read_text().replace('</main>', '<a href="/projects/sample-case/#missing-section">Broken section</a></main>'))
        result = self.build('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing-section', result.stderr)
        self.assertFalse((self.root / 'projects/sample-case/index.html').exists())

    def test_strict_check_can_validate_routes_before_the_first_build(self):
        result = self.build('--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'projects/sample-case/index.html').exists())

    def test_path_reset_keeps_a_visible_descriptive_mobile_label(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        from html.parser import HTMLParser
        class ResetButton(HTMLParser):
            attributes = None
            def handle_starttag(self, tag, attrs):
                if tag == 'button' and 'data-path-reset' in dict(attrs):
                    self.attributes = dict(attrs)
        parser = ResetButton()
        parser.feed((self.root / 'index.html').read_text())
        self.assertIsNotNone(parser.attributes)
        self.assertNotIn('control-button', parser.attributes.get('class', '').split(), 'The generic control-button mobile rule hides text and adds a theme icon')
        self.assertIn('Show all connections', (self.root / 'index.html').read_text())

    def test_unsafe_slug_cannot_write_outside_projects(self):
        self.project['slug'] = '../escape'
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('slug', result.stderr)
        self.assertFalse((self.root / 'escape/index.html').exists())

    def test_source_url_cannot_execute_script(self):
        for url in ['javascript:alert(1)', 'file:///private/source.pdf', 'https://user:password@example.org/', '/Users/private/source.pdf', '//example.org/file']:
            self.project['sources'][0]['url'] = url
            result = self.build()
            self.assertNotEqual(result.returncode, 0, url)
            self.assertIn('public URL', result.stderr)

    def test_strict_check_catches_missing_diagram_without_writing_pages(self):
        self.project['sections'][1]['diagrams'] = [{'src': '/assets/diagrams/missing.svg', 'title': 'Context', 'description': 'The context.', 'view': 'Context'}]
        result = self.build('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing.svg', result.stderr)
        self.assertFalse((self.root / 'projects/sample-case/index.html').exists())

    def test_embedded_svg_styles_and_ids_are_scoped_to_the_diagram(self):
        assets = self.root / 'assets/diagrams'
        assets.mkdir(parents=True)
        (assets / 'context.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 700" aria-labelledby="title"><title id="title">Context</title><style>text{fill:red}.label{font-size:18px}</style><text class="label">A readable label</text></svg>')
        self.project['sections'][1]['diagrams'] = [{'src': '/assets/diagrams/context.svg', 'title': 'Context', 'description': 'A text equivalent.', 'view': 'Context'}]
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / 'projects/sample-case/index.html').read_text()
        self.assertIn('id="context-root"', html)
        self.assertIn('#context-root text{fill:red}', html)
        self.assertIn('aria-labelledby="context-title"', html)
        self.assertIn('A text equivalent.', html)

    def test_embedded_svg_cannot_load_remote_styles(self):
        assets = self.root / 'assets/diagrams'
        assets.mkdir(parents=True)
        (assets / 'unsafe.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><style>@import "https://tracking.example/style.css";</style></svg>')
        self.project['sections'][1]['diagrams'] = [{'src': '/assets/diagrams/unsafe.svg', 'title': 'Context', 'description': 'Unsafe source.', 'view': 'Context'}]
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SVG style', result.stderr)

    def test_library_separates_recent_publications_from_selected_notes(self):
        self.library['selected_notes'] = [{'title': 'A <selected> note', 'url': 'https://example.org/notes/', 'description': 'An engineering decision & its evidence.'}]
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / 'library/index.html').read_text()
        self.assertIn('<h2>Recent publications</h2>', html)
        self.assertIn('href="/#latest-publications"', html)
        self.assertIn('automatically', html)
        self.assertIn('<h2>Selected engineering notes</h2>', html)
        self.assertIn('href="https://example.org/notes/"', html)
        self.assertIn('A &lt;selected&gt; note', html)
        self.assertIn('An engineering decision &amp; its evidence.', html)

    def test_library_notes_fall_back_to_existing_homepage_selection(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / 'library/index.html').read_text()
        self.assertIn('<h2>Selected engineering notes</h2>', html)
        self.assertIn('href="/#writing"', html)

    def test_library_rejects_uninspected_downloads(self):
        self.library['documents'] = [{'id': 'unknown', 'title': 'Unchecked', 'description': 'Unknown origin.', 'type': 'Thesis', 'year': '2024', 'url': 'https://example.org/document.pdf', 'verification': 'unverified'}]
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('verification', result.stderr)
        self.assertFalse((self.root / 'library/index.html').exists())

    def test_strict_check_rejects_missing_local_source(self):
        self.project['sources'][0]['url'] = '/assets/documents/missing.pdf'
        result = self.build('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing.pdf', result.stderr)

    def test_library_publishes_only_verified_documents_and_text(self):
        self.library['documents'] = [{'id': 'document', 'title': 'Thesis', 'description': 'A readable document.', 'type': 'Thesis', 'year': '2024', 'url': 'https://example.org/thesis.pdf', 'attribution': 'Author', 'verification': 'document-inspected', 'project': 'sample-case'}]
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / 'library/index.html').read_text()
        self.assertIn('https://example.org/thesis.pdf', html)
        self.assertIn('A readable document.', html)
        self.assertIn('/projects/sample-case/', html)


if __name__ == '__main__':
    unittest.main()
