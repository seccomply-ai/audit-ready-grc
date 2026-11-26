# Changelog

## Unreleased: framework expansion, Phase B

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
