# Official Reference Reusable Assets

## What Round 5A Adds

Round 5A turns the official materials into repository assets that can be reused in later rounds without rereading the raw sources from scratch.

## Asset Types

### Source assets

- original PDF or DOCX files preserved under `docs/reference/source/`
- committed for traceability and later manual review

### Reviewable Markdown assets

- full-text Markdown copies under `docs/reference/markdown/`
- optimized for AI reading, keyword lookup, and section navigation

### Structured accounting reference assets

- raw extraction table
- normalized standard-subject table
- mapping review queue
- standard-subject to taxonomy design table

### OTC derivative design assets

- chapter index and pattern table
- field dictionary
- review-rule candidates
- design documents for later subsystem work

## Intended Reuse By Later Rounds

### Round 5B

- reuse normalized accounting subjects as the draft mapping backbone
- add runtime-field proposal without revisiting raw OCR work
- consume mapping review queue as the first unresolved-item list

### Round 5C

- reuse derivative chapter indexing and field dictionary to define contract and exposure schemas
- reuse review-rule candidates as the initial derivative queue criteria

### Round 5D

- reuse derivative subject patterns to detect contract candidates inside valuation-table subjects
- keep incomplete contract records in review instead of forcing lookthrough

## Non-reuse Boundary

These assets are not executable parser configuration in Round 5A. They remain reference and planning inputs until a later round explicitly wires them into runtime behavior.
