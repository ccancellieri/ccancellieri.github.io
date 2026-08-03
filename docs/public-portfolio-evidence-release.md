# Public portfolio evidence release

## Purpose

Create a coherent public presence in which each surface has one job:

- the Carlo Cancellieri Sites project gives decision-makers a fast executive overview;
- `ccancellieri.github.io` remains the canonical detailed portfolio;
- Tellurion demos provides the primary public, interactive product evidence;
- Tellurion Italy remains the reproducible Rome field case and benchmark record;
- the legacy portfolio checkout remains a private reference and is not a deployment source.

The release should help a technical leader, collaborator, or recruiter understand the differentiator in under 30 seconds: Carlo turns open geospatial standards into systems that can be operated, inspected, and kept under local control.

## Release scope

### Executive Sites portfolio

Build a private, single-page executive portfolio for the existing Carlo Cancellieri Sites project. It should contain:

1. A direct positioning statement: open geospatial systems architect and creator of Tellurion.
2. Three evidence-led proof points:
   - the live Tellurion capability gallery, spanning seven visible paths over four read-only deployments;
   - the reproducible Rome field test, with its benchmark boundary stated next to the result;
   - GeoServer core development and standards-to-production platform experience.
3. A short systems map connecting standards, product engineering, and operations.
4. Clear links to the detailed portfolio, GitHub, LinkedIn, ORCID, the Tellurion gallery, release downloads, and the Italy evidence site.

The first deployment remains private. Public access is a separate decision after review.

### Canonical GitHub Pages portfolio

Keep the existing single-page architecture and earth-toned identity. Improve the first viewport and Tellurion project content so that:

- the main statement names the practical outcome, not only the role;
- the primary Tellurion action opens the public live gallery rather than a source repository that visitors cannot access;
- the Tellurion summary reflects the current breadth of vector, raster, multidimensional, 3D, filtering, catalog, maps, and styles work without presenting every route as a separate product;
- the Italy benchmark is presented with its scope and caveat beside the number;
- project links distinguish live demos, release downloads, and field-test evidence;
- repeated or conflicting Tellurion cards are consolidated.

No historical career claims or private contact details are reintroduced.

### Tellurion demos gallery

Treat `tellurion-demos` as the public product-demonstration hub. Its GitHub Pages site presents seven human-facing paths:

- vector features and MVT;
- COG raster tiles;
- fixed Zarr slices;
- 3D Tiles 1.1;
- bounded CQL2 text queries;
- STAC collection and item projections;
- server-rendered Maps with a named, read-only style.

Those pages are backed by four read-only Render services in Frankfurt: vector, raster, Zarr, and 3D. The services use the published Tellurion 0.3.0 distribution, accept Render's dynamic port, run without write routes, and may sleep on the free plan. Hosted response times are functional evidence only and are never benchmark claims.

The gallery owns public release downloads and the cross-capability narrative. Before it is promoted from the portfolios:

- retain the boundary text for every synthetic or deliberately limited fixture;
- keep the daily public-endpoint smoke test visible;
- correct any human-facing link that does not resolve even when the underlying capability is live;
- update repository summary text that still describes only the original four data lanes;
- verify the release manifest and all four deployed services.

### Tellurion Italy field case

Preserve Tellurion Italy as a focused, reproducible case study rather than the general product landing page. Its public Rome service and static evidence remain useful for one inspectable OSM and ESA WorldCover workflow.

The published performance result remains a Tellurion 0.2.0 measurement. The live Rome service and public downloads use Tellurion 0.3.0, but they do not retroactively change that benchmark. The site must distinguish:

- published release capabilities;
- live functional deployment evidence;
- current engine work that has not been released or deployed publicly;
- future measurements that have not yet been run.

The Italy site should link prominently to the general Tellurion demos gallery, retain its own test kit and benchmark evidence, and link back to the canonical portfolio. The generic gallery becomes the release-download home; the Italy repository remains the owner of the Rome dataset, reproduction steps, and benchmark artifacts.

### Verified Tellurion deployment snapshot

The release design is based on the deployment verified on 2026-08-03:

- `https://ccancellieri.github.io/tellurion-demos/` serves the public gallery;
- the vector, Zarr, and 3D Render service roots or resources respond successfully;
- the raster service returns its expected PNG tile even though the current viewer's tileset-metadata link returns `404` and must be corrected;
- the Rome Features service used by Tellurion Italy responds successfully;
- the latest public smoke workflow completed successfully against the seven gallery paths and their backing endpoints;
- Tellurion 0.3.0 release assets and their SHA-256 manifest are published from `tellurion-demos` for macOS Apple Silicon, Linux x86_64, and Windows x86_64.

The engine continues to advance beyond the public 0.3.0 distribution. Portfolio copy must therefore use the deployed gallery and published release as public evidence, and must not describe newer main-branch work as part of 0.3.0 or as deployed behavior.

## Content hierarchy

Every public surface uses the same claim structure:

1. **Claim** — a short statement a visitor can understand quickly.
2. **Boundary** — what was and was not demonstrated.
3. **Evidence** — a direct link to a live demo, a public release, or a reproducible report.
4. **Next action** — inspect, reproduce, download, or discuss.

Measured results never appear without their test boundary. Work completed after Tellurion 0.3.0 is not used as public evidence until it has an accessible artifact, deployment, or report. A live endpoint proves function, not throughput, production capacity, or availability.

## Visual direction

Extend the existing cartographic identity rather than redesigning every surface:

- basalt and limestone neutrals;
- restrained terrain orange for action and emphasis;
- water blue for evidence and external links;
- a subtle topographic or coordinate-grid motif as the single signature element;
- characterful display typography paired with highly legible body text;
- square or lightly rounded geometry, avoiding a wall of interchangeable cards.

Motion is limited to one purposeful entrance sequence and small interaction feedback. Reduced-motion preferences are respected.

## Information ownership

`ccancellieri.github.io` is the public source of truth for biography, career history, and detailed project descriptions. Tellurion demos owns the capability gallery, public distribution links, Render deployment definitions, and live smoke checks. Tellurion Italy owns the Rome dataset, reproduction workflow, benchmark methodology, and field-test evidence. The Sites portfolio contains concise summaries and links back to those sources; it does not become another detailed content store.

The legacy portfolio checkout remains untouched during this release. Any history rewrite or retirement is handled separately because it changes repository history.

## Failure and safety behavior

- Every external link must remain useful if JavaScript is disabled.
- A sleeping Render service must produce a clear cold-start state and a retry path in its viewer.
- A failed live service must not erase the page's evidence boundary, reproduction link, or raw endpoint link.
- Missing optional imagery must not hide claims or calls to action.
- The Sites page must render a complete static first view while enhanced behavior loads.
- No direct email address, employment-internal detail, private note, credential, or unpublished operational metric may be added.
- If a generated social image contains incorrect text, omit it rather than publishing misleading content.

## Verification

Before publication:

- validate the Sites production build;
- validate HTML structure and metadata on all static sites;
- verify internal and external links;
- check mobile layout, keyboard focus, semantic headings, contrast, and reduced motion;
- scan the complete public diff for private information and internal working references;
- confirm each factual claim against its linked public source;
- confirm the Tellurion 0.2.0 benchmark, 0.3.0 release, live deployment, and newer engine work remain explicitly separated;
- run every `tellurion-demos` deployment contract and verify every endpoint in its public smoke matrix;
- verify the corrected raster viewer action against a real `200` response.

## Delivery order

1. Correct and verify the public Tellurion demos gallery, deployment links, and repository summary.
2. Publish the pending Tellurion Italy links that make the general gallery the product hub while preserving the Rome field case.
3. Improve and publish the canonical GitHub Pages portfolio using the verified public Tellurion evidence.
4. Build and privately deploy the executive Sites portfolio using the stabilized copy and links.
5. Review the private Sites result before any public-access change.

## Acceptance criteria

- A first-time visitor can identify Carlo's role, Tellurion, and the evidence path from the first viewport.
- The primary Tellurion call to action opens the public capability gallery.
- The gallery presents seven visible paths backed by four read-only Render services and preserves each path's evidence boundary.
- The raster viewer contains no known dead action.
- Public 0.3.0 claims are limited to the published distribution and deployed demo configuration.
- The Rome benchmark number is never separated from its limited test boundary.
- The portfolio, general gallery, and Italy field case have distinct roles and consistent facts.
- The canonical portfolio, general gallery, and Italy field case are public and updated.
- The Sites portfolio is deployed privately and ready for review.
- The legacy portfolio checkout is unchanged.
