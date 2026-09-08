# PCNN variable vocabulary

Local and persistent identifiers for PCNN study variables.

- Persistent IRI pattern: `https://w3id.org/pcnn/var/{column_name}`
- Version: 0.1.0
- License for this encoding: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## What is in this repository

| File | Purpose |
|---|---|
| `variables.csv` | One row per PCNN column: local name, persistent IRI, definition, mapping |
| `valuesets.csv` | Shared answer lists |
| `vocabulary.ttl` | SKOS encoding |
| `docs/index.html` | Human-readable table for local testing and GitHub Pages |
| `docs/vocabulary.ttl` | Copy of the SKOS file for the website folder |

Item wording from DSQ, BPI, CIS20-R and COMPASS-31 remains copyright of the original authors. This repository publishes PCNN identifiers, short English labels, definitions written by the PCNN team, coded value lists needed to interpret PCNN data, and mappings.

## Test locally now

1. Open `docs/index.html` in a browser.
2. Open `variables.csv` in Excel or LibreOffice.
3. Optional: open `vocabulary.ttl` in a text editor.

You do not need GitHub Pages or w3id for this test. The persistent IRIs are already written in the files. They will start resolving on the web after you:

1. Put this folder in a public GitHub repository.
2. Enable GitHub Pages on the `docs/` folder.
3. Open a pull request to [w3id.org](https://github.com/perma-id/w3id.org) for the `pcnn/` path.

Until w3id is approved, keep the same IRIs in your data dictionary. Do not change them later.

## Mapping policy

- Every PCNN column has a PCNN IRI.
- `exactMatch` is used only when question, timeframe, scale and answer list are the same.
- `closeMatch` means the same topic with small differences.
- `relatedMatch` means a related concept only.
- An empty mapping is allowed when no suitable public item exists (common for DSQ-2 items).

Mappings do not replace the PCNN identifier.
