#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
INDEX=$ROOT/index.html

test -f "$ROOT/tellurion-mark.svg"
xmllint --noout "$ROOT/tellurion-mark.svg"
test "$(grep -c '<h3 class="project-title">Tellurion</h3>' "$INDEX")" -eq 1
grep -Fq 'src="tellurion-mark.svg" alt="Tellurion product mark"' "$INDEX"
grep -Fq 'https://github.com/ccancellieri/tellurion' "$INDEX"
grep -Fq 'independently created and owned by Carlo Cancellieri' "$INDEX"
grep -Fq 'Tellurion Cloud' "$INDEX"
grep -Fq 'service-level agreement' "$INDEX"
grep -Fq 'https://ccancellieri.github.io/tellurion/' "$INDEX"
grep -Fq 'https://ccancellieri.github.io/tellurion/proof/' "$INDEX"
grep -Fq 'href="https://ccancellieri.github.io/tellurion/releases/"' "$INDEX"
grep -Fq 'https://github.com/ccancellieri/tellurion/tree/main/demo/gallery' "$INDEX"
grep -Fq 'https://github.com/ccancellieri/tellurion/blob/main/demo/gallery/docs/articles/from-stac-discovery-to-a-live-map.md' "$INDEX"
grep -Fq 'href="https://tellurion-public-demo.onrender.com/ui/"' "$INDEX"
grep -Fq 'href="https://www.linkedin.com/feed/update/urn:li:activity:7505973347441328128/"' "$INDEX"
grep -Fq 'Watch the 90-second walkthrough' "$INDEX"
grep -Fq 'This edited walkthrough is not a performance benchmark' "$INDEX"
grep -Fq 'Monaco building footprints (GeoParquet)' "$INDEX"
grep -Fq 'Natural Earth coastline (ZIP Shapefile)' "$INDEX"
if grep -Fq 'href="https://github.com/ccancellieri/tellurion-demos/releases/tag/tellurion-v0.3.0"' "$INDEX"; then
    printf 'Retired binary release must not replace the current evaluator action.\n' >&2
    exit 1
fi
grep -Fq 'https://ccancellieri.github.io/tellurion/italy/' "$INDEX"
grep -Fq 'https://github.com/ccancellieri/tellurion/blob/main/demo/gallery/italy/evidence/BENCHMARK-REPORT.md' "$INDEX"
if grep -Eq 'https://(ccancellieri.github.io|github.com/ccancellieri)/tellurion-(demos|italy-demo)' "$INDEX" "$ROOT/README.md" "$ROOT/sitemap.xml"; then
    printf 'Active portfolio links must use the canonical Tellurion repository.\n' >&2
    exit 1
fi
grep -Fq 'Tellurion 0.2.0' "$INDEX"
grep -Fq 'Hosted timings are not benchmark evidence' "$INDEX"

printf 'Public evidence contract verified.\n'
