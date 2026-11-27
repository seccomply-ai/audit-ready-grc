<p align="center">
  <img src="assets/icon-128.png" alt="Audit Ready icon" width="96" height="96">
</p>

<h1 align="center">Audit Ready</h1>

<p align="center"><b>Your GRC assistant inside Claude Code. Scope it, collect it, audit it.</b></p>

<p align="center">
  <a href="https://github.com/seccomply-ai/audit-ready-grc/actions/workflows/validate.yml"><img src="https://github.com/seccomply-ai/audit-ready-grc/actions/workflows/validate.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/seccomply-ai/audit-ready-grc/releases/latest"><img src="https://img.shields.io/github/v/release/seccomply-ai/audit-ready-grc?labelColor=171717&color=FF570A" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-1f6feb?labelColor=171717" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-FF570A?labelColor=171717" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/frameworks-13%20curated%20%2B%20239%20via%20SCF-1f6feb?labelColor=171717" alt="Frameworks">
</p>

Audit Ready gets a company ready for its compliance audit from inside Claude Code. It reads the business, works out which frameworks and requirements apply, collects evidence from the systems you already use, and tests that evidence the way an external auditor would. That's the slow work a consultant or junior analyst usually does. You stay in charge: every decision is a proposal you approve.

There is no server, database or app. Audit Ready is made of commands, skills and agents, and everything it produces is a plain Markdown or CSV file in a `compliance/` folder that you can open, edit and hand to your auditor.

**Curated frameworks:** SOC 2, ISO 27001, ISO 42001 (AI), GDPR, PCI DSS 4.0.1, HIPAA, NIST CSF 2.0, NIS2, DORA, and India's DPDP, CERT-In, RBI and SEBI CSCRF. **239 more** (NIST 800-53, CIS, CMMC, FedRAMP, NYDFS, CCPA, ...) through the Secure Controls Framework.

> Not affiliated with Anthropic, the AICPA, ISO or any regulator. Outputs are readiness assessments, not certification or legal advice.

## What it does

| Pillar | What happens | Commands |
|---|---|---|
| **1. Scoping** | Reads the company website (every fact cites its source), asks only what the site can't show, recommends frameworks with reasons, and drafts the Statement of Applicability and a scoping memo | `start`, `scope` |
| **2. Evidence collection** | Turns the scope into one deduplicated evidence plan, runs read-only `gh`, `aws`, `gam`, `gcloud` and `az` commands after you approve them, drafts requests to evidence owners, and files what they send back. Every file is redacted, hashed and indexed | `evidence-plan`, `collect`, `request`, `inbox` |
| **3. Internal audit** | Audits one business function at a time with inquiry, inspection and sample testing; proposes verdicts and rated findings; writes the internal audit report after you approve | `audit` |
| **Hand-off** | Shows readiness per framework computed from the files, and builds an encrypted, hash-verified evidence bundle for the auditor | `status`, `package` |

```text
company website + your answers
        ↓
profile.md · applicability.csv (SoA) · scope.md
        ↓
evidence-plan.csv
        ↓
read-only CLI collection · owner requests · _inbox · inspector imports
        ↓  (redact · SHA-256 · index.csv)
evidence-reviewer + internal-auditor agents
        ↓
assessments.csv · findings.csv · internal audit report
        ↓
/audit-ready:status   ·   /audit-ready:package → encrypted bundle for the auditor
```

## Install in 60 seconds

Inside Claude Code:

```bash
/plugin marketplace add seccomply-ai/audit-ready-grc
/plugin install audit-ready@seccomply
```

Restart Claude Code, then type `/audit-ready:` to see the nine commands.

**First run without any credentials:** try it on the fictional sample company.

```bash
git clone https://github.com/seccomply-ai/audit-ready-grc
mkdir ~/ar-demo && cp -r audit-ready-grc/examples/acme-saas/compliance ~/ar-demo/
cd ~/ar-demo && claude
```

```bash
/audit-ready:status                 # readiness computed from the sample files
/audit-ready:audit Engineering      # a mock audit of one function
```

**First run on a real company:**

```bash
/audit-ready:start
/audit-ready:scope https://your-company.example
/audit-ready:evidence-plan
/audit-ready:collect gh             # read-only; you approve every command first
```

Update later with `/plugin marketplace update seccomply`.

<details>
<summary><b>Team setup: offer the plugin to everyone in a project</b></summary>

Add this to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "seccomply": { "source": { "source": "github", "repo": "seccomply-ai/audit-ready-grc" } }
  },
  "enabledPlugins": { "audit-ready@seccomply": true }
}
```

</details>

## Common workflows

| Goal | Command |
|---|---|
| Set up the working folder and see where things stand | `/audit-ready:start` |
| Scope a company and draft the Statement of Applicability | `/audit-ready:scope <url>` |
| Add any SCF-mapped framework (NIST 800-53, CIS, CMMC, ...) | `/audit-ready:scope` and name the framework |
| Plan evidence once for several frameworks | `/audit-ready:evidence-plan` |
| Collect from GitHub, AWS, Google Workspace, GCP or Azure | `/audit-ready:collect gh` (or `aws`, `gam`, `gcloud`, `az`) |
| Ask people for policies, HR records and other manual evidence | `/audit-ready:request [owner]` |
| File what owners sent back | `/audit-ready:inbox` |
| File claude-grc-engineering inspector results | `/audit-ready:collect import` |
| Run grc-engineer's gap assessment and file it as evidence | `/audit-ready:collect import gap` |
| Mock-audit a function (Engineering, IT, HR, Legal, Leadership) | `/audit-ready:audit <function>` |
| Write the internal audit report | `/audit-ready:audit --report` |
| See readiness per framework and the top open items | `/audit-ready:status` |
| Give the auditor an encrypted, hash-verified evidence bundle | `/audit-ready:package <gpg fingerprint>` |

Each command's full runbook is in [`plugins/audit-ready/commands/`](plugins/audit-ready/commands/).

## Frameworks

| Tier | Frameworks | What you get |
|---|---|---|
| **Curated (13)** | SOC 2 (TSC 2017), ISO 27001:2022, ISO/IEC 42001:2023, DPDP Act 2023 + Rules 2025, GDPR, PCI DSS 4.0.1, HIPAA Security + Breach Notification Rules, NIST CSF 2.0, NIS2 (+ IR 2024/2690), DORA, CERT-In Directions, RBI, SEBI CSCRF | Hand-written catalogs (677 requirements): paraphrased summaries, mandatory flags, owning function, typical evidence, framework-specific applicability rules, entity-derived locks, and hand-mapped CLI evidence |
| **SCF-backed (239)** | Every other framework mapped by the [Secure Controls Framework](https://securecontrolsframework.com), including NIST 800-53, CIS v8.1, CMMC, FedRAMP, NYDFS, CCPA, MAS TRM, Essential 8 and APRA CPS 234 | A catalog generated when you scope it, from the SCF crosswalk: real requirement ids with SCF wording, and no mandatory flags |

- **Cross-framework evidence.** Every catalog row and every playbook row carries SCF control ids, so one artifact can support requirements in several frameworks. Audit Ready proposes those links, and you confirm them.
- **India catalogs.** RBI, SEBI and CERT-In use thematic ids, with the official clause in each row. They were [source-checked on 27 Nov 2026](docs/reviews/india-catalogs-2026-11.md), which is not legal sign-off. RBI's 2023 master directions were replaced in 2025–26 by entity-specific directions, so confirm the current text before an audit.
- **SCF data** (CC BY-ND 4.0) comes from the GRC Engineering Club's community API mirror, not an official SCF release. It is downloaded at run time into `~/.cache/claude-grc/scf/<version>/` and never shipped in this repo.

## Works with claude-grc-engineering

[claude-grc-engineering](https://github.com/GRCEngClub/claude-grc-engineering) is optional, and Audit Ready works the same without it. When it is installed:

- **Inspector results become evidence.** `/audit-ready:collect import` files the newest `aws-`, `github-`, `gcp-`, `azure-`, `okta-` (and other) inspector runs, and flags runs older than 30 days.
- **Gap assessments become evidence.** `/audit-ready:collect import gap` runs grc-engineer's `gap-assessment.js` (allowlisted, writing only to a staging folder) and files its requirement-level report.
- **Failures become proposed findings.** `/audit-ready:audit` turns failing inspector checks into rated findings, with the inspector's remediation as the starting fix.
- **Stale data is flagged.** `/audit-ready:status` shows each inspector's last run.
- **Encrypted hand-off.** `/audit-ready:package` uses grc-engineer's `package-evidence.py`.
- **Second opinions.** Framework plugins (`soc2`, `iso27001`, `pci-dss`, `gdpr`, `ind-dpdpa`, ...) are offered as cross-checks during scoping and planning.

The two plugins meet on SCF control ids:

```text
inspector Finding v1  →  evaluations[].control_id (SCF, e.g. MON-01.4)
                      →  catalog rows whose scf_ids contain it
                      →  requirements in applicability.csv (e.g. soc2:CC7.2, iso27001:A.8.15)
```

## Your working files

```text
compliance/
  profile.md               business profile, every fact with a source
  scope.md                 scoping memo: frameworks chosen and why
  applicability.csv        Statement of Applicability
  evidence-plan.csv        evidence item, requirements, method, owner, due, status
  catalogs/                generated catalogs for SCF-backed frameworks
  evidence/
    _inbox/                owners drop files here
    index.csv              file, type, requirements, source, command, period, collected_at, sha256, redacted
    <framework>_<req_id>/  filed artifacts
  requests/<owner>.md      drafted evidence requests
  audit/
    assessments.csv        evidence, requirement, verdict, gaps, fix, reviewer, date, approved
    findings.csv           id, requirement, severity, finding, fix, owner, status, opened, due, closed (append-only)
    <date>-internal-audit-report.md
```

The CSV columns are fixed by templates. Readiness is always computed from `applicability.csv` and `assessments.csv`, never typed in. A requirement scores only as well as its weakest in-scope system.

## Safety and trust

- **Read-only.** Playbooks contain only get, list and describe commands. An allowlist and a secret-returning denylist enforce this, and CI checks every playbook command. Claude shows every command and waits for your approval.
- **No secrets.** Credentials come from your existing CLI sign-ins, never from chat. Tokens and keys are redacted before a file is saved, and you are told when that happens.
- **Nothing leaves your machine.** Requests are drafted, not sent. The evidence package is written locally, and you deliver it.
- **Personal data.** `compliance/evidence/`, `compliance/audit/` and `compliance/catalogs/` are git-ignored on start. Reports refer to people by role or count.
- **Integrity.** Every artifact gets a SHA-256 in `index.csv` with the exact command and collection time. The audit fails altered evidence, and the package refuses it.
- **Honest output.** Catalog text paraphrases official ids and never reproduces the standards. Reports are readiness assessments, not certification or legal advice.

## What's inside

| Part | Contents |
|---|---|
| [Commands](plugins/audit-ready/commands/) | `start`, `scope`, `evidence-plan`, `collect`, `request`, `inbox`, `audit`, `status`, `package` |
| [Skills](plugins/audit-ready/skills/) | `grc-assistant` (rules, templates, hashing, redaction, readiness), `business-discovery` (website reading, question bank, signal to scope), `framework-reference` (registry of 252 frameworks, 13 curated catalogs, SCF generator), `evidence-playbooks` (77 read-only CLI rows across gh, aws, gam, gcloud, az), `internal-audit-method` (rubric, sampling, severity, report) |
| [Agents](plugins/audit-ready/agents/) | `site-researcher`, `evidence-reviewer`, `internal-auditor` |
| [Examples](examples/) | `acme-saas` (a complete sample folder), plus scoping briefs with expected outcomes: `kirana-pay`, `ledgerloop`, `carecadence` |
| [Tests](tests/) | Static repo checks, a scoping-result checker, fixtures, and a manual end-to-end test plan |

## Documentation

- [CHANGELOG.md](CHANGELOG.md): what changed in each release, including schema changes
- [tests/e2e-test-plan.md](tests/e2e-test-plan.md): step-by-step manual test of every command
- [tests/README.md](tests/README.md): automated checks and the scoping test
- [docs/framework-expansion-plan.md](docs/framework-expansion-plan.md): how the curated and SCF-backed tiers were designed
- [docs/reviews/india-catalogs-2026-11.md](docs/reviews/india-catalogs-2026-11.md): source check of the CERT-In, RBI and SEBI catalogs
- [scf.md](plugins/audit-ready/skills/framework-reference/scf.md): SCF data source, licence, generator and known data issues

## Roadmap

- Rebase the RBI catalog onto the 2025 and 2026 entity-specific directions, and add the India obligations that have no row yet.
- Jira, Freshservice and HRMS playbooks.
- An automated leaver check: HR leavers list against account removals.

**Out of scope for v1:** risk register and vendor management modules, policy writing, remediation tracking beyond `findings.csv`, an auditor portal, continuous monitoring, and any hosted service.

## Contributing

Contributions from GRC practitioners, auditors and security engineers are welcome. The most useful are:

- **Catalog corrections** with a citation to the official source.
- **New playbook rows.** They must be read-only; the validator rejects write verbs, write flags and secret-returning commands.
- **New curated catalogs.** Add the CSV, register it in `CURATED` in `tools/build_scf_data.py` and `EXPECTED_ROWS` in `tests/validate_repo.py`, then update the tables in `framework-reference/SKILL.md`.
- **Example briefs** with an `expected.csv`, so scoping can be tested.

Before opening a pull request:

```bash
claude plugin validate .                       # marketplace and plugin manifests
python tests/validate_repo.py                  # catalogs, read-only allowlist, examples, fixtures (stdlib only)
python tools/build_scf_data.py --check         # registry and curated scf_ids match the SCF cache
npx markdownlint-cli2 "**/*.md"                # same rules as claude-grc-engineering
```

## Status

Pre-1.0 (currently 0.3.0). The `compliance/` CSV columns are versioned, and every change to them is listed in the [CHANGELOG](CHANGELOG.md).

## License

MIT. The layout and conventions follow [claude-grc-engineering](https://github.com/GRCEngClub/claude-grc-engineering) (MIT, GRC Engineering Club contributors). SCF data is licensed CC BY-ND 4.0 by the Secure Controls Framework Council; it is downloaded at run time and never redistributed here.
