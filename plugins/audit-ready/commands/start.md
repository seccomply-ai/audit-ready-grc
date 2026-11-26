---
description: Set up the compliance/ working folder, show where things stand and suggest the next step
argument-hint: "[folder]  (default: ./compliance)"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Audit Ready: start

Sets up the working folder from templates, protects evidence from git, detects optional claude-grc-engineering plugins, and shows status. Safe to re-run: it never overwrites an existing file.

## Usage

```
/audit-ready:start
/audit-ready:start path/to/compliance
```

## Arguments

Parse `$ARGUMENTS`. Accept zero or one positional argument: the folder path. Default `./compliance`. Reject more than one argument or a path that points at an existing regular file, with a short usage error.

## Steps

1. Load the `audit-ready:grc-assistant` skill and follow its operating rules.
2. **Create missing folders** (never delete or overwrite): `compliance/`, `compliance/catalogs/`, `compliance/evidence/`, `compliance/evidence/_inbox/`, `compliance/requests/`, `compliance/audit/`.
3. **Create missing files** by copying the templates in `${CLAUDE_PLUGIN_ROOT}/skills/grc-assistant/templates/` verbatim:
   - `applicability.csv` → `compliance/applicability.csv`
   - `evidence-plan.csv` → `compliance/evidence-plan.csv`
   - `index.csv` → `compliance/evidence/index.csv`
   - `assessments.csv` → `compliance/audit/assessments.csv`
   - `findings.csv` → `compliance/audit/findings.csv`
   - `README.md` → `compliance/README.md`
   For each target, check existence first (Glob or Read). If it exists, leave it untouched and note "kept". `profile.md` and `scope.md` are created later by `/audit-ready:scope`, not here.
4. **Protect evidence.** Read `.gitignore` at the working-directory root (create it if missing). Append only the lines that are not already present:
   ```
   # Audit Ready: evidence and audit working files can contain personal data;
   # generated catalogs contain SCF text (CC BY-ND 4.0)
   compliance/evidence/
   compliance/audit/
   compliance/catalogs/
   ```
   Tell the user what was added. Remind them once: never commit evidence; use an encrypted, access-controlled evidence locker.
5. **Validate** existing CSVs against the templates (see "Validate before continuing" in the skill). Report problems; do not repair silently.
6. **Detect integration** as described in the skill's "Integration with claude-grc-engineering" section. Print one line, e.g. `claude-grc-engineering: soc2, pci-dss, github-inspector found (will be used when helpful)` or `claude-grc-engineering: not installed (optional)`. Also print whether the SCF cache exists, for example `SCF cache: 2026.1 (controls + 4 crosswalks)` or `SCF cache: empty (downloaded when a non-curated framework is scoped)`.
7. **Show status** using the same computation as `/audit-ready:status` and suggest the next command:
   - no `profile.md` → `/audit-ready:scope <company website>`
   - scope not approved → finish `/audit-ready:scope`
   - empty plan → `/audit-ready:evidence-plan`
   - planned CLI items → `/audit-ready:collect`
   - planned owner items → `/audit-ready:request`
   - files in `_inbox/` → `/audit-ready:inbox`
   - collected evidence but no assessments → `/audit-ready:audit`

## Output

A short list of created vs kept paths, the `.gitignore` change, the integration line, and the status block from the skill.
