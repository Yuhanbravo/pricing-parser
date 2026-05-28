# Accounting Subjects Extraction Notes

## Extraction Scope

Round 5A only extracts a first-pass reference set centered on subject families that already matter to the current valuation-table parser surface:

- cash and settlement: 1002, 1021, 1031, 3003
- ordinary investment assets: 1102, 1103, 1104, 1105, 1202, 1203
- fees and liabilities: 2203, 2206, 2207, 2208, 2221
- fund capital and retained result: 4001, undistributed profit
- derivative indexing: 3102 plus Chapter 5 derivative language in the practice manual

## Extraction Method

- Reused the already-converted Markdown working copies from 任务书集合 and copied them into the formal Round 5A delivery path.
- Used exact subject-code and keyword lookups to avoid inventing unsupported rows.
- Normalized only the fields needed for the first-pass reference CSVs.
- Left unresolved or ambiguous rows in review queues instead of forcing full normalization.

## Known Quality Notes

### 中国基金估值标准 2018

- Page markers and repeated headers remain in the Markdown.
- Some OCR spacing and punctuation are inconsistent.
- Some subject names appear with OCR noise, for example stray punctuation around codes or section numbers.

### 证券投资基金会计核算操作实务手册-20240530

- Table rows sometimes wrap across lines.
- A few cells keep extra spaces caused by conversion.
- Derivative examples are clear enough for indexing, but not sufficient on their own for full OTC lookthrough implementation.

## Why Review Queues Are Preserved

The official sources are useful for standardization, but they do not remove the need for product-side business judgment. The repository therefore keeps explicit review surfaces for:

- raw subject patterns that may map to multiple standard subjects
- standard subjects that should not become ordinary positions
- derivative-related entries that belong to a later independent subsystem
