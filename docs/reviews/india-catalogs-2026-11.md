# Source check: CERT-In, RBI and SEBI CSCRF catalogs (27 Nov 2026)

**This is a source check, not legal sign-off.** Every row in `cert-in.csv`, `rbi.csv` and `sebi-cscrf.csv` was compared with the primary documents listed below. Summaries were corrected where they were wrong or incomplete, and each row's `category` now names the instrument and its official clause. Before an engagement relies on these catalogs, a practitioner who knows these regulators still has to confirm them, and should sign off at the end of this file.

## Sources

| Instrument | Read | Notes |
|---|---|---|
| CERT-In Directions under s.70B(6) IT Act, 28 Apr 2022 | In full (cert-in.org.in PDF) | No amendment or replacement found |
| CERT-In FAQs on the Directions, May 2022 | Targeted questions only | FAQ 30 (partial first report), 34 (public VPNs), 35 and 37 (log location), 40–42 (time source) |
| RBI MD on IT Governance, Risk, Controls and Assurance Practices, 7 Nov 2023 | In full (rbi.org.in Id=12562) | **Repealed.** Replaced by the entity-specific *Cybersecurity, Technology: Risk, Resilience and Assurance Framework Directions, 2026* (31 Jul 2026, updated 1 Oct 2026). The repeal (para 230) and new paragraph numbers were checked only in the commercial-bank version |
| RBI MD on Outsourcing of IT Services, 10 Apr 2023 | In full (Id=12486) | **Repealed.** Replaced by the *Managing Risks in Outsourcing Directions, 2025* (commercial banks: RBI/DOR/2025-26/171, 28 Nov 2025; IT outsourcing is Chapter IV) |
| RBI Storage of Payment System Data, 6 Apr 2018, and FAQs (Jun 2019) | Circular in full (Id=11244); FAQs by targeted question | Still in force |
| SEBI CSCRF circular SEBI/HO/ITD-1/ITD_CSC_EXT/P/CIR/2024/113, 20 Aug 2024 | In full (205 pages) | |
| SEBI CSCRF clarifications: CIR/2024/184 (31 Dec 2024), CIR/2025/45 (28 Mar 2025), CIR/2025/60 (30 Apr 2025), CIR/2025/119 (28 Aug 2025) | In full | The 30 Jun 2025 extension to 31 Aug 2025 and the 11 Jun 2025 FAQs are known only from secondary sources and CIR/2025/119 |

## What changed

### CERT-In (7 rows)

| Row | Clause | Result | Change |
|---|---|---|---|
| CERTIN-1 | (i) | OK | Category only |
| CERTIN-2 | (ii), Annexure I | Fixed | Annexure I lists 20 incident types; a first report may be partial |
| CERTIN-3 | (iii), Annexure II | OK | Category only |
| CERTIN-4 | (iii) | Fixed | An order can require action as well as information, in a format CERT-In sets |
| CERTIN-5 | (iv); FAQs 35, 37 | Fixed | FAQ 35 accepts logs stored abroad if they can be produced promptly |
| CERTIN-6 | (v); FAQ 34 | Fixed | Full record list; "public VPN" providers only (not corporate VPNs) |
| CERTIN-7 | (vi), Annexure III | Fixed | Applies to VASPs, exchanges and custodian wallets; records must reconstruct each transaction |

### RBI (26 rows)

All RBI rows apply only to the entity classes the instruments name; outsourcing rows apply only to *material* IT outsourcing. Paragraph numbers are from the 2023 master directions. Where the 2026 or 2025 commercial-bank paragraph was confirmed, it is added in brackets as `2026 CB` or `2025 CB`.

| Row | 2023 clause | Result | Change |
|---|---|---|---|
| RBI-ITG-01 | ITG paras 4–5 | Fixed | Replaced "value delivery" with the MD's focus areas; Board reviews annually |
| RBI-ITG-02 | ITG para 6 (2026 CB 17–18) | Fixed | ITSC: at least three directors, independent chair with IT expertise, quarterly meetings |
| RBI-ITG-03 | ITG paras 7–8 | Fixed | Steering committee of IT and business leaders, quarterly |
| RBI-ITG-04 | ITG paras 5, 24(a) | Fixed | Adds the Cyber Crisis Management Plan; Board reviews annually |
| RBI-ITG-05 | ITG para 24(b)–(d) (2026 CB 27–28) | Fixed | CISO independent of the Head of IT, no business targets |
| RBI-ITG-06 | ITG para 9 | Fixed | The MD requires CIA classification and end-of-support tracking, not a general inventory |
| RBI-ITG-07 | ITG para 11 | Fixed | Annual capacity assessment reviewed by the ITSC |
| RBI-ITG-08 | ITG para 13 | Fixed | Business-impact assessment and recovery from failed changes |
| RBI-ITG-09 | ITG para 15 | OK | Category only |
| RBI-ITG-10 | ITG paras 19–20 | Fixed | ITSC-approved access standards; MFA for privileged and remote access to critical systems |
| RBI-ITG-11 | ITG paras 22, 25–26 (2026 CB 151) | Fixed | VA every 6 months, PT every 12 months for critical and customer-facing systems |
| RBI-ITG-12 | ITG para 24(d) (2026 CB Chapter VI) | Fixed | The 2023 MD only assigns SOC monitoring to the CISO's office; the 2026 directions add a SOC chapter |
| RBI-ITG-13 | ITG para 27 (2026 CB 182) | Fixed | RBI within 6 hours of detection (DAKSH platform under 2026) and CERT-In |
| RBI-ITG-14 | ITG paras 16–17, 23 | Fixed | Cryptography and straight-through processing; the MD does not mention DLP |
| RBI-ITG-15 | ITG paras 28–29 (2026 CB 165) | Fixed | Half-yearly DR drills including a full business day from DR |
| RBI-ITG-16 | ITG para 30 (2026 CB 224–227) | Fixed | IS Audit Policy approved by the Audit Committee; frequency set by that policy |
| RBI-OUT-01 | OUT paras 4, 9 | OK | Category only |
| RBI-OUT-02 | OUT paras 13–14 | Fixed | Adds legal and reputational factors and concentration risk |
| RBI-OUT-03 | OUT paras 15–16 | OK | Category only |
| RBI-OUT-04 | OUT paras 16, 19(8), 21(3) | OK | Category only |
| RBI-OUT-05 | OUT para 17(8) (2025 CB 56) | Fixed | Provider reports so the RE can tell RBI within 6 hours of the provider's detection |
| RBI-OUT-06 | OUT paras 18, 22 | OK | Category only |
| RBI-OUT-07 | OUT Appendix I | Fixed | Cloud adoption policy, RE-controlled keys, MFA, CSP logs to the SOC |
| RBI-PDL-01 | PSD para 2(i); FAQs | Fixed | Adds the foreign-leg exception |
| RBI-PDL-02 | PSD FAQs (Jun 2019) | Fixed | "One business day or 24 hours, whichever is earlier"; the rule is in the FAQs |
| RBI-PDL-03 | PSD para 2(iii) | Fixed | The audit report is Board-approved |

### SEBI CSCRF (21 rows)

| Row | Reference | Result | Change |
|---|---|---|---|
| SEBI-GV-01 | GV.PO | Fixed | Annual review; covers CSCRF standards and guidelines |
| SEBI-GV-02 | GV.RR | Fixed | CISO reporting line by category; IT Committee with an external expert, quarterly |
| SEBI-GV-03 | GV.RM | OK | Category only |
| SEBI-GV-04 | GV.SC | OK | Category only |
| SEBI-GV-05 | PR.IP.S13, Annexure-J | OK | Category only. HSM mandatory for MIIs and Qualified REs (30 Apr 2025) |
| SEBI-ID-01 | ID.AM | OK | Category only |
| SEBI-ID-02 | GV.OV, Annexure-K | OK | CCI: third-party half-yearly for MIIs, self-assessment annually for Qualified REs |
| SEBI-PR-01 | PR.AA | OK | Category only |
| SEBI-PR-02 | PR.DS | Fixed | **Data localisation (PR.DS.S2) is in abeyance since 31 Dec 2024** |
| SEBI-PR-03 | PR.IP | OK | Category only |
| SEBI-PR-04 | PR.MA | OK | Category only |
| SEBI-PR-05 | PR.AT | OK | Category only |
| SEBI-PR-06 | PR.AA.S8–S9 | Fixed | CSCRF sets no retention period of its own; it defers to government rules (CERT-In) |
| SEBI-DE-01 | DE.CM, Annexure-N | Fixed | SOC for all REs; Small and self-certification REs join the Market SOC unless they run their own |
| SEBI-DE-02 | DE.CM.S5, Section 4.3 | Fixed | VAPT frequency depends on NCIIPC protected/CII status, not RE category; report, closure and revalidation deadlines |
| SEBI-RS-01 | RS.CO, Annexure-O | Fixed | 6 hours applies to incidents under the CERT-In directions; others 24 hours; 3-day and 30-day follow-ups |
| SEBI-RS-02 | RS.MA | Fixed | Aligned with CERT-In's national CCMP; approved by the Board, partners or proprietor |
| SEBI-RC-01 | RC.RP | Fixed | SEBI sets RTO 2 hours and RPO 15 minutes for critical systems |
| SEBI-RC-02 | RS.AN | Fixed | Sits under Respond; RCA to SEBI within 30 days |
| SEBI-AU-01 | Section 4.4 | Fixed | Frequency by category and trading channel; self-certification REs do VAPT only plus self-certification |
| SEBI-AU-02 | Section 4.1, Annexure-P | OK | Category only |

## Spot-check quotes

These short quotes let a reviewer confirm the source quickly.

- CERT-In Directions (ii): "shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents"
- CERT-In Directions (iv): "maintain them securely for a rolling period of 180 days and the same shall be maintained within the Indian jurisdiction."
- RBI ITG MD 2023 para 6(c): "The ITSC shall meet at least on a quarterly basis."
- RBI IT Outsourcing MD 2023 para 17(8): "the incident is reported by the RE to the RBI within 6 hours of detection by the TPSP."
- RBI payment data circular para 2(iii): "The audit should be conducted by CERT-IN empaneled auditors certifying completion of activity at (i) above."
- SEBI CIR/2024/184 para 2.3: "the guidelines and provisions with regard to Data Localisation [Data Security standard (PR.DS.S2)] has been kept in abeyance until further notification."
- SEBI CSCRF GV.SC.S5: "SBOM shall be obtained for all new software procurements of core and critical activities and kept updated with every upgrade or change."
- SEBI CSCRF Section 4.4.6: "REs categorised as self-certification shall be required to conduct only VAPT audit through CERT-In empanelled IS auditing organisation"

## Open items for the expert reviewer

1. **Rebase RBI onto the 2025 and 2026 directions.** Content largely carries over, but paragraph numbers differ by entity type (commercial, small finance, payments and co-operative banks, NBFCs, AIFIs, CICs). Non-bank payment system operators now have their own cyber resilience master directions; decide whether they need separate rows.
2. **Obligations with no row yet.**
   - RBI: grievance redress stays with the RE (OUT para 7); a central inventory of outsourcing arrangements (OUT paras 8, 12(2)); cross-border outsourcing (OUT para 21); conflict of interest (OUT para 4(3)); source code escrow and vendor "no known vulnerabilities" certificates (ITG para 12); geographically separate DC and DR (ITG para 18); teleworking (ITG para 20).
   - SEBI: red teaming and threat hunting (DE.DP.S4–S5); threat intelligence and advisories within 24 hours (ID.RA.S3); ISO 27001 for MIIs and CIS Controls (PR.IP.S16–S17); software assurance audits (PR.IP.S4–S6, S15); network segmentation and zero trust (PR.AA.S2, S4); the Evolve function (EV.ST); Cyber Swachhta Kendra onboarding (RS.MA.S5); data disposal and physical security (PR.AA.S10, S13–S14).
3. **SEBI categories.** The thresholds were revised on 30 Apr 2025 and 28 Aug 2025. Confirm the current thresholds and the Exclusivity and Equivalence principles for REs regulated by more than one regulator (28 Aug 2025).
4. **Unconfirmed items.** The CERT-In deadline extension for directions (v) and (vi) to 25 Sep 2022, and the 30 Jun 2025 SEBI extension, were not checked against the primary text.
5. **`mandatory` column.** All rows ship as `mandatory=no` on purpose: the entity-derived locks in `framework-reference/SKILL.md` set them to mandatory once the entity type is known. Confirm the lock table still matches the instruments above.

## Sign-off

| Reviewer | Role | Date | Scope | Result |
|---|---|---|---|---|
| | | | | |
