---
name: framework-reference
description: Framework registry (about 250 frameworks) and requirement catalogs. Curated catalogs for SOC 2, ISO 27001:2022, India DPDP, GDPR, PCI DSS 4.0.1, HIPAA Security Rule, NIST CSF 2.0, NIS2, DORA, CERT-In Directions, RBI (IT governance, IT outsourcing, payment data localisation) and SEBI CSCRF. On-demand SCF-backed catalogs for every other SCF-mapped framework (NIST 800-53, CIS, CMMC, FedRAMP, NYDFS, CCPA, ...). Use when recommending frameworks, drafting a Statement of Applicability, building an evidence plan, cross-mapping evidence, or auditing a requirement.
allowed-tools: Read, Glob, Grep, Write, Bash, WebFetch
---

# Framework reference

## Framework registry

`frameworks.csv` lists every framework Audit Ready can scope. Its columns are `key,display_name,tier,scf_framework_id,region,base_plugin,catalog,notes`.

| Tier | Meaning | Catalog |
|---|---|---|
| `curated` | Hand-written catalog shipped with the plugin: paraphrased summaries, mandatory flags, function, typical evidence and `scf_ids` | `catalogs/<key>.csv` |
| `scf` | Built on demand from the SCF crosswalk. Real requirement ids, but SCF wording and no mandatory flags | `compliance/catalogs/<key>.csv` (generated; see `scf.md`) |

- **Framework key:** the `key` is the value of the `framework` column in `applicability.csv` and the prefix of requirement keys, for example `pci-dss:8.4`, `soc2:CC6.1` or `gdpr:Article 32`.
- **Look-ups:** use Grep on `frameworks.csv` (`-i pci`); don't read the whole file.
- **Base plugins:** `base_plugin` names the matching claude-grc-engineering plugin, when one exists.
- **Maintenance:** `tools/build_scf_data.py` (repo root) regenerates `frameworks.csv` and the curated `scf_ids`.

## Curated catalogs

| Key | File | Rows | Source and version (verify before an audit) | Granularity |
|---|---|---|---|---|
| `soc2` | `catalogs/soc2.csv` | 61 | AICPA TSC 2017 (revised points of focus 2022) | Criterion: CC1.1–CC9.2, A1, C1, PI1, P1–P8 |
| `iso27001` | `catalogs/iso27001.csv` | 118 | ISO/IEC 27001:2022 (+ Amd 1:2024) | Clauses 4.1–10.2 (25) + Annex A (93) |
| `dpdp` | `catalogs/dpdp.csv` | 32 | DPDP Act 2023 + DPDP Rules 2025 (notified Nov 2025) | Section / rule (`DPDP-8-5`, `DPDP-R7`) |
| `gdpr` | `catalogs/gdpr.csv` | 38 | Regulation (EU) 2016/679 | Article (`Article 32`) |
| `pci-dss` | `catalogs/pci-dss.csv` | 71 | PCI DSS v4.0.1 (June 2024) | Requirement x.y (`8.4`) + Appendices A1–A3 |
| `hipaa-security` | `catalogs/hipaa-security.csv` | 62 | 45 CFR 164.306–164.316 | Standard / implementation spec (`164.312(d)`) |
| `nist-csf-2.0` | `catalogs/nist-csf-2.0.csv` | 106 | NIST CSWP 29, CSF 2.0 (Feb 2024) | Subcategory (`PR.AA-03`) |
| `nis2` | `catalogs/nis2.csv` | 35 | Directive (EU) 2022/2555 Arts 20, 21, 23, 24 + Implementing Regulation (EU) 2024/2690 annex | Article paragraph; `IR-1`–`IR-13` = annex sections |
| `dora` | `catalogs/dora.csv` | 28 | Regulation (EU) 2022/2554 (applies from 17 Jan 2025) + RTS on incident reporting | Article (Arts 28 and 30 split) |
| `cert-in` | `catalogs/cert-in.csv` | 7 | CERT-In Directions under s.70B(6) IT Act, 28 Apr 2022 (+ FAQs) | Obligation (`CERTIN-1`–`CERTIN-7`) |
| `rbi` | `catalogs/rbi.csv` | 26 | RBI MD on IT Governance, Risk, Controls and Assurance Practices (Nov 2023); RBI MD on Outsourcing of IT Services (Apr 2023); Storage of Payment System Data (Apr 2018) + FAQs | Thematic (`RBI-ITG-*`, `RBI-OUT-*`, `RBI-PDL-*`) |
| `sebi-cscrf` | `catalogs/sebi-cscrf.csv` | 21 | SEBI Cybersecurity and Cyber Resilience Framework (Aug 2024) and its clarifications | Thematic by function (`SEBI-GV-*` … `SEBI-AU-*`) |

Columns: `framework,req_id,title,summary,mandatory,function,typical_evidence,category,scf_ids`

- `summary` is a short paraphrase keyed to the official id. It is **not** the text of the standard. Never present it as quoted text. Point users to the official source for the wording.
- **RBI, SEBI and CERT-In:** their catalogs use **thematic Audit Ready ids**, not official clause numbers, because these instruments are revised often and are not structured as numbered controls. Each row names the instrument in `category`. Tell the user to confirm the clause references and current timelines against the latest circulars before an audit.
- `mandatory=yes` means the item cannot be excluded once the framework is in scope **and the entity is in direct scope**. See "Framework-specific applicability" below.
- `function` is the business function that usually owns the evidence: `Engineering`, `IT`, `HR`, `Legal` or `Leadership`. `/audit-ready:audit <function>` uses it.
- `scf_ids` holds the SCF control ids the requirement maps to. They are computed from SCF crosswalks, or hand-mapped for CERT-In, RBI and SEBI. They are used only to link evidence across frameworks; see `scf.md`.

Read catalogs with Grep for single ids (`^pci-dss,8.4,`). Read the whole file only when drafting applicability.

## Recommending frameworks (each reason must cite a profile fact)

| Signal in `profile.md` | Recommendation |
|---|---|
| Sells B2B SaaS to US or global mid-market and enterprise customers; questionnaires mention SOC 2 | **SOC 2**: Type I first if there's no history, then Type II over a 3–12 month period |
| Sells to EU, UK, Middle East, APAC or Indian enterprises, or government; RFPs ask for a certificate | **ISO 27001:2022** |
| Processes digital personal data of people in India (customers, end users or employees) | **DPDP**: applies regardless of company size, and to processing outside India when offering goods or services to people in India |
| Has ICT systems in India (any body corporate, service provider, intermediary or data centre) | **CERT-In**: CERTIN-1 to CERTIN-5 apply to almost every company operating in India. Recommend it whenever DPDP is in scope |
| Offers goods or services to, or monitors, people in the EU or UK; or has an EU establishment | **GDPR** (Art 3). For the UK, the UK GDPR follows the same structure |
| Stores, processes or transmits card data in its own systems, or can affect the security of the CDE | **PCI DSS 4.0.1**. Determine the SAQ or ROC path first |
| US covered entity, or business associate handling ePHI | **HIPAA Security Rule** |
| EU financial entity, or ICT third-party provider to one | **DORA**. ICT providers are in scope through contracts (Art 28–30), not directly, unless designated critical |
| EU essential or important entity (Annex I or II sector and size), or a digital provider listed in IR 2024/2690 | **NIS2** (national transposition applies) |
| RBI-regulated entity, or IT service provider or payment system participant for one | **RBI** |
| SEBI-regulated entity (broker, depository participant, AMC, MII, ...) or its technology vendor | **SEBI CSCRF** |
| Needs a general baseline with no certification, or a US enterprise or government buyer asks for it | **NIST CSF 2.0** |
| Both SOC 2 and ISO asked for | Both. Build one evidence plan; most evidence overlaps |
| US federal or defence buyers | **NIST 800-53** / **FedRAMP** / **CMMC** (SCF-backed) |
| Any other framework the user names | Look it up in `frameworks.csv`. If its tier is `scf`, build it as described in `scf.md` |

When the user names a framework with tier `scf`, say once that its catalog is generated from SCF mappings, with SCF wording and no mandatory flags.

### SOC 2 Trust Services Criteria selection

- **Security (Common Criteria)**: always included.
- **Availability**: customers rely on uptime (SLAs, status page, "99.9%" on the pricing page).
- **Confidentiality**: the company handles customer confidential data under NDA or contract (B2B data platforms, legal or financial documents).
- **Processing Integrity**: customers rely on accurate, complete processing (payments, payroll, calculations, data pipelines).
- **Privacy**: the company collects personal information directly from individuals as a B2C fiduciary, and customers ask for it. Many B2B companies leave it out and cover privacy through DPDP or GDPR instead.

State the reason for each category you include or exclude.

### Regulatory status notes

- **DPDP:** the Rules 2025 were notified in November 2025, with most fiduciary obligations phased in after that. Present DPDP as "prepare now" readiness, and confirm commencement dates with counsel.
- **HIPAA:** a January 2025 proposed rule would remove most "addressable" flexibility. Treat addressable items as expected, and check the rule's status.
- **DORA:** incident reporting timelines come from the RTS/ITS. The register of information follows the ITS template.
- **NIS2:** obligations come from each Member State's transposition law. Confirm the national rules and the competent CSIRT.
- **RBI / SEBI:** circulars change often. Check the latest master direction or circular and the FAQs.

## Applicability rules

1. Every row of every in-scope framework gets an `applicability.csv` row. Never skip rows.
2. If `mandatory=yes`, set `applicable=yes` with reason `mandatory`. The user cannot change it, except where the framework-specific rules below put the whole entity outside direct scope. If asked, explain why.
3. `applicable=inherited` applies when a subprocessor operates the control. Typical cases:
   - physical security (SOC 2 CC6.4, ISO A.7.x, PCI Req 9, HIPAA 164.310(a)) handled by a cloud provider;
   - PCI requirements handled by a PCI-compliant payment provider under a hosted checkout.

   The reason names the vendor. Inherited still needs evidence: the vendor's report or AOC.
4. `applicable=no` requires a concrete reason tied to a profile fact. Example: "No children's data: service is B2B, users are employees of business customers (profile.md: Customers)". "Not relevant" is never acceptable.
5. When a fact is unknown, propose `yes` and add an open question. Don't exclude on a guess.

### Framework-specific applicability

| Framework | Ask first | Rule |
|---|---|---|
| GDPR | Controller, processor or both? EU establishment? | Rights and notice articles (12–22) apply to controllers. A processor supports them through Art 28 and is still bound by 28–33. Without an EU establishment, Art 27 (representative) applies. Arts 7, 8, 9, 10, 20, 22, 26, 35–39 and 44–49 apply only when their trigger is true |
| PCI DSS | Which SAQ, or a ROC? Merchant or service provider? | The SAQ decides which requirements apply. SAQ A (fully hosted payment page) covers only parts of Req 2, 3, 6, 8, 9, 11 and 12, and other rows are `no` with reason "SAQ A". SAQ A-EP and SAQ D cover progressively more. A1 applies only to multi-tenant service providers, A2 only to card-present terminals with early TLS, and A3 only to designated entities. Mark Req 9 rows `inherited` for cloud-hosted CDEs |
| HIPAA | Covered entity or business associate? | Standards and required specs are mandatory. **Addressable** specs are not optional: implement them, or document why an equivalent alternative is reasonable. Use `applicable=yes` with reason "addressable: implemented" or "addressable: alternative documented (...)". Use `no` only where the spec doesn't fit at all, for example 164.308(a)(4)(ii)(A) when there's no clearinghouse |
| NIST CSF 2.0 | Target tier and profile? | Nothing is mandatory. Agree a target profile: propose `yes` for all subcategories, and `no` only with a reason the user accepts. Record the target tier (1–4) in `scope.md` |
| NIS2 | Sector (Annex I or II), size, essential or important, which Member States? Listed digital provider? | Arts 20, 21 and 23 apply to every in-scope entity. `IR-*` rows apply only to the digital providers listed in IR 2024/2690 (DNS, TLD, cloud, data centre, CDN, MSP, MSSP, online marketplaces, search engines, social networks, trust services); otherwise mark them `no`. If the company is only a supplier to an NIS2 entity, scope Art 21.2(d) and 21.3 obligations as contractual flow-down |
| DORA | Financial entity, ICT third-party provider, or designated critical ICT provider? Do your services support the customer's critical or important functions? | **Financial entity:** all rows apply. Art 16 replaces Arts 5–15 for entities on the simplified regime, Art 23 only for payment, credit and e-money institutions, and Arts 26–27 only if designated for TLPT. **ICT supplier:** mark Arts 5–27 `no` with reason "not a financial entity; obligations flow down via customer contracts". Keep Arts 28.4, 30.2 and 30.3 (what customers will require), plus any Art 9–12 controls the customer contracts require |
| CERT-In | Provider type (data centre, VPS, cloud, VPN, VASP)? | CERTIN-1 to CERTIN-5 are mandatory for bodies corporate operating in India. CERTIN-6 applies only to data centre, VPS, cloud and VPN providers. CERTIN-7 applies only to VASPs |
| RBI | Regulated entity (bank, NBFC, payment system operator, ...) or a vendor to one? | **RE:** all `RBI-ITG-*` and `RBI-OUT-*` rows apply (in proportion to the RE category); `RBI-PDL-*` applies if it is a payment system provider or participant. **Vendor:** `RBI-OUT-03` to `RBI-OUT-07` apply as contractual flow-down, plus `RBI-PDL-*` if it stores or processes payment system data for a payment system operator; mark `RBI-ITG-*` rows `no` unless the RE's contract imposes them |
| SEBI CSCRF | RE category (MII, Qualified, Mid-size, Small-size, Self-certification) or vendor? | The category decides which standards apply and how often (VAPT, audit, SOC model, CCI). SEBI-ID-02 (CCI) applies only to MIIs and Qualified REs. A vendor scopes SEBI-GV-04 and SEBI-GV-05 obligations through the RE's contract |

## Cross-framework dedupe

One evidence artifact often covers several requirements. Playbook rows carry hand-mapped keys for every curated framework (the `Requirements` column). Common overlaps:

| Theme | SOC 2 | ISO 27001 | DPDP | PCI DSS | HIPAA | NIST CSF | Others |
|---|---|---|---|---|---|---|---|
| MFA | CC6.1 | A.5.17, A.8.5 | DPDP-R6 | 8.4, 8.5 | 164.312(d) | PR.AA-03 | NIS2 21.2(j); RBI-ITG-10; SEBI-PR-01 |
| Access reviews | CC6.2, CC6.3 | A.5.18, A.8.2 | DPDP-R6 | 7.2 | 164.308(a)(4) | PR.AA-05 | NIS2 21.2(i); RBI-ITG-10 |
| Logging | CC7.2 | A.8.15 | DPDP-R6 | 10.2, 10.3 | 164.312(b) | PR.PS-04 | DORA 10; RBI-ITG-09; CERTIN-5 |
| Log retention | CC7.2 | A.8.15 | DPDP-R6 (1 yr) | 10.5 (12 mo) | 164.316(b)(2)(i) (docs 6 yr) | PR.PS-04 | CERTIN-5 (180 days, India); SEBI-PR-06 |
| Encryption | CC6.1, CC6.7 | A.8.24 | DPDP-8-5 | 3.5, 4.2 | 164.312(a)(2)(iv), (e)(2)(ii) | PR.DS-01, PR.DS-02 | GDPR 32; NIS2 21.2(h); RBI-ITG-14 |
| Change management | CC8.1 | A.8.32 | | 6.5 | | PR.PS-06 | DORA 9; RBI-ITG-08; NIS2 21.2(e) |
| Vulnerability management | CC7.1 | A.8.8 | DPDP-8-5 | 6.3, 11.3 | | ID.RA-01 | DORA 25; RBI-ITG-11; SEBI-PR-04 |
| Backups and DR | A1.2, A1.3 | A.8.13, A.5.30 | DPDP-R6 | | 164.308(a)(7) | PR.DS-11 | DORA 11, 12; NIS2 21.2(c); RBI-ITG-15 |
| Incident reporting | CC7.3–CC7.5 | A.5.24–A.5.26 | DPDP-8-6, R7 (72 h) | 12.10 | 164.308(a)(6) | RS.CO-02 | GDPR 33 (72 h); NIS2 23 (24 h / 72 h / 1 mo); DORA 19; CERTIN-2 (6 h); SEBI-RS-01 (6 h) |
| Vendors | CC9.2 | A.5.19–A.5.22 | DPDP-8-2 | 12.8 | 164.308(b) | GV.SC-* | GDPR 28; DORA 28–30; RBI-OUT-*; NIS2 21.2(d) |
| Data location | | | DPDP-16 | | | | RBI-PDL-01; SEBI-PR-02; CERTIN-5; GDPR 44–46 |
| Risk assessment | CC3.1–CC3.4 | 6.1.2, 8.2 | | 12.3 | 164.308(a)(1)(ii)(A) | ID.RA-* | NIS2 21.2(a); DORA 8 |
| Training | CC2.2 | A.6.3, 7.3 | | 12.6 | 164.308(a)(5) | PR.AT-01 | NIS2 20.2, 21.2(g); DORA 13 |

For any other pair of frameworks, the general rule is that two requirements may overlap when their `scf_ids` intersect. Treat that as a hint the user confirms (see `scf.md`).

If claude-grc-engineering's `grc-engineer` plugin is installed, `config/control-crosswalk.yaml` in its plugin folder adds SOC 2 to ISO mappings. It uses **ISO 27001:2013** Annex A ids (A.9.x, A.12.x), so translate them to 2022 ids before writing. Examples: 2013 A.9.2.1 becomes 2022 A.5.16, and 2013 A.12.4.1 becomes A.8.15.

## Framework plugins (optional)

If the framework's `base_plugin` from claude-grc-engineering is installed (detected by grc-assistant), `/audit-ready:evidence-plan` can suggest `/<base_plugin>:evidence-checklist` as a second opinion. Specialist commands help with applicability, for example `/pci-dss:saq-select`, `/gdpr:dpia`, `/dora:incident-reporting` and `/eu-nis2:scope`. Audit Ready's catalogs, curated or generated, remain the source for `applicability.csv`.
