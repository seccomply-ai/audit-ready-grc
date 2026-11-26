---
description: Run read-only CLI playbooks (gh, aws, gam, gcloud, az) for planned evidence items after you approve the exact commands; save raw output, redact, hash and index it
argument-hint: "[gh|aws|gam|gcloud|az|import|all] [EV-###...]"
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
```

## Arguments

Parse `$ARGUMENTS`:
- The first token may be `gh`, `aws`, `gam`, `gcloud`, `az`, `import` or `all` (the default is `all`).
- Any further tokens must be plan ids of the form `EV-\d{3,}`.
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

### `import` mode

- Look for `~/.cache/claude-grc/findings/<source>/*.json` from claude-grc-engineering inspectors. Show the newest run per source, with its `collected_at` and finding count.
- After approval, copy each file unchanged into `evidence/<first-mapped-req>/<YYYY-MM-DD>_import_<source>.json`.
- Map `evaluations[].control_framework` / `control_id` to catalog keys, keeping only exact matches with applicable requirements.
- Then hash and index with method note `imported from <path>`, and add `method=import` plan items when there's no matching item.

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
