# Tests

| Script | What it checks | Needs |
|---|---|---|
| `validate_repo.py` | Static checks, listed below | Python 3 standard library only |
| `check_scope_result.py` | Compares a real `/audit-ready:scope` run against an example's `expected.csv` | The `compliance/` folder from your run |
| `../tools/build_scf_data.py --check` | The registry and curated `scf_ids` still match the SCF data | The SCF cache in `~/.cache/claude-grc/scf/` |

`validate_repo.py` checks:

- **Manifests:** sources exist and names match their folders.
- **Templates:** CSV templates match the headers documented in the skill.
- **Catalogs:** headers, allowed values, unique ids, expected row counts, and mandatory rules (SOC 2 CC, ISO clauses).
- **Registry:** consistent with the catalog files.
- **Playbooks:** every requirement key exists, and **every command passes the read-only allowlist** (no write verbs, no `gh api -X/-f`, no chaining).
- **Examples:** CSV headers, sha256 of the filed evidence, and the readiness rows in the sample report recomputed from `assessments.csv`.
- **Skills:** frontmatter is present, and the generator embedded in `scf.md` compiles.

CI (`.github/workflows/validate.yml`) runs `validate_repo.py`, markdownlint, and an informational SCF freshness check.

## Full manual test

`e2e-test-plan.md` is a step-by-step checklist for every command, the safety rules, the claude-grc-engineering integration and the evidence package.

## End-to-end scoping test

Scoping is done by Claude, so its output varies from run to run. The `expected.csv` files hold the judgements that must not vary: which frameworks are in scope, and which key requirements are applicable.

1. Create an empty scratch folder and start Claude Code there, with the plugin installed.
2. Run `/audit-ready:start`, then `/audit-ready:scope`. Say the website is unavailable and paste the example's `company-brief.md` facts as your answers. Accept the recommendations unless they contradict the brief.
3. Check the result:

   ```bash
   python tests/check_scope_result.py --compliance <scratch>/compliance --expected examples/ledgerloop/expected.csv
   ```

| Example | Exercises |
|---|---|
| `acme-saas` | SOC 2 + DPDP: a complete folder (also run in CI against its own files) |
| `kirana-pay` | ISO 27001, DPDP (children's data), CERT-In, RBI as a vendor |
| `ledgerloop` | DORA supplier mode, GDPR controller and processor, NIS2 open question, PCI negative case, CERT-In for an India subsidiary |
| `carecadence` | HIPAA business associate (addressable specs), PCI SAQ A, SOC 2 categories, NIST CSF target tier |

Besides the per-example expectations, the checker always enforces two rules:
- every `no` or `inherited` row has a reason;
- a mandatory row is `no` only with an entity-scope reason (for example a DORA supplier, a GDPR processor or a PCI SAQ).
