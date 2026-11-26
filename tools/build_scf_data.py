"""Maintainer tool (not part of the plugin): refresh SCF-derived data shipped with Audit Ready.

What it writes (ids and framework metadata only - never SCF control text, which is CC BY-ND 4.0):
  1. plugins/audit-ready/skills/framework-reference/frameworks.csv   framework registry
  2. scf_ids column in the curated catalogs
     - crosswalk-backed catalogs: computed from the SCF crosswalk (rolled up to our requirement ids)
     - hand-mapped catalogs (no SCF crosswalk: cert-in, rbi, sebi-cscrf): kept as written, validated

Input: the SCF API cache shared with claude-grc-engineering, default
~/.cache/claude-grc/scf/<version>/api/ (crosswalks.json, controls.json, crosswalks/<id>.json).
Fill it first, e.g.:
  B=https://grcengclub.github.io/scf-api/api; C=~/.cache/claude-grc/scf/2026.1/api
  curl -sSf $B/crosswalks.json -o $C/crosswalks.json   (and controls.json, crosswalks/<id>.json)

Usage: python tools/build_scf_data.py [--scf-version 2026.1] [--check]
  --check  verify only (exit 1 if files would change or hand-mapped ids are invalid)
"""
import argparse
import csv
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR = os.path.join(ROOT, "plugins", "audit-ready", "skills", "framework-reference")

# key -> (registry scf_framework_id or "", base plugin, display name override or "", notes, resolver spec)
# resolver spec: ("under", fid) | ("iso",) | ("dpdp",) | ("nis2",) | ("manual",)
CURATED = {
    "soc2": ("general-aicpa-tsc-2017", "soc2", "", "Curated. SOC 2 Trust Services Criteria 2017 (rev. points of focus 2022)", ("under", "general-aicpa-tsc-2017")),
    "iso27001": ("general-iso-27001-2022", "iso27001", "", "Curated. Clauses via SCF general-iso-27001-2022; Annex A via general-iso-27002-2022", ("iso",)),
    "dpdp": ("apac-ind-dpdpa-2023", "ind-dpdpa", "", "Curated. DPDP Act 2023 + DPDP Rules 2025; Rules rows mapped via their parent Act section", ("dpdp",)),
    "gdpr": ("emea-eu-gdpr-2016", "gdpr", "", "Curated. GDPR (EU) 2016/679, article level", ("under", "emea-eu-gdpr-2016")),
    "pci-dss": ("general-pci-dss-4-0-1", "pci-dss", "", "Curated. PCI DSS v4.0.1 (June 2024), requirement level x.y; applicability by SAQ", ("under", "general-pci-dss-4-0-1")),
    "hipaa-security": ("usa-federal-law-hipaa-security-rule-2013", "us-hipaa-security", "", "Curated. HIPAA Security Rule 45 CFR 164.306-164.316 + Breach Notification Rule 164.402-164.414 (Privacy Rule out of scope)", ("under", "usa-federal-law-hipaa-security-rule-2013")),
    "nist-csf-2.0": ("general-nist-csf-2-0", "nist-csf-20", "", "Curated. NIST CSF 2.0 (Feb 2024), 106 subcategories", ("under", "general-nist-csf-2-0")),
    "nis2": ("emea-eu-nis2-2022", "eu-nis2", "", "Curated. NIS2 Directive (EU) 2022/2555 Arts 20, 21, 23 + Implementing Regulation (EU) 2024/2690 annex (IR-*)", ("nis2",)),
    "dora": ("emea-eu-dora-2023", "dora", "", "Curated. DORA Regulation (EU) 2022/2554, article level", ("under", "emea-eu-dora-2023")),
    "cert-in": ("", "", "India - CERT-In Directions under Section 70B(6) of the IT Act (28 Apr 2022)", "Curated. No SCF crosswalk; scf_ids hand-mapped by Audit Ready", ("manual",)),
    "rbi": ("", "", "India - RBI IT Governance Master Direction (2023), IT Outsourcing Master Direction (2023), payment data storage (2018)", "Curated. No SCF crosswalk; scf_ids hand-mapped by Audit Ready", ("manual",)),
    "sebi-cscrf": ("", "", "India - SEBI Cybersecurity and Cyber Resilience Framework (CSCRF, Aug 2024)", "Curated. No SCF crosswalk; scf_ids hand-mapped by Audit Ready", ("manual",)),
}
REGION = {"general": "Global", "emea": "EMEA", "apac": "APAC", "americas": "Americas", "amaericas": "Americas", "usa": "Americas"}


def base_plugins(marketplace):
    """scf_framework_id -> base plugin name, read from claude-grc-engineering plugin.json files."""
    out = {}
    fw = os.path.join(marketplace, "plugins", "frameworks")
    if not os.path.isdir(fw):
        return out
    for name in sorted(os.listdir(fw)):
        p = os.path.join(fw, name, ".claude-plugin", "plugin.json")
        if os.path.isfile(p):
            meta = json.load(open(p, encoding="utf-8")).get("framework_metadata", {})
            if meta.get("scf_framework_id"):
                out[meta["scf_framework_id"]] = name
    return out


_xw_cache = {}


def load_xw(api, fid):
    if fid not in _xw_cache:
        p = os.path.join(api, "crosswalks", fid + ".json")
        if not os.path.isfile(p):
            sys.exit(f"missing crosswalk {p} - fetch it into the cache first")
        _xw_cache[fid] = json.load(open(p, encoding="utf-8"))["framework_to_scf"]["mappings"]
    return _xw_cache[fid]


def rollup(mappings, match):
    ids = set()
    for k, v in mappings.items():
        if match(k):
            ids.update(v)
    return ids


def under(prefix):
    """Key equals prefix or is a child: 'CC6.1-POF2', '6.1.2(e)', '7.5.1', '8(7)(b)', 'Article 5.1(a)'."""
    return lambda k: k == prefix or k.startswith(prefix + "-") or k.startswith(prefix + "(") or k.startswith(prefix + ".")


def scf_sort(ids):
    def key(i):
        fam, _, num = i.partition("-")
        return (fam, [int(x) for x in re.findall(r"\d+", num)])
    return ";".join(sorted(ids, key=key))


DPDP_RULE_PARENT = {"DPDP-R3": ["5"], "DPDP-R4": ["6"], "DPDP-R6": ["8(5)"], "DPDP-R7": ["8(6)"],
                    "DPDP-R8": ["8(7)"], "DPDP-R9": ["8(9)"], "DPDP-R10": ["9"], "DPDP-R13": ["10"],
                    "DPDP-R14": ["11", "12", "13", "14"], "DPDP-R15": ["16"]}


def dpdp_sections(req_id):
    if req_id in DPDP_RULE_PARENT:
        return DPDP_RULE_PARENT[req_id]
    if req_id == "DPDP-6-CM":
        return ["6(7)", "6(8)", "6(9)"]
    m = re.fullmatch(r"DPDP-(\d+)(?:-(\d+))?", req_id)
    if not m:
        return []
    return [f"{m.group(1)}({m.group(2)})" if m.group(2) else m.group(1)]


def make_resolver(spec, api):
    kind = spec[0]
    if kind == "under":
        xw = load_xw(api, spec[1])
        return lambda rid: rollup(xw, under(rid))
    if kind == "iso":
        i01, i02 = load_xw(api, "general-iso-27001-2022"), load_xw(api, "general-iso-27002-2022")

        def iso(rid):
            if not rid.startswith("A."):
                return rollup(i01, under(rid))
            key = rid[2:]
            if key not in i02 and key.endswith("0"):
                # Upstream SCF data stores 27002 ids as numbers, so 5.10 collapsed into 5.1 (and 5.20 -> 5.2, ...).
                # Both controls of each pair get the shared, over-inclusive list. See framework-reference/scf.md.
                key = key.rstrip("0")
            return rollup(i02, lambda k: k == key)
        return iso
    if kind == "dpdp":
        dp = load_xw(api, "apac-ind-dpdpa-2023")

        def dpdp(rid):
            ids = set()
            for s in dpdp_sections(rid):
                ids |= rollup(dp, under(s))
            return ids
        return dpdp
    if kind == "nis2":
        art, annex = load_xw(api, "emea-eu-nis2-2022"), load_xw(api, "emea-eu-nis2-annex-2024")
        return lambda rid: rollup(annex, under(rid[3:])) if rid.startswith("IR-") else rollup(art, under(rid))
    return None  # manual


def catalog_with_scf(path, resolver, valid):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    hdr = [h for h in rows[0].keys() if h != "scf_ids"] + ["scf_ids"]
    unmapped, invalid = [], []
    for r in rows:
        if resolver is None:  # hand-mapped: keep, validate
            ids = {i for i in (r.get("scf_ids") or "").split(";") if i}
            invalid += [f"{r['req_id']}:{i}" for i in ids if i not in valid]
        else:
            ids = {i for i in resolver(r["req_id"]) if i in valid}
            if not ids:  # crosswalk has nothing for this row: keep a hand mapping if one exists, validated
                hand = {i for i in (r.get("scf_ids") or "").split(";") if i}
                invalid += [f"{r['req_id']}:{i}" for i in hand if i not in valid]
                ids = hand
        r["scf_ids"] = scf_sort(ids)
        if not ids:
            unmapped.append(r["req_id"])
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=hdr, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue(), unmapped, invalid, len(rows)


def registry(api, bases):
    idx = json.load(open(os.path.join(api, "crosswalks.json"), encoding="utf-8"))["frameworks"]
    by_id = {f["framework_id"]: f for f in idx}
    rows, cur_ids = [], set()
    for key, (fid, plug, name, notes, _) in CURATED.items():
        cat = f"catalogs/{key}.csv"
        if not os.path.isfile(os.path.join(FR, cat)):
            continue
        cur_ids.add(fid)
        region = REGION.get(fid.split("-")[0], "APAC") if fid else "APAC"
        rows.append([key, name or by_id.get(fid, {}).get("display_name", key), "curated", fid, region, plug, cat, notes])
    for f in sorted(idx, key=lambda x: x["framework_id"]):
        fid = f["framework_id"]
        if fid in cur_ids:
            continue
        plug = bases.get(fid, "")
        rows.append([plug or fid, f["display_name"], "scf", fid, REGION.get(fid.split("-")[0], ""), plug, "generated",
                     f"SCF-backed ({f.get('framework_controls_mapped', '?')} requirement ids mapped)"])
    keys = [r[0] for r in rows]
    dup = {k for k in keys if keys.count(k) > 1}
    for r in rows:  # disambiguate duplicate short keys with the full SCF id
        if r[0] in dup and r[2] == "scf":
            r[0] = r[3]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["key", "display_name", "tier", "scf_framework_id", "region", "base_plugin", "catalog", "notes"])
    w.writerows(rows)
    return buf.getvalue(), len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf-version", default="2026.1")
    ap.add_argument("--cache", default=os.path.expanduser("~/.cache/claude-grc/scf"))
    ap.add_argument("--marketplace", default=os.path.expanduser("~/.claude/plugins/marketplaces/grc-engineering-suite"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    api = os.path.join(a.cache, a.scf_version, "api")
    valid = {c["control_id"] for c in json.load(open(os.path.join(api, "controls.json"), encoding="utf-8"))["controls"]}

    outputs, report, all_invalid = {}, [], []
    for key, spec in CURATED.items():
        path = os.path.join(FR, "catalogs", key + ".csv")
        if not os.path.isfile(path):
            report.append(f"{key}: catalog not written yet - skipped")
            continue
        text, unmapped, invalid, n = catalog_with_scf(path, make_resolver(spec[4], api), valid)
        outputs[path] = text
        all_invalid += invalid
        report.append(f"{key}: {n} rows, {len(unmapped)} without SCF mapping {unmapped if len(unmapped) < 15 else str(len(unmapped)) + ' rows'}"
                      + (f", INVALID {invalid}" if invalid else ""))
    reg, n = registry(api, base_plugins(a.marketplace))
    outputs[os.path.join(FR, "frameworks.csv")] = reg
    report.append(f"frameworks.csv: {n} frameworks (SCF {a.scf_version})")

    changed = [p for p, t in outputs.items() if not os.path.isfile(p) or open(p, encoding="utf-8").read() != t]
    print("\n".join(report))
    if a.check:
        print("would change:", [os.path.relpath(p, ROOT) for p in changed] or "nothing")
        sys.exit(1 if changed or all_invalid else 0)
    if all_invalid:
        sys.exit(f"invalid hand-mapped SCF ids: {all_invalid}")
    for p in changed:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(outputs[p])
    print("wrote:", [os.path.relpath(p, ROOT) for p in changed] or "nothing")


if __name__ == "__main__":
    main()
