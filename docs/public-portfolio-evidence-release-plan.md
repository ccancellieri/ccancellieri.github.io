# Public portfolio evidence release implementation plan

**Goal:** Publish a coherent evidence-led portfolio in which the public Tellurion gallery is the product entry point, the Italy site is the bounded Rome field case, GitHub Pages is the canonical detailed portfolio, and Sites is the private executive overview.

**Architecture:** Stabilize the public evidence from the outside in. Fix and verify the live demo gallery first, publish the already-prepared Italy cross-links second, then update both portfolio surfaces from those verified URLs and claims. Each repository remains independently deployable and owns only its designated content.

**Technology:** Static HTML/CSS/JavaScript, POSIX shell contract tests, GitHub Pages, Render Blueprint services, Vinext/React for Sites.

## Global constraints

- Tellurion 0.2.0 is the only published Rome benchmark measurement.
- Tellurion 0.3.0 is the public distribution used by the live demo deployments.
- Newer engine work is not described as released or deployed behavior.
- Hosted Render timings are functional evidence, not benchmark or availability evidence.
- No direct email address, private career detail, credential, unpublished metric, or internal working reference enters a public diff.
- The legacy portfolio checkout remains unchanged.
- The existing cartographic visual identities are extended, not replaced.

## Task 1: Stabilize the public Tellurion gallery

**Files:**

- Modify: `tellurion-demos/demos/raster/index.html`
- Modify: `tellurion-demos/tests/render_raster_contract.sh`
- Verify: all files under `tellurion-demos/tests/`
- Update after merge: GitHub repository description for `ccancellieri/tellurion-demos`

**Produces:** A gallery with seven visible paths, no known dead action, a current repository summary, and passing deployment contracts.

- [ ] Add a failing raster contract assertion that requires a real PNG sample action and rejects the known `404` collection-metadata URL:

```sh
require_text demos/raster/index.html 'Open sample PNG tile'
require_text demos/raster/index.html '/tiles/WebMercatorQuad/13/3044/4380.png'

if grep -Fq '/collections/sample_landcover">Inspect tileset metadata' "$ROOT/demos/raster/index.html"; then
  printf 'raster viewer still links to the unsupported collection metadata route\n' >&2
  exit 1
fi
```

- [ ] Run `sh tests/render_raster_contract.sh` and confirm it fails on the missing sample action.
- [ ] Replace the unsupported raster metadata action with:

```html
<a class="button" href="https://tellurion-raster-demo.onrender.com/public/tiles/catalogs/default/collections/sample_landcover/tiles/WebMercatorQuad/13/3044/4380.png">Open sample PNG tile</a>
```

- [ ] Run every local contract:

```sh
sh tests/render_deployment_contract.sh
sh tests/render_raster_contract.sh
sh tests/render_zarr_contract.sh
sh tests/render_3d_contract.sh
sh tests/render_protocol_gallery_contract.sh
```

- [ ] Verify the static gallery and every URL in `.github/workflows/smoke.yml`, allowing for Render free-plan cold starts.
- [ ] Scan the staged diff for private information and internal working references, then commit the gallery fix.
- [ ] Push, open a pull request, wait for the repository checks, merge, and verify the GitHub Pages deployment.
- [ ] Update the repository description to: `Human-first demos of Tellurion serving vector, COG raster, Zarr, 3D Tiles, CQL2, STAC, Maps and Styles.`

## Task 2: Publish the Italy-to-gallery handoff

**Files:**

- Preserve prepared changes: `tellurion-italy-demo/README.md`
- Preserve prepared changes: `tellurion-italy-demo/index.html`
- Modify: `tellurion-italy-demo/tests/render_deployment_contract.sh`

**Consumes:** The verified gallery and public Tellurion 0.3.0 release URLs from Task 1.

**Produces:** A Rome case-study site that points visitors to the general gallery and uses `tellurion-demos` as the release-download home without changing the benchmark claim.

- [ ] Create an isolated branch from the remote default branch, leaving the existing local checkout and its prepared commit untouched.
- [ ] Add failing contract assertions:

```sh
require_text README.md 'https://ccancellieri.github.io/tellurion-demos/'
require_text README.md 'https://github.com/ccancellieri/tellurion-demos/releases/tag/tellurion-v0.3.0'
require_text index.html 'Explore all live demos'
require_text index.html 'https://github.com/ccancellieri/tellurion-demos/releases/download/tellurion-v0.3.0/SHA256SUMS'
```

- [ ] Run `sh tests/render_deployment_contract.sh` against the remote baseline and confirm the new assertions fail.
- [ ] Apply the existing prepared gallery-link commit to the isolated branch.
- [ ] Run the deployment contract again and confirm it passes.
- [ ] Verify that the page still calls the result a Tellurion 0.2.0 benchmark and the live/download path Tellurion 0.3.0.
- [ ] Verify the public Rome Features endpoint and the gallery endpoint.
- [ ] Scan, commit the contract update, push, open a pull request, merge after checks, and verify the GitHub Pages deployment.

## Task 3: Consolidate Tellurion in the canonical portfolio

**Files:**

- Create: `ccancellieri.github.io/tests/public_evidence_contract.sh`
- Modify: `ccancellieri.github.io/index.html`
- Modify: `ccancellieri.github.io/README.md`

**Consumes:** The live gallery, public release, and Italy URLs verified in Tasks 1 and 2.

**Produces:** One Tellurion project presentation with accessible public actions and no duplicate project card.

- [ ] Add a failing public-evidence contract:

```sh
#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
INDEX=$ROOT/index.html

test "$(grep -c '<h3 class="project-title">Tellurion</h3>' "$INDEX")" -eq 1
grep -Fq 'https://ccancellieri.github.io/tellurion-demos/' "$INDEX"
grep -Fq 'https://github.com/ccancellieri/tellurion-demos/releases/tag/tellurion-v0.3.0' "$INDEX"
grep -Fq 'https://ccancellieri.github.io/tellurion-italy-demo/' "$INDEX"
grep -Fq 'Tellurion 0.2.0' "$INDEX"
grep -Fq 'Hosted timings are not benchmark evidence' "$INDEX"
```

- [ ] Run the contract and confirm it fails because the page has two Tellurion cards and no general-gallery/release hierarchy.
- [ ] Remove the short duplicate Italy card.
- [ ] Update the remaining Tellurion card to lead with the seven-path public gallery, describe the four read-only services, and keep the Rome result boundary in the expanded evidence list.
- [ ] Use these public actions in this order:

```text
Explore live demos
Download Tellurion 0.3.0
Inspect the Rome field case
Read the benchmark report
```

- [ ] Update the About paragraph so the public gallery demonstrates vector, raster, multidimensional, 3D, CQL2, STAC, Maps, and Styles, while the Italy site owns the reproducible benchmark.
- [ ] Keep all three language dictionaries internally consistent with any changed hero copy.
- [ ] Update the README overview and file/section inventory to match the page.
- [ ] Run `sh tests/public_evidence_contract.sh`, parse `index.html` with a standard HTML parser, and run `git diff --check`.
- [ ] Scan the complete staged diff for private information and internal working references.
- [ ] Commit, push, open a pull request, merge after checks, and verify `https://ccancellieri.github.io/`.

## Task 4: Build the private executive Sites portfolio

**Files:**

- Create a dedicated Sites source directory with the standard Vinext starter.
- Modify: `app/page.tsx`
- Modify: `app/layout.tsx`
- Modify: `app/globals.css`
- Modify: `.openai/hosting.json`
- Create when validated: `public/og.png`

**Consumes:** Stabilized public copy and URLs from Tasks 1–3.

**Produces:** A privately deployed executive portfolio version in the existing Carlo Cancellieri Sites project.

- [ ] Initialize the standard Sites project once and retain its package manager, lockfile, and Cloudflare-compatible build structure.
- [ ] Store only the existing Sites project identifier in `.openai/hosting.json`; do not create another remote Sites project.
- [ ] Replace the starter with one responsive page containing:

```text
Hero: Open geospatial standards, turned into systems you can inspect and run.
Proof 1: Tellurion — seven public paths, four read-only services.
Proof 2: Rome field case — reproducible workload and bounded benchmark.
Proof 3: GeoServer to GeoID/DynaStore — standards through production architecture.
System map: Standards → Engine → Deployment → Evidence.
Actions: Explore demos, Read field case, Detailed portfolio, LinkedIn, GitHub, ORCID.
```

- [ ] Derive all colors and typography from the approved basalt, limestone, terrain-orange, and water-blue direction. Use one subtle coordinate-grid signature, visible focus states, and reduced-motion handling.
- [ ] Keep the page useful without client-side state; external links remain ordinary anchors.
- [ ] Generate one site-specific social preview after the headline and copy are final. Inspect its text; wire it only if accurate.
- [ ] Run the production build and fix any real build errors.
- [ ] Push the exact validated source, save one Sites version, deploy it privately, wait for success, and open the private URL for review.

## Task 5: Cross-surface verification and handoff

**Produces:** Four consistent surfaces with clear ownership and verified public actions.

- [ ] Check that the canonical portfolio, Tellurion gallery, and Italy case study link to one another without loops that obscure the primary action.
- [ ] Confirm that every public claim is backed by a live demo, public release, or reproducible report.
- [ ] Confirm that no page presents Render latency as performance evidence or the free service as a production SLA.
- [ ] Confirm that newer engine work is absent from 0.3.0 and deployment claims.
- [ ] Verify mobile layout, semantic headings, keyboard focus, contrast, metadata, and reduced motion on the changed pages.
- [ ] Report the three public URLs, the private Sites URL, the merged pull requests, the release/deployment checks, and any intentionally deferred history cleanup.
