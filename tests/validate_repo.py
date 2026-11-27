"""Static checks for the Audit Ready repo. Standard library only; no network, no SCF cache needed.

Usage: python tests/validate_repo.py      (exit 1 on any failure)

Checks
  manifests      marketplace.json sources exist; plugin.json name matches its folder; required fields
  templates      CSV templates match the headers documented in the grc-assistant skill
  catalogs       header, enums, unique ids, expected row counts, mandatory rules, scf_ids format
  registry       frameworks.csv header, unique keys, curated rows <-> catalog files
  playbooks      row shape, unique ids, requirement keys exist in catalogs, SCF id format,
                 every command obeys the read-only allowlist
  examples       CSV headers, sha256 of filed evidence, readiness in the report matches assessments,
                 expected.csv references real requirements
  skills         frontmatter present; scf.md embedded generator compiles
"""
import ast
import csv
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "audit-ready")
SK = os.path.join(PLUGIN, "skills")
FR = os.path.join(SK, "framework-reference")

HEADERS = {
    "applicability.csv": "framework,req_id,title,applicable,mandatory,reason,approved_by,approved_at",
    "evidence-plan.csv": "item_id,item,requirements,method,tool,command_ref,owner,period,due,status",
    "index.csv": "file,type,requirements,source,command,period,collected_at,sha256,redacted",
    "assessments.csv": "evidence,requirement,verdict,gaps,fix,reviewer,date,approved",
    "findings.csv": "id,requirement,severity,finding,fix,owner,status,opened,due,closed",
}
CATALOG_HEADER = "framework,req_id,title,summary,mandatory,function,typical_evidence,category,scf_ids"
EXPECTED_ROWS = {"soc2": 61, "iso27001": 118, "dpdp": 32, "gdpr": 38, "pci-dss": 71, "hipaa-security": 69,
                 "nist-csf-2.0": 106, "nis2": 35, "dora": 28, "cert-in": 7, "rbi": 26, "sebi-cscrf": 21}
FUNCTIONS = {"Engineering", "IT", "HR", "Legal", "Leadership"}
INDEX_TYPES = {"config", "population", "log", "policy", "procedure", "record", "report", "screenshot", "other"}
FINDING_STATUS = {"open", "in-progress", "accepted", "closed"}
SCF_ID = re.compile(r"^[A-Z]{3}-\d{2}(\.\d+)?$")

errors = []


def err(area, msg):
    errors.append(f"[{area}] {msg}")


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    header = text.split("\n", 1)[0].rstrip("\r")
    return header, list(csv.DictReader(text.splitlines()))


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# ---------------------------------------------------------------- manifests
def check_manifests():
    mp = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    for k in ("name", "owner", "plugins"):
        if k not in mp:
            err("manifests", f"marketplace.json missing {k}")
    names = [p["name"] for p in mp.get("plugins", [])]
    if len(names) != len(set(names)):
        err("manifests", "duplicate plugin names in marketplace.json")
    for p in mp.get("plugins", []):
        src = os.path.normpath(os.path.join(ROOT, p["source"]))
        pj = os.path.join(src, ".claude-plugin", "plugin.json")
        if not os.path.isfile(pj):
            err("manifests", f"{p['name']}: source {p['source']} has no .claude-plugin/plugin.json")
            continue
        m = json.load(open(pj, encoding="utf-8"))
        if m.get("name") != p["name"] or m.get("name") != os.path.basename(src):
            err("manifests", f"{p['name']}: plugin.json name '{m.get('name')}' must match marketplace entry and folder")
        if not m.get("version"):
            err("manifests", f"{p['name']}: plugin.json has no version")


# ---------------------------------------------------------------- templates
def check_templates():
    skill = open(os.path.join(SK, "grc-assistant", "SKILL.md"), encoding="utf-8").read()
    for name, hdr in HEADERS.items():
        t = open(os.path.join(SK, "grc-assistant", "templates", name), encoding="utf-8").read().strip()
        if t != hdr:
            err("templates", f"{name} header differs from expected")
        if f"`{hdr}`" not in skill:
            err("templates", f"grc-assistant SKILL.md does not document the {name} header exactly")


# ---------------------------------------------------------------- catalogs
def load_catalogs():
    cats = {}
    for f in sorted(glob.glob(os.path.join(FR, "catalogs", "*.csv"))):
        key = os.path.basename(f)[:-4]
        header, rows = read_csv(f)
        cats[key] = (header, rows, f)
    return cats


def check_catalogs(cats):
    if set(cats) != set(EXPECTED_ROWS):
        err("catalogs", f"catalog set {sorted(cats)} differs from expected {sorted(EXPECTED_ROWS)}")
    for key, (header, rows, f) in cats.items():
        if header != CATALOG_HEADER:
            err("catalogs", f"{key}: header is '{header}'")
        if key in EXPECTED_ROWS and len(rows) != EXPECTED_ROWS[key]:
            err("catalogs", f"{key}: {len(rows)} rows, expected {EXPECTED_ROWS[key]}")
        ids = [r["req_id"] for r in rows]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            err("catalogs", f"{key}: duplicate req_ids {dup}")
        for r in rows:
            where = f"{key}:{r.get('req_id')}"
            if None in r or None in r.values():
                err("catalogs", f"{where}: wrong number of fields")
                continue
            if r["framework"] != key:
                err("catalogs", f"{where}: framework column '{r['framework']}' != file key")
            if r["mandatory"] not in ("yes", "no"):
                err("catalogs", f"{where}: mandatory '{r['mandatory']}'")
            if r["function"] not in FUNCTIONS:
                err("catalogs", f"{where}: function '{r['function']}'")
            for col in ("title", "summary", "typical_evidence", "category"):
                if not r[col].strip():
                    err("catalogs", f"{where}: empty {col}")
            for s in filter(None, r["scf_ids"].split(";")):
                if not SCF_ID.match(s):
                    err("catalogs", f"{where}: malformed SCF id '{s}'")
    if "soc2" in cats:
        for r in cats["soc2"][1]:
            if r["req_id"].startswith("CC") and r["mandatory"] != "yes":
                err("catalogs", f"soc2:{r['req_id']}: Common Criteria must be mandatory")
    if "iso27001" in cats:
        rows = cats["iso27001"][1]
        if sum(1 for r in rows if r["req_id"].startswith("A.")) != 93:
            err("catalogs", "iso27001: Annex A must have 93 controls")
        for r in rows:
            if not r["req_id"].startswith("A.") and r["mandatory"] != "yes":
                err("catalogs", f"iso27001:{r['req_id']}: clauses 4-10 must be mandatory")
    if "nist-csf-2.0" in cats:
        for r in cats["nist-csf-2.0"][1]:
            if not re.match(r"^(GV|ID|PR|DE|RS|RC)\.[A-Z]{2}-\d{2}$", r["req_id"]):
                err("catalogs", f"nist-csf-2.0:{r['req_id']}: not a CSF 2.0 subcategory id")


def valid_keys(cats):
    return {f"{k}:{r['req_id']}" for k, (_, rows, _) in cats.items() for r in rows}


# ---------------------------------------------------------------- registry
def check_registry(cats):
    header, rows = read_csv(os.path.join(FR, "frameworks.csv"))
    if header != "key,display_name,tier,scf_framework_id,region,base_plugin,catalog,notes":
        err("registry", f"header is '{header}'")
    keys = [r["key"] for r in rows]
    if len(keys) != len(set(keys)):
        err("registry", "duplicate keys")
    curated = {r["key"] for r in rows if r["tier"] == "curated"}
    if curated != set(cats):
        err("registry", f"curated keys {sorted(curated)} != catalog files {sorted(cats)}")
    for r in rows:
        if r["tier"] not in ("curated", "scf"):
            err("registry", f"{r['key']}: tier '{r['tier']}'")
        if r["tier"] == "scf" and not r["scf_framework_id"]:
            err("registry", f"{r['key']}: scf tier without scf_framework_id")


# ---------------------------------------------------------------- playbooks
SPLIT = re.compile(r"(?<!\\)\|")
ALLOWED_VERB = {
    "aws": re.compile(r"^aws (\S+) (get-|list-|describe-|generate-credential-report\b)"),
    "gcloud": re.compile(r"^gcloud (.+ )?(list|describe|get-iam-policy)\b"),
    "az": re.compile(r"^az (.+ )?(show|list)\b|^az rest --method get\b"),
    "gam": re.compile(r"^gam (all users |ou \S+ )?(info|print|show|report)\b"),
    "gh": re.compile(r"^gh (api|repo list|auth status)\b"),
}
GH_WRITE_FLAGS = re.compile(r"\s(-X|--method|-f|-F|--field|--raw-field|--input)(\s|=|$)")
# Commands that return secrets even though their verb looks read-only (keep in sync with evidence-playbooks SKILL.md)
SECRET_DENY = re.compile(
    r"^aws (secretsmanager get-secret-value|ssm get-parameters?(-by-path)?\b|kms decrypt|ecr get-(login-password|authorization-token)"
    r"|codeartifact get-authorization-token|sts (get-session-token|get-federation-token|assume-role)|rds generate-db-auth-token"
    r"|lambda get-function(-configuration)?\b|iam get-ssh-public-key)"
    r"|^az (keyvault (secret (show|download)|key download|certificate download)|storage account (keys list|show-connection-string)"
    r"|storage .*generate-sas|acr credential show|cosmosdb keys list|redis list-keys|servicebus .*keys list|eventhubs .*keys list"
    r"|functionapp (function )?keys list|webapp deployment list-publishing-(credentials|profiles)|aks get-credentials"
    r"|sql db show-connection-string|account get-access-token)"
    r"|^az rest .*vault\.azure\.net"
    r"|^gcloud (auth (application-default )?print-(access|identity)-token|secrets versions access|container clusters get-credentials"
    r"|sql generate-login-token)"
    r"|^gh (auth token|api graphql|secret\b|variable get)"
    r"|^gam .*backupcodes"
)


def commands_in(cell):
    return [c.strip() for c in re.findall(r"`([^`]+)`", cell.replace("\\|", "|"))]


QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def check_command(where, cmd):
    if cmd.startswith(("base64", "jq")) or not re.match(r"^(aws|gcloud|az|gam|gh) ", cmd):
        return  # helper fragments such as `base64 -d` or flags quoted in notes
    tool = cmd.split()[0]
    bare = QUOTED.sub("''", cmd)  # pipes, & and ; inside quotes (jq filters, URL queries) are data, not shell
    for part in re.split(r"\s\|\s", bare):
        part = part.strip()
        if part.startswith(("base64 -d", "jq", "head")):
            continue
        if not ALLOWED_VERB[tool].search(part):
            err("playbooks", f"{where}: command not on the read-only allowlist: {part}")
        if SECRET_DENY.search(part):
            err("playbooks", f"{where}: command returns secrets (denylist): {part}")
        if tool == "gh" and GH_WRITE_FLAGS.search(part):
            err("playbooks", f"{where}: gh api command uses a write flag: {part}")
    if re.search(r"[;&]|\$\(|`", bare):
        err("playbooks", f"{where}: command chaining or substitution is not allowed: {cmd}")


def check_playbooks(keys):
    seen = set()
    for f in sorted(glob.glob(os.path.join(SK, "evidence-playbooks", "playbooks", "*.md"))):
        text = open(f, encoding="utf-8").read()
        if "| ID | Evidence item | Requirements | SCF | Command(s) | File slug | Notes |" not in text:
            err("playbooks", f"{rel(f)}: table header changed")
        for line in text.split("\n"):
            cells = SPLIT.split(line)
            if len(cells) < 3 or not re.match(r"^ [A-Z]+-\d{2} $", cells[1]):
                continue
            rid = cells[1].strip()
            where = f"{os.path.basename(f)}:{rid}"
            if len(cells) != 9:
                err("playbooks", f"{where}: expected 7 columns, found {len(cells) - 2}")
                continue
            if rid in seen:
                err("playbooks", f"{where}: duplicate row id")
            seen.add(rid)
            for k in filter(None, cells[3].strip().split(";")):
                if k not in keys:
                    err("playbooks", f"{where}: unknown requirement key '{k}'")
            for s in filter(None, cells[4].strip().split(";")):
                if not SCF_ID.match(s):
                    err("playbooks", f"{where}: malformed SCF id '{s}'")
            for cmd in commands_in(cells[5]):
                check_command(where, cmd)
    if len(seen) < 77:
        err("playbooks", f"only {len(seen)} playbook rows found")


# ---------------------------------------------------------------- claude-grc-engineering integration
FIX = os.path.join(ROOT, "tests", "fixtures")
EVAL_STATUS = {"pass", "fail", "not_applicable", "inconclusive", "skipped"}
SEVERITY = {"critical", "high", "medium", "low", "info"}
GAP_CMD = re.compile(r"gap-assessment\.js")
FENCE = re.compile(r"```[a-z]*\n(.*?)```", re.S)


def scf_index(cats):
    """SCF id -> set of framework:req_id keys from curated catalogs."""
    idx = {}
    for key, (_, rows, _) in cats.items():
        for r in rows:
            for s in filter(None, r["scf_ids"].split(";")):
                idx.setdefault(s, set()).add(f"{key}:{r['req_id']}")
    return idx


def rollup(fid, native):
    """Native id from a gap report -> curated catalog key, as commands/collect.md describes."""
    if fid == "general-aicpa-tsc-2017":
        return "soc2:" + re.sub(r"-POF\d+$", "", native)
    if fid == "general-iso-27002-2022":
        return "iso27001:A." + native
    if fid == "general-iso-27001-2022":
        return "iso27001:" + native
    return None


def check_integration(cats):
    # 1. every gap-assessment command shown to users stays inside the allowlist
    for f in glob.glob(os.path.join(PLUGIN, "**", "*.md"), recursive=True):
        for block in FENCE.findall(open(f, encoding="utf-8").read()):
            for line in block.split("\n"):
                if not GAP_CMD.search(line):
                    continue
                if "--output=json" not in line or "--report-dir=compliance/evidence/_staging/" not in line:
                    err("integration", f"{rel(f)}: gap-assessment must use --output=json and --report-dir=compliance/evidence/_staging/...: {line.strip()}")
                if "github-issues" in line or "--create" in line:
                    err("integration", f"{rel(f)}: gap-assessment must not create GitHub issues: {line.strip()}")
    idx = scf_index(cats)
    # 2. inspector Finding fixture: Finding v1 shape, and every SCF id links to a curated requirement
    path = os.path.join(FIX, "findings", "github-inspector.json")
    docs = json.load(open(path, encoding="utf-8"))
    if not isinstance(docs, list) or not docs:
        err("integration", f"{rel(path)}: must be a non-empty JSON array of Findings")
        docs = []
    for d in docs:
        for k in ("schema_version", "source", "source_version", "run_id", "collected_at", "resource", "evaluations"):
            if k not in d:
                err("integration", f"{rel(path)}: Finding missing '{k}'")
        for e in d.get("evaluations", []):
            if e.get("status") not in EVAL_STATUS:
                err("integration", f"{rel(path)}: bad status {e.get('status')}")
            if e.get("status") == "fail" and (e.get("severity") not in SEVERITY or not e.get("message")):
                err("integration", f"{rel(path)}: fail needs severity and message")
            if e.get("control_framework") == "SCF" and e.get("control_id") not in idx:
                err("integration", f"{rel(path)}: SCF {e.get('control_id')} maps to no curated requirement")
    # 3. gap report fixture: native ids roll up to real catalog rows
    path = os.path.join(FIX, "gap", "findings.normalized.json")
    gap = json.load(open(path, encoding="utf-8"))
    keys = valid_keys(cats)
    hits = 0
    for tier in ("tier1", "tier2", "tier3", "passes", "inconclusive"):
        for item in gap.get(tier, []):
            for fid, natives in item.get("frameworks", {}).items():
                for n in natives:
                    k = rollup(fid, n)
                    if k is None:
                        continue
                    if k in keys:
                        hits += 1
                    elif not re.search(r"-POF|\.\d+\.\d+", n):
                        err("integration", f"{rel(path)}: {fid} {n} rolls up to unknown {k}")
    if hits == 0:
        err("integration", f"{rel(path)}: no native id rolled up to a curated requirement")


# ---------------------------------------------------------------- examples
def readiness(app_rows, ass_rows):
    applicable = {}
    for r in app_rows:
        if r["applicable"] in ("yes", "inherited"):
            applicable.setdefault(r["framework"], set()).add(r["req_id"])
    latest = {}
    for r in ass_rows:
        if r["approved"] == "yes":
            latest[(r["evidence"], r["requirement"])] = r  # later rows win
    score = {}
    for (_, req), r in latest.items():
        fw, rid = req.split(":", 1)
        s = {"satisfies": 1.0, "partial": 0.5, "fails": 0.0}[r["verdict"]]
        score[(fw, rid)] = min(score.get((fw, rid), 1.0), s)  # worst verdict across evidence
    out = {}
    for fw, ids in applicable.items():
        total = sum(score.get((fw, i), 0.0) for i in ids)
        out[fw] = (len(ids), sum(1 for i in ids if score.get((fw, i)) == 1.0),
                   sum(1 for i in ids if score.get((fw, i)) == 0.5), round(total / len(ids) * 100))
    return out


def check_examples(keys):
    for comp in sorted(glob.glob(os.path.join(ROOT, "examples", "*", "compliance"))):
        name = rel(comp)
        for fname, hdr in HEADERS.items():
            for p in glob.glob(os.path.join(comp, "**", fname), recursive=True):
                h, _ = read_csv(p)
                if h != hdr:
                    err("examples", f"{rel(p)}: header differs from template")
        idx = os.path.join(comp, "evidence", "index.csv")
        if os.path.isfile(idx):
            for r in read_csv(idx)[1]:
                fp = os.path.join(comp, "evidence", r["file"])
                if not os.path.isfile(fp):
                    err("examples", f"{name}: indexed file missing: {r['file']}")
                    continue
                if hashlib.sha256(open(fp, "rb").read()).hexdigest() != r["sha256"]:
                    err("examples", f"{name}: sha256 mismatch for {r['file']}")
                for k in filter(None, r["requirements"].split(";")):
                    if k not in keys:
                        err("examples", f"{name}: index requirement '{k}' not in catalogs")
                if r["type"] not in INDEX_TYPES:
                    err("examples", f"{name}: index type '{r['type']}' for {r['file']}")
        fnd = os.path.join(comp, "audit", "findings.csv")
        if os.path.isfile(fnd):
            for r in read_csv(fnd)[1]:
                if r["status"] not in FINDING_STATUS or r["severity"] not in ("major", "minor", "observation"):
                    err("examples", f"{name}: finding {r['id']} has status '{r['status']}' / severity '{r['severity']}'")
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", r["opened"]):
                    err("examples", f"{name}: finding {r['id']} needs an ISO 'opened' date")
                if (r["status"] in ("closed", "accepted")) != bool(r["closed"]):
                    err("examples", f"{name}: finding {r['id']}: 'closed' date must be set exactly when status is closed/accepted")
        app, ass = os.path.join(comp, "applicability.csv"), os.path.join(comp, "audit", "assessments.csv")
        if os.path.isfile(app):
            for r in read_csv(app)[1]:
                if f"{r['framework']}:{r['req_id']}" not in keys:
                    err("examples", f"{name}: applicability row {r['framework']}:{r['req_id']} not in catalogs")
        if os.path.isfile(app) and os.path.isfile(ass):
            got = readiness(read_csv(app)[1], read_csv(ass)[1])
            for rep in glob.glob(os.path.join(comp, "audit", "*-internal-audit-report*.md")):
                text = open(rep, encoding="utf-8").read()
                for fw, (n, sat, par, pct) in got.items():
                    label = {"soc2": "SOC 2", "dpdp": "DPDP"}.get(fw, fw)
                    row = f"| {label} | {n} | {sat} | {par} | {n - sat - par} | {pct}% |"
                    if row not in text:
                        err("examples", f"{rel(rep)}: readiness row for {fw} should be '{row}'")
    for exp in sorted(glob.glob(os.path.join(ROOT, "examples", "*", "expected.csv"))):
        h, rows = read_csv(exp)
        if h != "kind,framework,req_id,expect,why":
            err("examples", f"{rel(exp)}: header")
        for r in rows:
            if r["kind"] == "requirement" and f"{r['framework']}:{r['req_id']}" not in keys:
                err("examples", f"{rel(exp)}: unknown requirement {r['framework']}:{r['req_id']}")
            if r["kind"] == "framework" and r["expect"] not in ("in", "out", "either"):
                err("examples", f"{rel(exp)}: framework expect '{r['expect']}'")


# ---------------------------------------------------------------- skills, agents, commands
def check_markdown_units():
    for f in glob.glob(os.path.join(SK, "*", "SKILL.md")):
        text = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m or "name:" not in m.group(1) or "description:" not in m.group(1):
            err("skills", f"{rel(f)}: frontmatter needs name and description")
        elif f"name: {os.path.basename(os.path.dirname(f))}" not in m.group(1):
            err("skills", f"{rel(f)}: name must match folder")
    for f in glob.glob(os.path.join(PLUGIN, "commands", "*.md")) + glob.glob(os.path.join(PLUGIN, "agents", "*.md")):
        text = open(f, encoding="utf-8").read()
        if not text.startswith("---\n") or "description:" not in text.split("---", 2)[1]:
            err("commands", f"{rel(f)}: frontmatter with description required")
    scf = open(os.path.join(FR, "scf.md"), encoding="utf-8").read()
    m = re.search(r"<<'PY'\n(.*?)\nPY\n", scf, re.S)
    if not m:
        err("skills", "scf.md: embedded generator not found")
    else:
        try:
            ast.parse(m.group(1))
        except SyntaxError as e:
            err("skills", f"scf.md: embedded generator does not compile: {e}")


def main():
    check_manifests()
    check_templates()
    cats = load_catalogs()
    check_catalogs(cats)
    keys = valid_keys(cats)
    check_registry(cats)
    check_playbooks(keys)
    check_examples(keys)
    check_integration(cats)
    check_markdown_units()
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s)")
        sys.exit(1)
    print(f"OK: {len(cats)} catalogs ({len(keys)} requirements), playbooks, registry, examples, skills")


if __name__ == "__main__":
    main()
