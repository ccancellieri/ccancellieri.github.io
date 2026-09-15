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
grep -Fq 'https://ccancellieri.github.io/tellurion-demos/' "$INDEX"
grep -Fq 'https://ccancellieri.github.io/tellurion-demos/proof/' "$INDEX"
grep -Fq 'href="https://tellurion-public-demo.onrender.com/ui/"' "$INDEX"
if grep -Fq 'href="https://github.com/ccancellieri/tellurion-demos/releases/tag/tellurion-v0.3.0"' "$INDEX"; then
    printf 'Retired binary release must not replace the current evaluator action.\n' >&2
    exit 1
fi
grep -Fq 'https://ccancellieri.github.io/tellurion-italy-demo/' "$INDEX"
grep -Fq 'Tellurion 0.2.0' "$INDEX"
grep -Fq 'Hosted timings are not benchmark evidence' "$INDEX"

printf 'Public evidence contract verified.\n'
