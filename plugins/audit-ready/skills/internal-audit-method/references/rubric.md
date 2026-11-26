# Evidence rubric

Check each evidence file against the requirement it is filed for. Record every failed check in `gaps`.

| # | Check | Pass when | Typical failure |
|---|---|---|---|
| 1 | **Relevant** | The file shows the specific control the requirement asks for | An MFA policy filed for an access review requirement |
| 2 | **System coverage** | It covers every in-scope system named in `scope.md` (all production accounts, repos and tenants) | One AWS account of three, or one repo of five production repos |
| 3 | **Period coverage** | Point-in-time evidence is dated inside the audit period, ideally recent. Population evidence covers the whole period | A screenshot from before the period; a leaver list for 3 of 6 months |
| 4 | **Complete** | Unfiltered, or the filter is stated and justified. Screenshots show the URL and the date | A cropped screenshot; an export filtered to one team |
| 5 | **Authentic** | There's an `index.csv` row with a sha256 that matches the file. CLI evidence records the exact command. Owner evidence records its original name | No index row; a hash mismatch; a hand-edited CSV |
| 6 | **Approved and current** (policies, plans, reviews) | Shows an approver, approval date, version, and a review within the last 12 months | Draft watermark; last reviewed 2 years ago |
| 7 | **Effective** | The content shows the control working, not just existing | The policy exists but the export shows 5 users without MFA |
| 8 | **Consistent** | Doesn't contradict other evidence | The HR leaver list has someone still active in the IdP export |

Verdict mapping:
- **`satisfies`:** every applicable check passes.
- **`partial`:** checks 1 and 5 pass, but one or more of 2, 3, 4, 6 or 7 fails in a limited way.
- **`fails`:** check 1 or 5 fails, check 7 fails broadly, or there's no evidence.
