# SCF-backed frameworks

Audit Ready ships curated catalogs for 12 frameworks (`tier=curated` in `frameworks.csv`). Every other framework that the Secure Controls Framework (SCF) maps (`tier=scf`, 240 of them) is built on demand from the SCF crosswalks. claude-grc-engineering uses the same crosswalks.

- **Source:** `https://grcengclub.github.io/scf-api/api/` (SCF version in the cache path, currently `2026.1`).
- **Licence:** SCF data is CC BY-ND 4.0. Audit Ready never ships SCF text. It fetches at run time into the user's own cache, and writes generated catalogs only into the user's `compliance/catalogs/` folder, with attribution. Do not paste SCF descriptions into committed docs.
- **What you get:**
  - real requirement ids from the crosswalk (`framework_to_scf`);
  - the SCF control ids and titles each requirement maps to;
  - the SCF evidence-request ids;
  - an inferred owning function.
- **What you don't get:**
  - the official requirement wording;
  - mandatory flags (all rows are `mandatory=no`, unless the registry `notes` say otherwise);
  - framework-specific applicability logic.
- Say this plainly in `scope.md` and in reports, and recommend checking against the official text.

## 1. Pick the framework

Look the user's request up in `frameworks.csv`, matching on `key`, `display_name` or `base_plugin` (for example "PCI" → `pci-dss`, "CIS" → `cis-controls`, "800-53" → `nist-800-53`). When several match, such as CIS IG1, IG2 and IG3, or NIS2 and its annex, ask which one.

- `tier=curated`: use `catalogs/<key>.csv`, which is shipped. Stop here.
- `tier=scf`: continue below.
- Not in the registry at all: say so, and treat it as out of scope. Never invent requirement ids.

## 2. Make sure the SCF data is cached

The cache is shared with claude-grc-engineering:

```
~/.cache/claude-grc/scf/<version>/api/controls.json               (about 14 MB, once per version)
~/.cache/claude-grc/scf/<version>/api/crosswalks/<scf_framework_id>.json
```

If a file is missing, show the user the command and fetch it after they approve. It's a read-only download of public data:

```bash
B=https://grcengclub.github.io/scf-api/api; C=~/.cache/claude-grc/scf/2026.1/api
mkdir -p "$C/crosswalks"
curl -sSf "$B/controls.json" -o "$C/controls.json"
curl -sSf "$B/crosswalks/<scf_framework_id>.json" -o "$C/crosswalks/<scf_framework_id>.json"
```

On PowerShell, use `Invoke-WebRequest -Uri ... -OutFile ...`.

**Offline:** if the API can't be reached and nothing is cached, say so and offer only the curated frameworks. Never guess requirement ids.

## 3. Generate the catalog

Choose a granularity:

| Mode | Use when | Example result |
|---|---|---|
| `rollup` (default) | Ids have lettered or numbered sub-items such as `Article 5.2(a)`, `AC-2(1)` or `CC6.1-POF3` | NIST 800-53: 292 base controls; DORA: 117 article paragraphs |
| `rollup2` | Ids are deeply dotted, such as `8.4.2` | PCI DSS: 71 requirements (`8.4`) instead of 351 sub-requirements |
| `full` | The user wants every sub-requirement | DORA: 241 rows |

Run this read-only command, standard-library Python only, after showing it to the user. It writes one file: `compliance/catalogs/<key>.csv`. Arguments: cache api dir, `scf_framework_id`, `key`, output file, mode.

```bash
mkdir -p compliance/catalogs
python3 -I - ~/.cache/claude-grc/scf/2026.1/api <scf_framework_id> <key> compliance/catalogs/<key>.csv rollup <<'PY'
import csv, json, re, sys
api, fid, key, out, mode = sys.argv[1:6]
xw = json.load(open(f"{api}/crosswalks/{fid}.json", encoding="utf-8"))["framework_to_scf"]["mappings"]
ctl = {c["control_id"]: c for c in json.load(open(f"{api}/controls.json", encoding="utf-8"))["controls"]}
FN = {"AAT": "Engineering", "AST": "IT", "BCD": "Engineering", "CAP": "Engineering", "CFG": "Engineering", "CHG": "Engineering",
      "CLD": "Engineering", "CPL": "Leadership", "CRY": "Engineering", "DCH": "Engineering", "EMB": "Engineering", "END": "IT",
      "GOV": "Leadership", "HRS": "HR", "IAC": "IT", "IAO": "Leadership", "IRO": "Engineering", "MDM": "IT", "MNT": "IT",
      "MON": "Engineering", "NET": "Engineering", "OPS": "Engineering", "PES": "IT", "PRI": "Legal", "PRM": "Leadership",
      "RSK": "Leadership", "SAT": "HR", "SEA": "Engineering", "TDA": "Engineering", "THR": "Engineering", "TPM": "Legal",
      "VPM": "Engineering", "WEB": "Engineering"}
strip = lambda k: re.sub(r"(-POF\d+|\([^)]*\))+$", "", k)
two = lambda k: re.sub(r"^(\D*\d+\.\d+)(\.\d+)+", r"\1", strip(k))
parent = {"full": lambda k: k, "rollup": strip, "rollup2": two}[mode]
groups = {}
for k, v in xw.items():
    groups.setdefault(parent(k), set()).update(v)
nat = lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["framework", "req_id", "title", "summary", "mandatory", "function", "typical_evidence", "category", "scf_ids"])
    for rid in sorted(groups, key=nat):
        ids = sorted(i for i in groups[rid] if i in ctl)
        fams = [ctl[i]["family"] for i in ids]
        fam = max(set(fams), key=fams.count) if fams else ""
        titles = [ctl[i]["title"] for i in ids]
        w.writerow([key, rid, "; ".join(titles[:3]) + (" ..." if len(titles) > 3 else ""),
                    f"SCF-backed row: requirement id from the SCF crosswalk {fid}; text is SCF control titles (CC BY-ND 4.0). Verify against the official text.",
                    "no", FN.get(fam, "Leadership"),
                    ";".join(sorted({e for i in ids for e in ctl[i].get("evidence_requests") or []})[:10]),
                    ctl[ids[0]]["family_name"] if ids else "", ";".join(ids)])
print(out, len(groups), "rows")
PY
```

On Windows PowerShell, put the program in a single-quoted here-string and pipe it: `@'...'@ | python -I - <args>`.

The output has the same columns as the curated catalogs plus `scf_ids`:

- `title`: the SCF control titles (at most 3).
- `function`: the most common SCF family among the mapped controls, using the family → function map above.
- `typical_evidence`: SCF evidence-request ids (ERL, `E-XXX-nn`).
- `category`: the SCF family name.

Write the SCF version and the date into `scope.md`: "SCF-backed catalog: <display_name>, SCF crosswalk <version>, generated <date>, <n> rows (<mode>)".

## 4. Applicability for SCF-backed rows

- With no mandatory flags, propose `applicable=yes` for every row. Then propose `no` only where a profile fact clearly excludes the requirement. For example, PCI wireless requirements when there is no wireless in the cardholder data environment (CDE).
- If the base-repo plugin for the framework is installed (`base_plugin` column, with integration detected by grc-assistant), point the user to its specialist commands for applicability decisions:

| Plugin | Commands |
|---|---|
| `pci-dss` | `/pci-dss:saq-select`, `/pci-dss:requirement` |
| `cis-controls` | `/cis-controls:ig-select` |
| `nist-800-53` | `/nist-800-53:select-baseline`, `/nist-800-53:control-tailor` |
| `gdpr` | `/gdpr:dpia` |
| `cmmc` | `/cmmc:level-select` |

## 5. How evidence links across frameworks

Every curated catalog row and every generated row carries `scf_ids`. Every playbook row carries an `SCF` column.

- **When filing evidence (`/collect`, `/inbox`):**
  - Start from the item's own `requirements`.
  - Propose adding every in-scope requirement, in any framework, whose `scf_ids` include one of the item's SCF ids.
  - Show these additions as "also supports (via SCF)" and let the user accept or trim them before writing `index.csv`.
- **When building the plan (`/evidence-plan`):**
  - A playbook row is relevant to an SCF-backed framework when its SCF ids intersect the requirement's `scf_ids`.
  - Dedupe items across frameworks by shared SCF ids.
- **Mappings are broad.** One SOC 2 criterion maps to up to 20 SCF controls. An SCF link is a hint that an artifact may support a requirement, not proof that it does. The evidence reviewer still judges relevance (rubric check 1), and a weak link becomes `partial` or `fails` with a gap.

## Known SCF data issues

- **ISO 27002:2022 crosswalk:** ids ending in 0 collapsed into their prefix, because they were stored as numbers. `5.10` merges into `5.1`, and the same happens to 5.20, 5.30, 7.10, 8.10, 8.20 and 8.30. In the curated `iso27001.csv`, both controls of each pair carry the shared, over-inclusive SCF list.
- **Unmapped rows:** some curated rows have no SCF mapping, so their `scf_ids` are empty. Evidence for them is planned directly, not by SCF dedupe. They are: DPDP §16, §17 and Rule 15; GDPR Articles 6, 22, 26 and 47; NIS2 Articles 20.1, 20.2 and 24.
- **No SCF crosswalk:** CERT-In, RBI and SEBI CSCRF have none. Their `scf_ids` are hand-mapped by Audit Ready and validated by `tools/build_scf_data.py`.
- **Uneven coverage:** SCF links from playbook rows reach some frameworks well (PCI DSS) and others poorly (GDPR maps mostly to privacy controls). Curated catalogs therefore also get hand-mapped keys in the playbooks' `Requirements` column. SCF links only add to those.

## Maintainers

`tools/build_scf_data.py` (repo root, not part of the plugin) refreshes `frameworks.csv` and the curated `scf_ids` columns from the cache. Run it with `--check` in CI.
