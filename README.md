# Audit Ready

**Your GRC assistant inside Claude Code: scope it, collect it, audit it.**

Audit Ready is a Claude Code plugin for GRC engineers, internal auditors and consultants getting a company ready for **SOC 2**, **ISO 27001**, **DPDP**, **GDPR**, **PCI DSS**, **HIPAA**, **NIST CSF**, **NIS2**, **DORA** and India's **CERT-In**, **RBI** and **SEBI** requirements. It can also scope about 240 more frameworks through the SCF. It does the slow work a consultant or junior analyst would do: it reads the business, maps what applies, pulls evidence from systems, and tests it before the auditor does. You stay in charge, and every decision is a proposal you approve.

It runs no database, server or app. It is made of commands, skills and agents, and everything it produces is a plain Markdown or CSV file in `compliance/` that you can open, edit, and hand to an auditor.

## Install

```bash
# in Claude Code
/plugin marketplace add seccomply-ai/audit-ready-grc
/plugin install audit-ready@seccomply
```

The repository is private for now. Installing needs git access to `seccomply-ai/audit-ready-grc` (for example via `gh auth login`). Background auto-updates for a private marketplace also need a `GITHUB_TOKEN` with read access in your environment; otherwise, update manually with `/plugin marketplace update seccomply`.

To offer the plugin automatically to everyone working in a project, add this to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "seccomply": { "source": { "source": "github", "repo": "seccomply-ai/audit-ready-grc" } }
  },
  "enabledPlugins": { "audit-ready@seccomply": true }
}
```

[claude-grc-engineering](https://github.com/GRCEngClub/claude-grc-engineering) is optional. If its framework plugins (`soc2`, `iso27001`, `ind-dpdpa`) or inspectors (`aws-inspector`, `github-inspector`, ...) are installed, Audit Ready uses them, and it works the same without them.

## Frameworks

| Tier | Frameworks | What you get |
|---|---|---|
| Curated (12) | SOC 2, ISO 27001:2022, DPDP Act 2023 + Rules 2025, GDPR, PCI DSS 4.0.1, HIPAA Security Rule, NIST CSF 2.0, NIS2 (+ IR 2024/2690), DORA, CERT-In Directions, RBI (IT governance, IT outsourcing, payment data localisation), SEBI CSCRF | Hand-written catalogs: paraphrased summaries, mandatory flags, owning function, typical evidence, framework-specific applicability rules, and hand-mapped CLI evidence |
| SCF-backed (240) | Every other framework mapped by the [Secure Controls Framework](https://securecontrolsframework.com), including NIST 800-53, CIS v8.1, CMMC, FedRAMP, NYDFS, CCPA, MAS TRM, Essential 8, APRA CPS 234 | A catalog generated at scope time from the SCF crosswalk, the same data source claude-grc-engineering uses: real requirement ids with SCF wording, and no mandatory flags |

RBI, SEBI and CERT-In catalogs use thematic ids, and these regulators revise their circulars often. Verify the clause references against the latest circulars before an audit.

Every catalog row and every playbook row carries SCF control ids, so one artifact can support requirements in several frameworks. You confirm each such link.

SCF data is CC BY-ND 4.0. It is downloaded at run time into `~/.cache/claude-grc/scf/` and never shipped in this repo.

## How it works

```
1. Scoping            2. Evidence collection          3. Internal audit
/audit-ready:scope -> /audit-ready:evidence-plan  ->  /audit-ready:audit <function>
                      /audit-ready:collect [tool]
                      /audit-ready:request [owner]
                      /audit-ready:inbox
```

| Command | Pillar | What it does |
|---|---|---|
| `/audit-ready:start` | All | Sets up `compliance/` (never overwrites), adds evidence to `.gitignore`, shows status |
| `/audit-ready:scope <url>` | Scoping | Reads the website (every fact sourced), asks at most 5 questions at a time, recommends frameworks and TSC categories, drafts the Statement of Applicability and the scoping memo |
| `/audit-ready:evidence-plan` | Collection | Builds a tool-specific evidence plan from the approved scope, deduplicated across frameworks |
| `/audit-ready:collect [tool]` | Collection | Runs read-only `gh`, `aws`, `gam`, `gcloud` and `az` playbooks after you approve each command; saves raw output, redacts secrets, hashes it (SHA-256) and indexes it |
| `/audit-ready:request [owner]` | Collection | Drafts one evidence request per owner. Nothing is sent unless you ask |
| `/audit-ready:inbox` | Collection | Checks, renames, hashes and files what owners dropped into `_inbox/`, and flags mismatches |
| `/audit-ready:audit [function]` | Internal audit | Audits Engineering, IT, HR, Legal or Leadership like an external auditor would: inquiry, inspection and sample testing. It proposes verdicts and rated findings, then writes the report |
| `/audit-ready:status` | All | Readiness per framework computed from the CSVs, plus the top open items and the next step |

## Working files

```
compliance/
  profile.md               business profile, every fact with a source
  scope.md                 scoping memo: frameworks chosen and why
  applicability.csv        Statement of Applicability
  evidence-plan.csv        evidence item, requirements, method, owner, due, status
  evidence/
    _inbox/                owners drop files here
    index.csv              file, requirements, source, command, period, collected_at, sha256, redacted
    <requirement-id>/      filed artifacts
  requests/<owner>.md      drafted evidence requests
  audit/
    assessments.csv        evidence, requirement, verdict, gaps, fix, reviewer, date, approved
    findings.csv           id, requirement, severity, finding, fix, owner, status
    <date>-internal-audit-report.md
```

The CSV columns are fixed by templates. Readiness is always computed from `applicability.csv` and `assessments.csv`, never typed in by hand.

## What's inside

| Part | Contents |
|---|---|
| Skills | `grc-assistant` (rules, folder format, templates, hashing, redaction, readiness formula), `business-discovery`, `framework-reference` (registry of 252 frameworks; 12 curated catalogs with 605 requirements; SCF-backed catalogs generated on demand), `evidence-playbooks` (gh, aws, gam, gcloud, az, each row tagged with SCF ids), `internal-audit-method` (rubric, sampling, severity, report) |
| Agents | `site-researcher`, `evidence-reviewer`, `internal-auditor` |
| Examples | `examples/acme-saas` (a complete sample folder), plus scoping test briefs with expected outcomes: `kirana-pay`, `ledgerloop`, `carecadence` |
| Tests | `tests/validate_repo.py`, `tests/check_scope_result.py`, CI in `.github/workflows/validate.yml` |

## Safety and trust

- **Read-only.** Playbooks contain only get, list and describe commands, enforced by an allowlist. Claude shows every command and waits for your approval before running it.
- **No secrets.** Credentials come from your existing CLI sign-ins, never from chat. Tokens and keys are redacted before a file is saved, and you are told when that happens.
- **Personal data.** `compliance/evidence/` and `compliance/audit/` are git-ignored on start. Reports refer to people by role or count.
- **Integrity.** Every artifact gets a SHA-256 in `index.csv`, together with the exact command and the time it was collected.
- **Honest output.** Catalog text is a short paraphrase keyed to official ids, not the text of the standards. Reports are readiness assessments, not certification or legal advice. DPDP Rules commencement dates and edge cases should be confirmed with counsel.

## Out of scope (v1)

Risk register and vendor management modules, policy writing, remediation tracking, an auditor portal, continuous monitoring, and any hosted service. The P1 and P2 roadmap includes deeper claude-grc-engineering reuse, Jira, Freshservice and HRMS playbooks, and an automated leaver check.

## Development

```bash
claude plugin validate .                       # marketplace + plugin manifests
python tests/validate_repo.py                  # catalogs, read-only playbook allowlist, examples (stdlib only)
python tools/build_scf_data.py --check         # registry + curated scf_ids are up to date with the SCF cache
npx markdownlint-cli2 "**/*.md"                # same lint rules as claude-grc-engineering
```

## License

MIT. Its layout and conventions follow claude-grc-engineering (MIT, GRC Engineering Club contributors).
