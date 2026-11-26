# Framework expansion plan

Status: Phase A and Phase B done (2026-11-26); Phase C (new example briefs and tests) not started. Builds on v0.1.0 (SOC 2, ISO 27001:2022, DPDP).

## Goal

Audit Ready should scope, collect and audit against more than three frameworks without becoming a database or a platform. Two tiers:

| Tier | What it is | Quality | Frameworks |
|---|---|---|---|
| **Curated** | Hand-written catalogs shipped in the plugin, like the v0.1 ones: paraphrased summaries, mandatory flags, owning function, typical evidence | Best | SOC 2, ISO 27001, DPDP (done); GDPR, PCI DSS 4.0.1, HIPAA Security, NIST CSF 2.0, NIS2, DORA, RBI, CERT-In, SEBI CSCRF (this plan) |
| **SCF-backed** | Generated at scope time from the Secure Controls Framework crosswalks that claude-grc-engineering uses (`https://grcengclub.github.io/scf-api/`, 249 frameworks) | Good: real requirement ids, SCF control text, evidence-request ids; mandatory and function are inferred | Everything else the SCF maps (CIS v8.1, NIST 800-53, CMMC, CSA CCM, Essential 8, APRA CPS 234, NYDFS, CCPA, MAS TRM, Singapore PDPA, Japan APPI, Swiss FADP, ...) |

## What exists in claude-grc-engineering (checked 2026-11-26, commit 79ac7a7)

- **35 framework plugins.**
  - Most are `depth: reference`: prompt-only, with assess and evidence-checklist commands and no data files.
  - Four are `stub`: ch-fadp, nist-ai-600-1, nist-ai-rmf and us-finra.
  - Five have no SCF id: fedramp-20x, hitrust, irap, pbmm and us-export.
- **Machine-readable data comes from the SCF API.**
  - `api/crosswalks/<scf_framework_id>.json` gives `framework_to_scf` (requirement id → SCF control ids) and `scf_to_framework`. Ids only, no requirement text.
  - `api/controls/<SCF-ID>.json` gives `title`, `description`, `scf_question`, `conformity_cadence`, `evidence_requests` (ERL ids) and `pptdf`.
  - The cache is `~/.cache/claude-grc/scf/<version>/`, currently 2026.1.
- **Licence.** SCF data is CC BY-ND 4.0. Audit Ready must **not ship** SCF text or modified SCF files. It fetches at run time and keeps a local copy, as `grc-engineer` does. Storing only SCF control *ids* next to our own curated rows is fine.
- **Not in the SCF or the base repo:** RBI, CERT-In and SEBI CSCRF. These are curated-only.

## Phase A: SCF infrastructure (do first, unlocks every framework)

1. **Framework registry** `skills/framework-reference/frameworks.csv`
   - Columns: `key,display_name,tier,scf_framework_id,region,sector,base_plugin,catalog,notes`.
   - Seed it from the base repo's `plugin.json` `framework_metadata` and the SCF `api/summary.json`. Our own registry text, not SCF text.
   - The `key` is what goes in the `framework` column of `applicability.csv`, for example `pci-dss`, `gdpr` or `cis-v8.1`. Widen the `grc-assistant` allowed values from three fixed keys to "any key in the registry".
2. **SCF ids on curated rows.** Add an optional `scf_ids` column (`;`-separated) to every curated catalog. Fill it for soc2, iso27001 and dpdp from the cached crosswalks (`general-aicpa-tsc-2017`, `general-iso-27001-2022`, `apac-ind-dpdpa-2023`). This links evidence across tiers.
3. **SCF evidence tags on playbooks.** Add an `SCF` column to each playbook row, for example GH-01 → `IAC-06;IAC-10`. When filing, expand the `requirements` field to include every in-scope framework requirement that maps to those SCF ids. One GitHub 2FA export then counts for SOC 2, ISO, PCI DSS 8.4 and NIST CSF PR.AA together.
4. **`skills/framework-reference/scf.md`**, which explains how to build an SCF-backed catalog with no helper code:
   1. Fetch `crosswalks/<id>.json` with WebFetch, or with `curl -s` into `~/.cache/claude-grc/scf/<version>/api/...`. Reuse the cache if the base repo already filled it.
   2. For each requirement id in `framework_to_scf`, read the mapped SCF controls from cache or fetch them.
   3. Write `compliance/catalogs/<key>.csv` in the user's folder. This is a generated working file, git-ignored, not shipped. It has the standard columns plus `scf_ids`:
      - `summary` is the SCF control title or titles, with a note "SCF wording, CC BY-ND";
      - `function` comes from an SCF family → function map that we write (for example IAC → IT, CHG → Engineering, HRS → HR, PRI → Legal, GOV → Leadership);
      - `typical_evidence` comes from the SCF evidence-request ids;
      - `mandatory=no` unless the registry `notes` say otherwise.
   4. Label scoping memos and reports "SCF-backed catalog: requirement ids from SCF crosswalk vX; verify against the official text".
5. **Command changes**
   - **`/scope`:** recommends from the registry plus `signal-to-scope.md`, and accepts any registry key. For SCF-backed frameworks it builds the catalog first, then applicability.
   - **`/evidence-plan` and `/audit`:** read `compliance/catalogs/*.csv` as well as the shipped catalogs. Dedupe through `scf_ids`.
   - **`/status`:** shows readiness for every framework in scope.
   - **Integration:** when the matching base-repo plugin is installed, offer its specialist commands where they help, such as `/pci-dss:saq-select`, `/gdpr:dpia`, `/cis-controls:ig-select` and `/nist-800-53:select-baseline`.
6. **Offline behaviour.** If the SCF API can't be reached and nothing is cached, say so and offer curated frameworks only. Never guess requirement ids.

## Phase B: curated catalogs

Each one needs the following:
- **Catalog CSV:** same columns plus `scf_ids`.
- **Rules:** a `signal-to-scope.md` rule and an `applicability` rule.
- **Requirement keys:** playbook requirement keys added where the CLIs give evidence.
- **Questions:** question-bank entries if the framework needs facts we don't ask about yet.
- **Example coverage:** an example or test brief.

| # | Framework | Granularity (approx. rows) | Mandatory logic | Notes |
|---|---|---|---|---|
| B1 | **GDPR** | Articles 5–49 relevant to controllers and processors (~55) | Arts 5, 6, 12–15, 17, 24, 25, 28, 30, 32, 33 = yes when GDPR applies; Art 37 DPO, Art 35 DPIA and Art 27 representative are conditional | Overlaps heavily with DPDP and SOC 2 Privacy. Flag the Art 3(2) territorial trigger. Base plugin `gdpr` offers `dpia` and `rights-check` |
| B2 | **PCI DSS 4.0.1** | Requirement level x.y (~64), not the ~250 sub-requirements | Depends on SAQ type: applicability is driven by the chosen SAQ (A, A-EP, D-Merchant, D-SP), which is a new question in scoping | The future-dated requirements became effective 31 Mar 2025. Most "cardholder data environment" rows are inherited when payments are hosted (Stripe, Razorpay). Base plugin offers `saq-select` |
| B3 | **HIPAA Security Rule** | §164.308–164.316 standards and implementation specs (~54) | `Required` specs = yes. `Addressable` = yes, but each needs an implement-or-document-alternative reason | Only for covered entities and business associates. Add the BAA to the vendor items |
| B4 | **NIST CSF 2.0** | 6 functions → 22 categories → 106 subcategories (~106) | No mandatory items. Targets are set per profile tier, so add a "target tier" question | Good baseline for US enterprise. Map to SOC 2 and ISO via `scf_ids` |
| B5 | **NIS2** | Art 20 (governance), Art 21(2)(a)–(j) (measures), Art 23 (reporting), plus Implementing Regulation (EU) 2024/2690 for digital providers (~35) | All yes for essential and important entities | Needs an entity classification question (sector + size). Reporting is 24 h early warning, 72 h notification and 1 month final report |
| B6 | **DORA** | Ch II Arts 5–16 ICT risk management, Ch III Arts 17–23 incidents, Ch IV Arts 24–27 testing, Ch V Arts 28–30 third-party risk (~45) | Yes for in-scope financial entities. Simplified framework (Art 16) for small entities | Has a register of information for ICT third parties. B2B SaaS selling to EU banks gets contractual DORA flow-down (Art 30), so scope it as a supplier, not an entity |
| B7 | **CERT-In Directions (28 Apr 2022)** | ~10 obligations | Yes for any organisation with systems in India | Report specified incidents within 6 hours; keep ICT logs for 180 days within India; NTP sync to Indian sources; point of contact. Very cheap to add, and applies to every DPDP-scoped company. Pairs with the existing log-retention playbook rows |
| B8 | **RBI** | Master Direction on IT Governance, Risk, Controls and Assurance Practices (2023) and payment data storage localisation (2018) (~40) | Yes for regulated entities. For vendors, only the clauses passed down by the RBI-regulated partner (outsourcing) | Needs a question on regulated entity vs vendor to an RE. Covers the kirana-pay example's RBI overlay. Consider later adding the Digital Payment Security Controls MD (2021) |
| B9 | **SEBI CSCRF (2024)** | Goals and standards by RE category (~50) | Depends on the RE category (Qualified, Mid-size, Small-size, Self-certification, Basic) | Only for SEBI-regulated entities and their tech vendors. Needs a category question |

India sector catalogs (B7–B9) have no SCF crosswalk. Their `scf_ids` are filled by hand from the closest SCF controls so evidence still dedupes, and marked "Audit Ready mapping".

Accuracy: every curated row is a paraphrase keyed to the official clause id. Each catalog's SKILL section names the official source document and date. RBI, SEBI, CERT-In and NIS2 national transpositions change often, so give each catalog a `source_version` line and a "verify before audit" note.

## Phase order and rough effort

| Step | Content | Effort |
|---|---|---|
| A1–A6 | Registry, `scf_ids`, playbook SCF tags, `scf.md`, command updates | 1 session |
| B7 | CERT-In (small; benefits all Indian customers) | small |
| B1, B2 | GDPR, PCI DSS | 1 session |
| B3, B4 | HIPAA, NIST CSF 2.0 | 1 session |
| B5, B6 | NIS2, DORA | 1 session |
| B8, B9 | RBI, SEBI CSCRF | 1 session |
| C | Examples and tests: extend kirana-pay (RBI + CERT-In), add an EU fintech supplier brief (DORA flow-down + NIS2 + GDPR), add a US health-tech brief (HIPAA + SOC 2) | 1 session |

## Verification

- A catalog checker (the same checks as v0.1) covers every curated CSV:
  - headers, no duplicate ids, and expected row counts (NIST CSF 2.0 = 106 subcategories; HIPAA = all §164.308–316 specs);
  - every `scf_ids` value is a real SCF id in the cached `controls.json`.
- SCF-backed generation: run `/scope` on a test brief that picks CIS v8.1. Check that the generated `compliance/catalogs/cis-v8.1.csv` row count equals the number of `framework_to_scf` entries, and that the scoping memo carries the SCF attribution.
- Dedupe: with SOC 2 + PCI DSS + NIST CSF in scope, a single `gh_org-settings` artifact appears in `index.csv` with requirement keys from all three.
- The plugin passes `claude plugin validate .` and markdownlint as before.
- Licence check: `git grep` for SCF control descriptions in the repo should find nothing. Only ids are shipped.
