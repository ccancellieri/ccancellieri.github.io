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

printf 'Public evidence contract verified.\n'
