# Carlo Cancellieri — Personal Portfolio

A public, evidence-led portfolio of software engineering, architecture,
DevOps, cloud and geospatial work, open-source contributions and international
collaboration. The homepage presents Carlo's career; Tellurion has its own
[project site](https://ccancellieri.github.io/tellurion/).

Live portfolio: [ccancellieri.github.io](https://ccancellieri.github.io/).

## Content

- Professional introduction and technical foundations, including Linux since
  1997 and development across Linux, macOS and Windows. Early computing
  experience is kept separate from professional employment dates.
- Selected work spanning FAO platforms, GeoServer, OPeNDAP, independent
  Tellurion development and MCP Skill Hub research.
- Career and team context, education, selected writing and engineering
  principles grounded in concrete work.
- Public professional links, with institutional work distinguished from
  independent projects. The portfolio does not imply institutional endorsement.

Project descriptions identify Carlo's role and distinguish demonstrated
results, proposed standards and intended capacity. Private employment records,
contact details, client data and unpublished internal materials do not belong
in this repository. Historical articles are dated sources, not automatic proof
of current capability, availability or operational scale.

## Website

Static HTML, CSS and JavaScript, with a Python standard-library generator and no framework. English is the
supported content language. Visitor theme preferences are optional; content
and navigation remain available without JavaScript or browser storage.

- `templates/home.html`: homepage source; preserve existing projects, evidence and section anchors.
- `content/portfolio.json`: six paths, homepage project mappings and site metadata.
- `content/projects/*.json`: case-study text, source URLs and diagram references.
- `content/library.json`: inspected public documents and source notes.
- `scripts/build_portfolio.py`: deterministic generation of the homepage, case studies, library and sitemap.
- `index.html`: generated public content and search/social metadata.
- `knowledge/`: a connected engineering notebook with seven public-source notes,
  three thematic indexes and reciprocal related links; readable without JavaScript.
- `projects/<slug>/index.html` and `library/index.html`: generated static reading pages.
- `portfolio.css`: responsive personal-brand presentation.
- `portfolio.js`: theme preferences, mobile navigation and deep-link focus.
- `portfolio-enhancements.js`: path highlighting, five-section presentations and scrollable diagram zoom.
- `social-card.svg` and `og-personal.png`: editable sharing graphic and its
  1200 × 630 PNG rendition.
- `sitemap.xml`, `robots.txt`, `404.html`: discovery and route recovery.
- `tests/`: navigation, metadata, content and historical-demo regression checks.

To rebuild after editing the source content or templates:

```sh
python3 scripts/build_portfolio.py
python3 scripts/build_portfolio.py --check
```

The build writes only changed files. `--check` validates strict references without
writing output. During an incomplete content edit, normal builds can render
missing diagram references; run the strict check before publishing. Public
sources must use HTTPS or public root-relative routes. Text is HTML-escaped and
SVG diagrams are checked before embedding. Sitemap entries for historical routes
are retained; the configured revision date applies to changed generated pages.

The homepage retains all projects and offers six connected paths. Selecting a
path highlights matching work while keeping every project visible. Case studies
have five reading sections, source context, questions and related documents.
All content and ordinary links work without JavaScript. With JavaScript, use
“Present this case”, the Previous/Next buttons or arrow/Page keys, Home/End and
Escape. Exit restores the reading page and focus. Printing includes all sections.
Diagram views remain ordinary anchor links; zoom and flow emphasis are optional.
On narrow screens diagrams scroll horizontally to keep labels readable, and a
full-size SVG link is always available.

To preview locally from this directory:

```sh
python3 -m http.server 8767 --bind 127.0.0.1
```

Open [localhost:8767](http://127.0.0.1:8767/).

## Verification

```sh
python3 scripts/build_portfolio.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs tests/*.test.mjs
sh tests/public_evidence_contract.sh
git diff --check
```

Also check the rendered page at desktop and narrow mobile widths, keyboard
menu/focus behavior, both themes, direct section links and content without
JavaScript. External sources and free hosted demos can change independently;
a passing local regression does not establish their availability.

## Tellurion evidence and historical links

The [canonical gallery](https://ccancellieri.github.io/tellurion/),
[proof brief](https://ccancellieri.github.io/tellurion/proof/),
[version index](https://ccancellieri.github.io/tellurion/releases/) and
[source](https://github.com/ccancellieri/tellurion/tree/main/demo/gallery)
remain separate from the personal homepage. The public evaluator is temporary
and is not a managed cloud service or a production service-level agreement.
Historical viewers preserve dated evidence, not guaranteed backend uptime.

Legacy demo directories and `legacy-tellurion-redirect.js` preserve existing
shared URLs, including queries and fragments. Do not remove them during
personal-portfolio updates. The standalone Planner privacy policy is retained.

## Publishing

Review the preview and public-safe copy before publishing through the existing
GitHub Pages configuration. Keep the selected publishing source unchanged and
verify the live homepage, social metadata and old demo links after deployment.

Public profiles: [LinkedIn](https://www.linkedin.com/in/ccancellieri/),
[GitHub](https://github.com/ccancellieri),
[ORCID](https://orcid.org/0009-0006-4092-4234),
[WordPress](https://ccancellieri.wordpress.com/) and
[X](https://x.com/cancellieric).
