# Changelog

## 0.2.0 - 2026-11-26

Fixes from an external review of 0.1.0 plus Phases A–C. The base for curated `scf_ids` is SCF 2026.1 (via the community API mirror).

- **Readiness uses the worst verdict.** A requirement scores 1 only if every current verdict satisfies, and at most 0.5 until every in-scope system has evidence. The internal auditor adds `(none: <system>)` rows for systems with no evidence. As a result, the acme-saas example's SOC 2 readiness drops from 6% to 4%.
- **Read-only allowlist hardened.**
  - gh: `--field`, `--raw-field` and `gh api graphql` are denied.
  - A new denylist covers secret-returning commands that look read-only (`secretsmanager get-secret-value`, `ssm get-parameter`, `keyvault secret show`, `storage account keys list`, `acr credential show`, `auth print-access-token`, `gh auth token`, ...).
  - `tests/validate_repo.py` enforces both.
- **HIPAA Breach Notification Rule** added (§164.402–414; 69 rows). §164.410 is locked for business associates. The Privacy Rule is stated as out of scope.
- **Entity-derived mandatory locks** for PCI DSS (SAQ type), DORA, RBI and SEBI CSCRF, plus the conditional HIPAA, NIS2 and CERT-In rows. Locked rows are written with `mandatory=yes` and the reason `mandatory (entity: ...)` or `mandatory (contract: ...)`. The scope checker fails a locked row set to `no`.
- **Sampling.**
  - Systematic interval selection only, with an exact `jq`, `sort` or `sed` recipe and a fixed start `s = floor(k/2)`.
  - Seeded random removed.
  - Readiness minimums raised (monthly 3, weekly 10, daily 25), with typical auditor ranges shown alongside.
- **`findings.csv`** gains `opened`, `due` and `closed`. It is append-only: the last row per id is the current state.
- **`index.csv`** gains `type` (`config`, `population`, `log`, `policy`, `procedure`, `record`, `report`, `screenshot`, `other`). The inquiry step uses `type` = `policy` or `procedure`.
- **SCF source** is described as the GRC Engineering Club community mirror. The version is read from `summary.json`, not assumed.
- **Windows-safe SCF commands:** `python` with an interpreter check, `$HOME` instead of `~`, and PowerShell variants.
- **Redaction** adds Slack, Azure SAS and `AccountKey`, Stripe, basic-auth URLs, and normalised key names (`private_key`, `private_key_id`, `client_secret`).
- **Consistency fixes:**
  - evidence folder examples use `<framework>_<req_id>/`;
  - a single hash-mismatch gap text;
  - ISO 4.1 and 4.2 mention the climate-change amendment (Amd 1:2024).
- **Descriptions** in `plugin.json`, the marketplace and the READMEs list all 12 curated frameworks.

## Unreleased: framework expansion, Phase C

- New test briefs:
  - `examples/ledgerloop`: EU ICT supplier, covering DORA supplier mode, GDPR controller and processor, an NIS2 open question, a PCI negative case, and CERT-In and DPDP for an India subsidiary.
  - `examples/carecadence`: US health-tech business associate, covering HIPAA addressable specs, PCI SAQ A, SOC 2 categories and a NIST CSF target tier.
- An `expected.csv` for every example. `tests/check_scope_result.py` checks a real scoping run against it, and always enforces "reason for every no/inherited" and "mandatory rows are no only with an entity-scope reason".
- `tests/validate_repo.py`, stdlib only, runs static checks: manifests, templates, catalogs (row counts, allowed values, mandatory rules), registry, playbooks (requirement keys plus the **read-only command allowlist**), example hashes and readiness numbers, skill frontmatter, and the embedded generator compiling.
- CI workflow: static checks, markdownlint, and an informational SCF freshness check pinned to SCF 2026.1 and base-repo commit 79ac7a7.
- PCI SAQ A note: the January 2025 revision replaced 6.4.3 and 11.6.1 with an eligibility confirmation.

## Framework expansion, Phase B

- Nine new curated catalogs:

  | Catalog | Rows |
  |---|---|
  | GDPR | 38 articles |
  | PCI DSS 4.0.1 | 71 requirements |
  | HIPAA Security Rule | 62 standards and specs |
  | NIST CSF 2.0 | 106 subcategories |
  | NIS2 | 35 rows (Arts 20, 21, 23, 24 + IR 2024/2690 annex) |
  | DORA | 28 articles |
  | CERT-In Directions 2022 | 7 obligations |
  | RBI | 26 rows (IT governance MD 2023, IT outsourcing MD 2023, payment data storage 2018) |
  | SEBI CSCRF | 21 rows |

- The registry now has 12 curated and 240 SCF-backed frameworks.
- `scf_ids` for the new catalogs: computed from the SCF crosswalks (NIS2 from two crosswalks), and hand-mapped and validated for CERT-In, RBI and SEBI.
- All 77 CLI playbook rows now carry hand-mapped requirement keys for the new curated frameworks, because SCF links alone gave uneven coverage (GDPR 1 of 38).
- Framework-specific applicability rules:
  - GDPR: controller vs processor;
  - PCI DSS: SAQ type;
  - HIPAA: addressable specs;
  - NIST CSF: target profile;
  - NIS2: entity classification and the IR annex;
  - DORA: financial entity vs ICT supplier;
  - CERT-In: provider types;
  - RBI: regulated entity vs vendor;
  - SEBI: RE category.
- Question bank Round 4 (Q16–Q23); `signal-to-scope` triggers for every new framework.
- The kirana-pay expected outcome now includes RBI vendor flow-down and CERT-In.

## Framework expansion, Phase A

- Framework registry `framework-reference/frameworks.csv` with 252 frameworks: 3 curated, 246 SCF-backed and 3 planned. Each SCF-backed entry is linked to its claude-grc-engineering plugin where one exists (30 frameworks).
- SCF-backed catalogs: `/scope` can now scope any SCF-mapped framework (PCI DSS, GDPR, NIST 800-53, CIS, DORA, NIS2, ...). It generates `compliance/catalogs/<key>.csv` from the SCF crosswalk at run time; see `framework-reference/scf.md`.
- New `scf_ids` column in the curated catalogs. SOC 2 and ISO are fully mapped; DPDP is mapped except §16, §17 and Rule 15, which have no SCF mapping.
- New `SCF` column on all 77 playbook rows. Evidence can now support requirements in other frameworks through SCF links, which the user confirms.
- `applicability.csv` accepts any registry key as `framework`. Folder names use `<key>_<req_id>`. `compliance/catalogs/` is git-ignored.
- `signal-to-scope` recommends PCI DSS, GDPR, HIPAA, DORA, NIS2 and US federal frameworks, and notes the CERT-In, RBI and SEBI duties until those catalogs ship.
- Maintainer tool `tools/build_scf_data.py` regenerates the registry and the curated `scf_ids`. Its `--check` mode is for CI.
- Documented a known SCF data issue: ISO 27002 ids ending in 0 have collapsed into their prefix (5.10 into 5.1).

## 0.1.0 - 2026-11-26

First release, built to the requirements in PRD v2.

- Eight commands: `start`, `scope`, `evidence-plan`, `collect`, `request`, `inbox`, `audit`, `status`.
- Five skills:
  - `grc-assistant`
  - `business-discovery`
  - `framework-reference`, with full catalogs: SOC 2 TSC 2017, ISO 27001:2022 and DPDP Act 2023 + Rules 2025
  - `evidence-playbooks`, covering gh, aws, gam, gcloud and az
  - `internal-audit-method`
- Three agents: `site-researcher`, `evidence-reviewer`, `internal-auditor`.
- Optional detection of claude-grc-engineering framework plugins and inspector findings.
- Fictional examples: `acme-saas` and `kirana-pay`.
