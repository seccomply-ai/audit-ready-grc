---
name: evidence-playbooks
description: Read-only evidence collection playbooks for gh (GitHub), aws, gam (Google Workspace), gcloud (GCP) and az (Azure) - the exact get/list/describe commands, which requirements each artifact supports across the 12 curated frameworks (SOC 2, ISO 27001, DPDP, GDPR, PCI DSS, HIPAA, NIST CSF, NIS2, DORA, CERT-In, RBI, SEBI CSCRF) plus SCF ids for any other framework, file naming, plus owner request templates for manual evidence. Use when building an evidence plan, running /audit-ready:collect, or drafting /audit-ready:request messages.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Evidence playbooks

| Playbook | CLI | Detect (signed in?) | File |
|---|---|---|---|
| GitHub | `gh` | `gh auth status` | `playbooks/gh.md` |
| AWS | `aws` | `aws sts get-caller-identity` | `playbooks/aws.md` |
| Google Workspace | `gam` (GAM7 / GAMADV-XTD3) | `gam info domain` | `playbooks/gam.md` |
| Google Cloud | `gcloud` | `gcloud auth list --filter=status:ACTIVE --format="value(account)"` | `playbooks/gcloud.md` |
| Azure | `az` | `az account show` | `playbooks/az.md` |

Find out whether a CLI is installed with `command -v <cli>` (bash) or `Get-Command <cli>` (PowerShell) before running its detect command. A CLI that is missing or not signed in is not an error. Its items become owner requests or wait until the user signs in. Never ask for credentials in chat. Credentials come only from the user's existing CLI sign-ins.

## Read-only allowlist (hard rule)

A command may run only if all of these are true:

1. It appears in a playbook, or it is a variant of a playbook command that only changes ids, regions, `--query`, `--format`, `--output`, `--jq`, pagination or filters.
2. Its verb is read-only:
   - aws: `get-*`, `list-*`, `describe-*`, plus the documented exception `iam generate-credential-report`, which only builds a report and changes no configuration;
   - gcloud: `list`, `describe`, `get-iam-policy`;
   - az: `show`, `list`, and `az rest --method get`;
   - gh: `gh api` with no `-X`, `--method`, `-f`, `-F`, `--field`, `--raw-field` or `--input` flags (any of these can turn a request into a write), never `gh api graphql` (it can carry mutations), plus `gh repo list` and `gh auth status`;
   - gam: `info`, `print`, `show`, `report`;
   - claude-grc-engineering (only when installed): exactly `node "<grc-engineer installPath>/scripts/gap-assessment.js" <framework ids> --output=json --report-dir=compliance/evidence/_staging/<dir> [--quiet] [--offline]`. It reads the local Findings cache and writes only the report folder. `--output=github-issues` is denied, and so is any `--report-dir` outside `compliance/evidence/_staging/`. Audit Ready never runs inspector `collect` scripts; the user runs those.
3. It is not on the **secret-returning denylist** below, even though its verb looks read-only.
4. It contains no shell redirection into anything other than the target evidence file, no `;`, `&&` or pipes into commands other than `jq`, `base64 -d` or `head`, and no `$( )` that runs non-allowlisted commands.

### Secret-returning denylist (never run, never "vary" a playbook command into these)

Evidence is about configuration, never about credential values.

| CLI | Denied |
|---|---|
| aws | `secretsmanager get-secret-value`, `ssm get-parameter`, `ssm get-parameters`, `ssm get-parameters-by-path` (any of these with `--with-decryption`, or on `SecureString` parameters), `kms decrypt`, `ecr get-login-password`, `ecr get-authorization-token`, `codeartifact get-authorization-token`, `sts get-session-token`, `sts get-federation-token`, `sts assume-role*`, `rds generate-db-auth-token`, `lambda get-function` and `lambda get-function-configuration` (they return environment variables), `iam get-ssh-public-key`, `cognito-idp` admin token calls |
| az | `keyvault secret show`, `keyvault secret download`, `keyvault key download`, `keyvault certificate download`, `storage account keys list`, `storage account show-connection-string`, `storage * generate-sas`, `acr credential show`, `cosmosdb keys list`, `redis list-keys`, `servicebus * keys list`, `eventhubs * keys list`, `functionapp keys list`, `functionapp function keys list`, `webapp deployment list-publishing-credentials`, `webapp deployment list-publishing-profiles`, `aks get-credentials`, `sql db show-connection-string`, `account get-access-token`, `az rest` against Key Vault data-plane URLs (`*.vault.azure.net`) |
| gcloud | `auth print-access-token`, `auth print-identity-token`, `auth application-default print-access-token`, `secrets versions access`, `container clusters get-credentials`, `sql generate-login-token`, `iam service-accounts keys get-public-key` (not needed for evidence) |
| gh | `gh auth token`, `gh api graphql`, `gh secret` (any subcommand), `gh variable get` |
| gam | `show backupcodes`, `print backupcodes`, any command that prints passwords or app-specific passwords' values |

General rule: if a command's purpose is to return a secret, token, key, password, connection string or credential, it is denied, whatever its verb. Listing the *names* or *metadata* of secrets (for example `aws secretsmanager list-secrets`, or `az keyvault secret list` without values) is allowed when a playbook row asks for it.

If anything the user asks for falls outside this list, say it is outside Audit Ready's read-only scope, and don't run it.

## Running a playbook

1. Read `compliance/applicability.csv` and `compliance/evidence-plan.csv`. Run only items whose `method=cli` and `tool` match, and which support at least one applicable requirement.
2. Fill in placeholders (`<org>`, `<repo>`, `<account>`, `<project>`, `<subscription>`, `<region>`) from `profile.md`, or ask the user. Expand loops, such as per-region or per-repo calls, into the concrete list.
3. **Show the full list of commands** in a numbered code block, grouped by plan item. Wait for explicit approval. The user may approve all, pick a subset, or edit ids.
4. Run each approved command and write its stdout to a temp file in `compliance/evidence/_staging/`. Don't print large outputs into the conversation. Read only the head, counts, or `jq` summaries.
5. If a command fails because of permissions, a missing feature or the plan tier, save stderr as `<name>.error.txt` in staging. It is not evidence. Set the plan item status to `planned` with a note, and tell the user what role or permission is missing.
6. For each successful output:
   - redact (see the grc-assistant skill);
   - move it to `compliance/evidence/<first-requirement-folder>/<YYYY-MM-DD>_<tool>_<item-slug>.<ext>`;
   - hash it;
   - append an `index.csv` row with:
     - `type`: `config` for settings exports, `population` for lists to sample from (users, PRs, leavers, alert lists), `log` for activity or audit logs. GH-08, GH-03, AWS-04, GWS-02, GWS-03 and AZ-02 are populations; GH-15, GWS-06, GWS-07 and AWS-19 jobs are logs;
     - `requirements`: every applicable requirement the item supports, including SCF links the user accepted (see "Requirement keys and SCF tags");
     - `source`: `<tool> <account/org/project>`;
     - `command`: the exact command line;
     - `period`: `point-in-time` or the date range queried;
     - `collected_at`: UTC timestamp;
     - `sha256`;
     - `redacted`.
7. Set the plan item `status=collected`. Remove `_staging/` when it is empty.

File extensions: `.json` for JSON output, `.csv` for CSV (gam, credential report), `.txt` otherwise. Always prefer `--output json`, `--format=json` or the `--json` flags so the auditor gets structured data.

## Large outputs

Never read a full large export into context. Use counts and samples:

```bash
jq 'length' file.json
jq '.[0:5]' file.json
jq '[.[] | select(.isEnforcedIn2Sv == false)] | length' file.json
wc -l file.csv
head -n 6 file.csv
```

## Requirement keys and SCF tags

Each playbook row has two mapping columns:

- **`Requirements`** holds hand-mapped keys for the curated frameworks, such as `soc2:CC6.1;iso27001:A.8.5;dpdp:DPDP-R6`.
- **`SCF`** holds the SCF control ids the artifact evidences, such as `IAC-06;IAC-02`. These link the row to **any** framework, including SCF-backed ones like PCI DSS, NIST 800-53 or DORA.

When filing:

1. Keep the `Requirements` keys that are applicable (or inherited) in `applicability.csv`.
2. For every other in-scope framework, find the applicable requirements whose `scf_ids` (in the curated or generated catalog) contain any of the row's SCF ids. Propose them as "also supports (via SCF)".
3. Show the proposed additions per file and let the user accept, trim or reject them. Write only the accepted keys into `index.csv`.

SCF links are broad hints, not proof (see `framework-reference/scf.md`). Prefer fewer, stronger links. When a requirement links to more than 3 artifacts through SCF only, offer just the 3 most specific ones, meaning those whose SCF ids share the most with the requirement's `scf_ids`.

## Manual evidence

Items that no CLI can collect (policies, HR records, training, board minutes, vendor reports, screenshots of settings in tools without a CLI) become `method=owner` plan items. Draft requests with `templates/owner-request.md` through `/audit-ready:request`.

## Integration (optional)

When claude-grc-engineering inspectors have run (`aws-inspector`, `github-inspector`, `gcp-inspector`, `azure-inspector`, `okta-inspector`, and the other connectors such as `wiz-inspector` or `tenable-inspector`), their Findings sit in `~/.cache/claude-grc/findings/<source>/<run_id>.json`, with one summary line per run in `~/.cache/claude-grc/runs.log`.

- `/audit-ready:collect import` files the newest run per source as evidence (method `import`, `type=report`, source `<source> run <run_id>`, command `imported from ~/.cache/claude-grc/findings/...`). The file is copied unchanged, then redacted, hashed and indexed.
- Findings use SCF control ids (`evaluations[].control_framework == "SCF"`), so link them to requirements through the catalogs' `scf_ids`, with the same accept-or-trim step and the 3-per-requirement limit as playbook SCF links. Non-SCF evaluations (testssl) map by exact id only.
- `/audit-ready:collect import gap` runs grc-engineer's gap-assessment engine (allowlisted above) and files `findings.normalized.json`, whose `frameworks{}` field already holds native ids for every in-scope SCF-mapped framework.
- Inspectors check configuration across every resource they can see, which complements a playbook export: prefer the inspector run as population evidence (every repo, every bucket) and the playbook export as the detailed artifact.
