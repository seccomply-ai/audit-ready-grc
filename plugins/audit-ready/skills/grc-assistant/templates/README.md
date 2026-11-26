# compliance/

Working folder for Audit Ready. Every file here is plain Markdown or CSV and opens in any editor, Excel or Google Sheets.

- The files are the source of truth. Audit Ready re-reads them every session.
- You may edit them by hand. Keep the CSV headers unchanged; Audit Ready reports anything malformed before continuing.
- `evidence/` and `audit/` are git-ignored because they can contain personal data. Never commit evidence to source control; store it in an encrypted, access-controlled evidence locker for the audit.
- Drop files requested from owners into `evidence/_inbox/`, then run `/audit-ready:inbox`.

Commands: `/audit-ready:start`, `scope <url>`, `evidence-plan`, `collect [tool]`, `request [owner]`, `inbox`, `audit [function]`, `status`.
