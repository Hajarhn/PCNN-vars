# PCNN variable vocabulary

A SKOS vocabulary of **study variables** for the PCNN post-COVID research
codebook. It is a register of codebook columns, not a subject taxonomy.

Each column has one persistent identifier:

```
https://w3id.org/pcnn/var/{variable_name_CBS}
```

Version **0.3.2** · **636** variables · **382** with a SKOS match so far.

Creator: [Hajar Hasannejadasl](https://orcid.org/0000-0001-5262-7399)  
Publisher: PCNN study  
Created: 2026-09-08 · Modified: 2026-09-09

The w3id prefix is **minted in these files but not yet registered**, so
`https://w3id.org/pcnn/...` currently 404s in a browser. GitHub Pages can
already serve the human catalogue and `vocabulary.ttl`.

## Why this exists

Column names (`smokingstatus`, `HI7`, …) are not enough for reuse across
sites. The IRI stays stable even if the spreadsheet header changes later.
SKOS matches (`exactMatch` / `closeMatch` / `relatedMatch`) to LOINC,
SNOMED CT or NCIt are annotations. They do not replace the PCNN identifier.

Machine-readable file: [`vocabulary.ttl`](public/vocabulary.ttl)  
Licence notice: [`LICENSE`](LICENSE)

## IRI rules

| Keep | Change later if needed |
| --- | --- |
| The PCNN IRI after it is used in a dataset | SKOS matches, labels, value-set tables, theme |

One codebook column = one IRI, even when two questions look similar
(for example DSQ fatigue vs CIS fatigue). Link them; do not merge them.

`variable_name_CBS` is the column name used to harmonise PCNN datasets.
The IRI is based on that name.

## SKOS matches

The field name on every variable is **SKOS match**.

- **exactMatch** — same question, timeframe, scale and answer list (used for official PROMIS, PHQ-8, PSQI and BPI items encoded in LOINC/NCIt)
- **closeMatch** — same topic, small differences
- **relatedMatch** — related concept only (typical for a SNOMED finding vs a questionnaire item)
- empty (`—`) — no public item yet; the local IRI is enough

Matches may be filled or revised without minting a new IRI.

## Value sets

Identical answer lists share one `vs-…` identifier (DDI / SKOS code-list
pattern). The catalogue lists shared lists once; each variable links to
its list instead of repeating the table.

## Files

| File | Role |
| --- | --- |
| `LICENSE` | What CC BY 4.0 covers — and what it does not |
| `public/vocabulary.ttl` | SKOS RDF |
| `public/codebook.json` | Source used to generate the catalogue |
| GitHub Pages `docs/index.html` | Human catalogue |

## Licence

**PCNN encoding** (IRIs, Turtle, `variable_name_CBS`, labels and mappings
created by the PCNN team) is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

This does **not** license third-party questionnaires (DSQ, PROMIS, BPI,
CIS20-R, COMPASS-31, PHQ-8, PSQI, SF-36, and others). Their wording,
scoring and layout stay with the original authors. SKOS matches point at
LOINC / SNOMED CT / NCIt under those resources’ own terms.

See [`LICENSE`](LICENSE) for the full notice, no-warranty clause, and
preferred citation.

## Citation

Hasannejadasl, H. (2026). PCNN variable vocabulary. https://w3id.org/pcnn
