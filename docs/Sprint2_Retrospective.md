# Sprint 2 Retrospective

## Formula decisions
- Capex intensity is derived as abs(investing_activity) / sales * 100.
- Free cash flow conversion is calculated as free cash flow / operating profit * 100.
- Capital allocation patterns are based on the sign pattern of CFO, CFI, and CFF.

## Edge cases handled
- Missing or zero denominators return None rather than raising errors.
- Negative equity is treated as non-computable for ROE and debt-to-equity.
- Turnaround and negative-based CAGR cases are surfaced as None or flagged in the logs.

## Bank carve-outs
- Debt and interest coverage warnings are suppressed for financial-sector companies.

## Debt-free companies
- Debt-free companies are treated as having a neutral leverage profile and do not generate leverage warnings.

## Negative equity
- Negative equity results in a missing ROE instead of an invalid numeric value.

## Turnaround CAGR
- Turnaround CAGR is handled as a non-computable case and left as None.

## Known source data anomalies
- Some companies show unusually high or low ratio values due to temporary accounting effects, which are logged for manual review.

## Validation summary
- Missing values are reported as errors.
- Extreme values are logged as warnings.
- Bank-related leverage and interest coverage are intentionally suppressed.

## Test summary
- Existing KPI and screener tests continue to pass.
- New Sprint 2 regression tests validate the KPI helpers, manual utility, and verification script.
