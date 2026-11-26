"""Check a /audit-ready:scope result against an example's expected outcome.

Usage:
  python tests/check_scope_result.py --compliance <run>/compliance --expected examples/<name>/expected.csv

expected.csv columns: kind,framework,req_id,expect,why
  kind=framework    expect = in | out | either   (in = the framework has rows in applicability.csv)
  kind=requirement  expect = allowed applicable values separated by "|", e.g. "yes" or "yes|inherited".
                    Skipped (not failed) when its framework is not in scope.

Exit code 0 when every check passes, 1 otherwise. Standard library only.
"""
import argparse
import csv
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compliance", required=True, help="path to the compliance/ folder of a run")
    ap.add_argument("--expected", required=True, help="path to an examples/<name>/expected.csv")
    a = ap.parse_args()

    app_path = os.path.join(a.compliance, "applicability.csv")
    if not os.path.isfile(app_path):
        sys.exit(f"no applicability.csv in {a.compliance}")
    rows = list(csv.DictReader(open(app_path, encoding="utf-8")))
    in_scope = {r["framework"] for r in rows}
    actual = {(r["framework"], r["req_id"]): r for r in rows}

    passed = failed = skipped = 0
    lines = []
    for e in csv.DictReader(open(a.expected, encoding="utf-8")):
        fw, rid, exp, why = e["framework"], e["req_id"], e["expect"], e["why"]
        if e["kind"] == "framework":
            got = "in" if fw in in_scope else "out"
            ok = exp == "either" or got == exp
            label = f"framework {fw}: expected {exp}, got {got}"
        else:
            if fw not in in_scope:
                skipped += 1
                lines.append(f"  SKIP {fw}:{rid} (framework not in scope)")
                continue
            r = actual.get((fw, rid))
            if r is None:
                ok, label = False, f"{fw}:{rid}: missing from applicability.csv"
            else:
                allowed = exp.split("|")
                ok = r["applicable"] in allowed
                label = f"{fw}:{rid}: expected {exp}, got {r['applicable']}"
                if not ok:
                    label += f" (reason given: {r['reason']})"
                elif r["applicable"] == "no" and not r["reason"].strip():
                    ok, label = False, f"{fw}:{rid}: 'no' without a reason"
        if ok:
            passed += 1
            lines.append(f"  PASS {label}")
        else:
            failed += 1
            lines.append(f"  FAIL {label}  [why expected: {why}]")

    # Rules that hold for every run
    for r in rows:
        if r["mandatory"] == "yes" and r["applicable"] == "no":
            reason = r["reason"].lower()
            # mandatory rows may only be 'no' when the whole entity is outside direct scope (framework-specific rules)
            if reason.startswith("mandatory (entity:") or reason.startswith("mandatory (contract:"):
                failed += 1
                lines.append(f"  FAIL {r['framework']}:{r['req_id']}: entity-locked row set to 'no'")
            elif not any(k in reason for k in ("not a financial entity", "processor", "supplier", "vendor", "not a covered", "saq")):
                failed += 1
                lines.append(f"  FAIL {r['framework']}:{r['req_id']}: mandatory row set to 'no' without an entity-scope reason")
        if r["applicable"] in ("no", "inherited") and not r["reason"].strip():
            failed += 1
            lines.append(f"  FAIL {r['framework']}:{r['req_id']}: '{r['applicable']}' without a reason")

    print("\n".join(lines))
    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
