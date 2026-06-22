# pricing-parser-rc1-sample-intake-planning-001

## Objective

Receive the sanitized RC1 handoff subset prepared by `Pricing_sheet` into local ignored staging and record the owner decisions needed before any parser-side sample baseline work begins.

This is an intake planning task only. It does not change parser runtime behavior, parser adapters, expected outputs, or comparison workflows.

## Source Materials

Source handoff package:

`D:\dev\Pricing_sheet\output\parser_handoff\pricing-parser-rc1-intake-001`

The source package comes from the `Pricing_sheet` sanitized sample library. `Pricing_sheet` itself is not under review in this task. This task only receives already-sanitized handoff materials.

Source files staged locally:

- `README.md`
- `LOCAL_SELECTION.md`
- `selected_sample_manifest.csv`
- `source_rc1_manifest_excerpt.csv`
- `sample_coverage_summary.md`
- `evidence_index_excerpt.csv`
- `workbooks/`

## Local Ignored Sample Staging

Local staging path:

`data_samples/local_rc1/pricing-parser-rc1-intake-001/`

The staging directory is intentionally ignored by Git. Workbooks in this directory are for local intake planning and owner review only. They are not parser fixtures, not expected baselines, and not committed sample assets.

## Selected RC1 Samples

The received subset contains 8 sanitized workbooks.

Coverage summary from the handoff manifest:

- Scenarios: `month_end`, `normal_day`, `quarter_end`, `special_day`
- Workbook extensions: `.xls`, `.xlsx`
- Adapter keys: `UNKNOWN`, `citic`, `gt_haitong`, `guoxin`, `orient`, `xingye`
- `UNKNOWN` adapter-key count: 1, retained only as a gap-analysis case

Known intake note: the handoff preserves RC1 manifest fields as provided by `Pricing_sheet`; parser-side baseline work should decide whether it keys extension semantics from manifest metadata or actual staged workbook filenames.

## Current Non-goals

- Do not modify parser runtime.
- Do not add or change adapters.
- Do not import the full RC1 library into tracked baseline.
- Do not generate parser expected output.
- Do not refresh `data_samples/expected/`.
- Do not establish a parser comparison workflow.
- Do not commit staged workbooks.
- Do not commit raw workbooks.
- Do not commit controlled identity-map exports.
- Do not infer real product or custodian identities.
- Do not change existing R1-P2 owner decisions.

## Boundary Rules

- The staged RC1 materials are sanitized handoff inputs only.
- Workbooks must remain under `data_samples/local_rc1/` unless a future owner-approved task explicitly imports selected fixtures.
- Current R1 work must not broaden expected baselines just because RC1 materials are available locally.
- R1-P2 remains focused on workbook-to-CSV consistency regression for the existing controlled baseline.
- Formal adapter baseline and expected-baseline work should be deferred to R3 unless the owner explicitly changes the roadmap order.

## Owner Decision Checklist

- [ ] Allow selected RC1 samples to enter a parser baseline?
- [ ] Decide the first baseline sample count.
- [ ] Restrict first baseline samples to known `adapter_key` rows only?
- [ ] Allow the one `UNKNOWN` adapter-key sample as a gap-analysis case?
- [ ] Allow parser expected output generation for selected RC1 samples?
- [ ] Identify who confirms expected baselines.
- [ ] Require a separate PR for sample import?
- [ ] Commit sanitized workbooks to Git, or keep them local ignored only?
- [ ] Create a dedicated test group for `special_day` samples?
- [ ] Require R1-P2 completion before starting R3 sample baseline work?

## Recommended R3 Follow-up

Recommended later task name:

`pricing-parser-sample-adapter-baseline-001`

That task should decide which sanitized samples graduate from local staging into a tracked parser baseline, what expected outputs are generated, who approves those outputs, and which adapter or routing gaps become implementation work.

## Validation

Suggested validation for this planning task:

```powershell
git status --short
git diff --stat
git diff --check
git check-ignore -v data_samples/local_rc1/pricing-parser-rc1-intake-001/README.md
git check-ignore -v data_samples/local_rc1/pricing-parser-rc1-intake-001/workbooks/<one-staged-workbook>
git diff -- . ':!data_samples/local_rc1' | Select-String -Pattern "D:\\BaiduSyncdisk|产品全称|托管机构全称|source_path|expected output|comparison workflow" -CaseSensitive:$false
```

Expected result: local staging is ignored, tracked changes are limited to `.gitignore`, task/status/roadmap docs, and no parser runtime, tests, expected baseline, or comparison workflow changes are present.
