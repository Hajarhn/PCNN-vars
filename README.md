# PCNN variable vocabulary

Persistent identifiers for PCNN study variables.

- IRI pattern: `https://w3id.org/pcnn/var/{column_name}`
- Version: 0.1.0
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Upload only these files to GitHub

Put them in the **root** of `PCNN-vars` (not inside another `pcnn-vars/` folder):

```
README.md
LICENSE
CITATION.cff
codebook.csv
variables.csv
valuesets.csv
vocabulary.ttl
collections.ttl
docs/index.html
docs/vocabulary.ttl
```

Do **not** upload `.grok`, `node_modules`, `src`, `server`, or the Grok app zip.

Then: Settings → Pages → Deploy from branch → `/docs`.

The public HTML is `docs/index.html`.

## Mapping policy

- Every column has a PCNN IRI.
- `exactMatch` only when question, timeframe, scale and answers are the same.
- `closeMatch` = same topic, small differences (wording, extra answer).
- `relatedMatch` = related concept only (e.g. SNOMED headache vs DSQ frequency item).
- Empty mapping is allowed.

Mappings do not replace the PCNN identifier.

Item wording from DSQ, BPI, CIS20-R and COMPASS-31 remains copyright of the original authors.
