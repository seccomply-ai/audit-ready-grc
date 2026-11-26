---
description: Draft one evidence request per owner for manual evidence (what, period, format, due date) - nothing is sent unless you ask
argument-hint: "[owner role or name | all]"
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Audit Ready: request

Pillar 2, collection. Writes a ready-to-send message per owner into `compliance/requests/<owner>.md` for all `method=owner` items that are still `planned`.

## Usage

```
/audit-ready:request          # all owners
/audit-ready:request HR
/audit-ready:request "Priya (Legal)"
```

## Arguments

Parse `$ARGUMENTS` as one optional owner filter. Match it case-insensitively against the `owner` column. `all` or no argument means every owner. If nothing matches, list the known owners and stop.

## Steps

1. Load the skills `audit-ready:grc-assistant` and `audit-ready:evidence-playbooks`. Validate `evidence-plan.csv`.
2. Select `method=owner` items with status `planned`, plus items with status `requested` whose `due` date has passed (these are follow-ups). Group them by `owner`.
3. For each owner, fill in `${CLAUDE_PLUGIN_ROOT}/skills/evidence-playbooks/templates/owner-request.md`:
   - one table row per item, with the `EV` id, a plain-language item, the period it must cover, an acceptable format, and a one-line "why the auditor needs it" (from the catalog summary, phrased for a non-specialist);
   - framework list and audit period from `scope.md`; the drop location `compliance/evidence/_inbox/`; the naming rule `EV-###_<short-name>.<ext>`;
   - for follow-ups, a short polite reminder line at the top.
4. Write the file to `compliance/requests/<owner-slug>.md`, where the slug is lowercase with hyphens. If the file already exists, append a dated section rather than overwriting.
5. Show each draft. After the user confirms, set those items' status to `requested` in `evidence-plan.csv`.
6. **Nothing is sent.** If the user asks to send, use an email or chat tool only when one is connected, and only after showing the exact recipient and message and getting a yes. Otherwise, tell them the drafts are ready to copy.

## Output

Print:
- `Owner | items | earliest due | file`;
- the status block;
- the next step: `/audit-ready:inbox` once files arrive.
