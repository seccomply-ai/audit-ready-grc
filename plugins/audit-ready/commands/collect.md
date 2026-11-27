---
description: Run read-only CLI playbooks (gh, aws, gam, gcloud, az) for planned evidence items after you approve the exact commands; save raw output, redact, hash and index it
argument-hint: "[gh|aws|gam|gcloud|az|import [gap]|all] [EV-###...]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Audit Ready: collect

Pillar 2, collection. Automatic evidence from CLIs the user is already signed in to. It is read-only, it shows every command first, and it saves the raw output exactly as returned.

## Usage

```
/audit-ready:collect              # detect signed-in tools, offer what can run
/audit-ready:collect gh           # only GitHub items
/audit-ready:collect aws EV-014 EV-015
/audit-ready:collect import       # file cached claude-grc-engineering inspector findings
/audit-ready:collect import gap   # run grc-engineer gap-assessment over them and file the report
```

## Arguments

Parse `$ARGUMENTS`:
- The first token may be `gh`, `aws`, `gam`, `gcloud`, `az`, `import` or `all` (the default is `all`).
- After `import`, the only allowed token is `gap`.
- Otherwise any further tokens must be plan ids of the form `EV-\d{3,}`.
- Reject unknown tools, malformed ids, or ids that are not `method=cli` items for that tool.

## Preconditions

- `evidence-plan.csv` has `method=cli` items with status `planned`, unless you are running `import`. If it doesn't, suggest `/audit-ready:evidence-plan`.
- Load the skills `audit-ready:grc-assistant` and `audit-ready:evidence-playbooks`, plus the playbook files for the selected tools. Validate the CSVs.

## Steps

1. **Detect tools.**
   - For each selected tool, check that it is installed, then run its detect command. Show a table: `tool | installed | signed in as | items planned`.
   - The detect commands are read-only, but list them and get approval before the first run in a session.
2. **Resolve placeholders.**
   - Fill in org, repo, account, project, subscription and region from `profile.md` and the detect output.
   - Ask for anything still missing (at most 5 questions).
   - Expand per-region, per-repo and per-bucket loops into concrete commands. List commands (such as `list-buckets`) may need to run first, so do this in two approval rounds if needed.
3. **Show the plan.** Print a numbered code block with every exact command, grouped by `EV` id with the playbook id. Check every line against the read-only allowlist in the skill and drop anything that fails, saying so. Ask: run all, a subset (by number), or cancel.
4. **Run** only the approved commands. Write stdout to `compliance/evidence/_staging/<name>`. Keep outputs out of the conversation and look only at counts and heads.
5. **File each result.** Follow "Running a playbook" steps 5–7 in the skill:
   - handle errors as `.error.txt` notes, not evidence;
   - redact;
   - move to `evidence/<first-req-folder>/<YYYY-MM-DD>_<tool>_<slug>.<ext>`;
   - hash with sha256;
   - propose "also supports (via SCF)" requirement keys for other in-scope frameworks, and let the user trim them;
   - append to `index.csv`;
   - set the plan status to `collected`.
6. **Quick look (not a verdict).** For each file, give one line on what it shows, such as "2 of 41 active users lack 2SV enforcement". Label these "observations for the audit". Verdicts come from `/audit-ready:audit`.

### `import` mode (claude-grc-engineering inspectors)

Inspector Findings are keyed by **SCF** control ids, not framework ids, so they are mapped to requirements through the catalogs' `scf_ids`.

1. **Find runs.** Read `~/.cache/claude-grc/runs.log` (one JSON line per run: `source`, `run_id`, `started_at`, `resources`, `counters{pass,fail,inconclusive}`) and pick the newest run per source. Its file is `~/.cache/claude-grc/findings/<source>/<run_id>.json`. If `runs.log` is missing, take the newest file per source folder. Show a table: `source | run_id | age | resources | pass | fail | inconclusive`.
2. **Freshness.** Warn when a run is older than 30 days, or ended before the audit period in `scope.md`. Suggest the user re-run `/<source>:collect` themselves; Audit Ready never runs inspectors.
3. **Read the file without loading it all.** It is a JSON array of Finding v1 documents: `source`, `run_id`, `collected_at`, `resource{type,id}`, and `evaluations[{control_framework, control_id, status, severity, message, remediation{summary}}]`. Use `jq` summaries, for example:

   ```bash
   jq -r '.[] | .resource.id as $r | .evaluations[] | [$r, .control_framework, .control_id, .status, (.severity // "")] | @tsv' <file>
   ```

4. **Map to requirements.**
   - `control_framework == "SCF"`: a requirement matches when its catalog row (curated, or generated in `compliance/catalogs/`) lists the `control_id` in `scf_ids`, and it is applicable or inherited in `applicability.csv`.
   - Any other `control_framework` (only testssl emits these): exact id match only.
   - Propose the matches per run and let the user accept or trim them. Offer at most 3 runs per requirement through SCF only, the most specific first (see the evidence-playbooks skill, "Requirement keys and SCF tags").
5. **File.** After approval, copy each run file unchanged to `evidence/<first-mapped-req-folder>/<YYYY-MM-DD>_import_<source>.json`, then redact, hash and index it:
   - `type=report`;
   - `source`: `<source> run <run_id>`;
   - `command`: `imported from ~/.cache/claude-grc/findings/<source>/<run_id>.json`;
   - `period`: `point-in-time`; `collected_at`: the run's `collected_at`.
   Add a `method=import` plan item when no plan item covers it.
6. **Quick look.** One line per run: resources, failing evaluations by severity, and the requirements they touch. Verdicts come from `/audit-ready:audit`.

### `import gap` mode (claude-grc-engineering gap assessment)

Needs `grc-engineer` installed. Its gap-assessment engine resolves every cached inspector result to native framework ids, which gives the auditor one requirement-level report.

1. Read `installPath` for the `grc-engineer@...` key in `~/.claude/plugins/installed_plugins.json`.
2. Build the framework list from the in-scope frameworks: the `scf_framework_id` column of `framework-reference/frameworks.csv` (curated rows such as SOC 2 use `general-aicpa-tsc-2017`; ISO 27001 Annex A uses `general-iso-27002-2022`). Frameworks with no SCF id (CERT-In, RBI, SEBI) are skipped and said so.
3. Show this one command and wait for approval:

   ```bash
   node "<installPath>/scripts/gap-assessment.js" <fid1>,<fid2> --output=json --report-dir=compliance/evidence/_staging/gap --quiet
   ```

   It reads the local Findings cache and the public SCF API, and writes only into the staging folder. Never use `--output=github-issues` (it can open GitHub issues) and never point `--report-dir` outside `_staging`. Add `--offline` only when the SCF cache already holds every control file.
4. File `_staging/gap/findings.normalized.json` as `evidence/<first-mapped-req-folder>/<YYYY-MM-DD>_import_gap-assessment.json` (`type=report`, source `grc-engineer gap-assessment <run_id>`, command as run). Delete the rest of the staging bundle.
5. **Map.** The file has `tier1`, `tier2`, `tier3`, `passes` and `inconclusive` arrays. Each item has `scf_id`, `status`, `severity`, `frameworks{<fid>: [native ids]}` and `failing_resources[{source, resource_id, message, remediation{summary}}]`.
   - Native ids first: roll them up to the catalog's id (drop SOC 2 point-of-focus suffixes, `CC7.2-POF2` → `CC7.2`; prefix ISO 27002 ids with `A.`, `8.15` → `A.8.15`; for SCF-backed frameworks use the same granularity as `compliance/catalogs/<key>.csv`).
   - Then `scf_ids` for anything the native ids did not reach.
   - Keep only applicable requirements, and let the user trim the list as above.
6. Show the per-framework `stats` from the command output (`evaluated`, `passing`, `failing`, `coverage_pct`) as context, labelled "inspector coverage, not readiness".

## Output

Print:
- a table `EV id | file | requirements | sha256 (first 12) | redacted`;
- failures with the permission or feature that was missing;
- the status block;
- the next step: `/audit-ready:request` for owner items, or `/audit-ready:audit` once enough evidence is in.

## Guardrails

- No command runs before the user approves it. Approval covers only the commands shown.
- Never change cloud, GitHub or Workspace settings, even to "fix" what you just saw.
- Never print secrets. If an output contains one, redact it before filing and tell the user.
- Never edit a filed evidence file after hashing. Recollect it instead; the new file gets a new date and a new row.
