---
description: Scope a company for compliance - read its website, ask what the site can't show, recommend frameworks, draft the Statement of Applicability and the scoping memo
argument-hint: "<company website url>"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebFetch, WebSearch, Agent
---

# Audit Ready: scope

Pillar 1, scoping. It turns a website and a few answers into `profile.md`, `applicability.csv` and `scope.md`. Every decision is a proposal the user approves.

## Usage

```
/audit-ready:scope https://acme.example
/audit-ready:scope            # resume an unfinished scoping
```

## Arguments

Parse `$ARGUMENTS`. Accept zero or one argument: a URL.

- If the URL has no scheme, add `https://`.
- Reject anything that isn't an http(s) URL or a bare domain.
- With no argument:
  - if `profile.md` exists, resume at the first unfinished step below;
  - otherwise ask for the website.

If `compliance/` doesn't exist, run the folder setup from `/audit-ready:start` first (create only, never overwrite).

## Steps

Load the skills `audit-ready:grc-assistant`, `audit-ready:business-discovery` and `audit-ready:framework-reference`. Re-read any existing `profile.md`, `applicability.csv` and `scope.md`, and validate them.

### Step 1: research the site

Launch the `audit-ready:site-researcher` agent with the URL. Tell it to read `${CLAUDE_PLUGIN_ROOT}/skills/business-discovery/SKILL.md`. Receive its sourced profile draft. If `profile.md` already exists and is confirmed, show only what's new or different, and ask before changing it.

### Step 2: fill the gaps

Compare the draft with the `profile.md` template. Pick unanswered questions from `references/question-bank.md`. Ask at most 5 per round, each with its "why it matters". Repeat rounds until the systems, people and audit-context sections are answered or the user says "unknown". Answers get the source `user`.

### Step 3: confirm and write the profile

Show the full profile as tables. After the user confirms, write `compliance/profile.md` from the template with the status `confirmed on <today> by user`. Nothing is saved before confirmation.

### Step 4: recommend frameworks

Use the framework-reference rules and `signal-to-scope.md`. Present a table:

`Framework | Tier (curated / SCF) | Recommend? | Reason (profile fact + source)`

Include:
- the SOC 2 TSC categories, each with its reason;
- Type I vs Type II and the proposed period;
- any further frameworks the signals point to, such as PCI DSS, GDPR, HIPAA or DORA, each with its tier from `frameworks.csv`.

The user may also name any other framework. Look it up in `frameworks.csv`:
- Not in the registry: say it isn't supported and offer the closest alternative. Never invent requirement ids.
- For curated frameworks, ask the framework-specific questions (Q16–Q24 in the question bank) before drafting applicability, then apply "Framework-specific applicability" in framework-reference.
- Several matches (for example CIS IG1, IG2 or IG3): ask which one.

The user picks. Record the choice.

### Step 4b: build SCF-backed catalogs

For each chosen framework with `tier=scf`, follow `framework-reference/scf.md`:

1. Check the SCF cache. Fetch any missing files after showing the download command and getting approval.
2. Propose a granularity: `rollup` by default, or `rollup2` for deeply dotted ids such as PCI DSS.
3. Run the generator, after approval, to write `compliance/catalogs/<key>.csv`.
4. Report the row count. If it's over 200 rows, offer a coarser mode.
5. If the framework's `base_plugin` is installed, mention its specialist commands, such as `/pci-dss:saq-select`.

### Step 5: draft applicability

For each chosen framework, read its catalog: shipped `catalogs/<key>.csv` for curated frameworks, or `compliance/catalogs/<key>.csv` for SCF-backed ones. Propose one `applicability.csv` row per requirement. For SCF-backed rows there are no mandatory flags: propose `yes`, and use `no` only with a concrete profile reason.

- **Mandatory rows:** `applicable=yes`, reason `mandatory`, locked. If the user asks to exclude one, refuse and explain.
- **Entity-derived locks:** apply "Entity-derived locks" in framework-reference, for PCI DSS (SAQ type), DORA, RBI, SEBI CSCRF, and the conditional HIPAA, NIS2 and CERT-In rows. Write the locked rows with `mandatory=yes` and reason `mandatory (entity: <type>)` or `mandatory (contract: <customer>)`. If the entity answer is unknown, lock nothing and keep the question open.
- **Inherited rows:** name the vendor (for example, "AWS SOC 2 Type II report; physical data centre security").
- **`no` rows:** give a concrete reason citing a profile fact.
- **Unknowns:** default to `yes`, plus an open question.

Show the user a compact summary rather than every row:
- counts per framework;
- the full list of `no` and `inherited` rows with their reasons;
- the open questions.

Let them change any non-mandatory row. Then write `applicability.csv`. Use the `approved_by` value `user` and `approved_at` set to today, for rows approved in this session only.

### Step 6: write the scoping memo

Fill the `scope.md` template:
- frameworks and reasons, with the tier. For SCF-backed frameworks, add the line "SCF-backed catalog: <display_name>, SCF crosswalk <version>, generated <date>, <n> rows (<mode>); requirement text is SCF wording. Verify against the official standard";
- system boundary;
- inherited controls;
- applicability summary computed from the CSV;
- exclusions with reasons;
- assumptions;
- next steps.

Show it. After approval, set `Status: approved on <today> by user`. If the user wants changes, edit and show again.

## Output

At the end, print:
- the paths written;
- the applicability counts per framework;
- any open questions still unresolved;
- the status block;
- `Next: /audit-ready:evidence-plan`.

## Guardrails

- Never mark anything approved without an explicit yes from the user in this session.
- Every fact in `profile.md` has a URL or `user` as its source.
- Catalog summaries are paraphrases. Don't present them as the standard's wording.
- This is readiness scoping, not legal advice. For DPDP applicability edge cases, such as significant data fiduciary status or exemptions, recommend that the user confirm with counsel.
