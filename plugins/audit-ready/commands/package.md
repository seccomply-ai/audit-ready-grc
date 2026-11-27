---
description: Build an encrypted, hash-verified evidence bundle for the external auditor from the filed evidence, using claude-grc-engineering's packager when installed
argument-hint: "<recipient GPG fingerprint (40 or 64 hex)> [framework key]"
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Audit Ready: package

Hand-off. Bundles the filed evidence for the auditor in one encrypted file, with a manifest of SHA-256 hashes the auditor can check. Nothing is sent: the user delivers the file.

## Usage

```
/audit-ready:package 0123456789ABCDEF0123456789ABCDEF01234567
/audit-ready:package 0123456789ABCDEF0123456789ABCDEF01234567 soc2
```

## Arguments

Parse `$ARGUMENTS`:
- **Fingerprint (required):** the auditor's full primary-key fingerprint, 40 or 64 hex characters, spaces removed. Reject short key ids and email addresses: the user must confirm the fingerprint with the auditor through a separate channel.
- **Framework key (optional):** must be in scope (`applicability.csv`). Only evidence linked to that framework's requirements is packaged.

## Preconditions

- `evidence/index.csv` has rows, and `scope.md` is approved. Load the skill `audit-ready:grc-assistant` and validate the CSVs.
- `gpg` is installed (`gpg --version`), and the recipient key is in the user's keyring (`gpg --list-keys <fingerprint>`). If it isn't, tell the user to import it; never import keys yourself.

## Steps

1. **Select files.** Take the `index.csv` rows (filtered by framework if given). Skip anything under `_inbox/` or `_staging/`, and any `.error.txt`.
2. **Verify.** Recompute each file's SHA-256 and compare it with the index. Stop and list mismatches: altered evidence is never packaged. Re-collect it instead.
3. **Stage.** Copy the selected files, keeping their folder paths, into `compliance/evidence/_staging/package-<YYYY-MM-DD>/`. Add a copy of `index.csv` filtered to those rows, and, if approved, the latest `audit/<date>-internal-audit-report.md`.
4. **Show the command and wait for approval.**
   - If `grc-engineer` is installed (its `installPath` from `~/.claude/plugins/installed_plugins.json`):

     ```bash
     python -I "<installPath>/scripts/package-evidence.py" compliance/evidence/_staging/package-<YYYY-MM-DD> compliance/audit/<YYYY-MM-DD>-evidence.zip.gpg <FINGERPRINT>
     ```

     It refuses symlinks and an output inside the source, writes `MANIFEST.json` (`algorithm`, and `files[{path, sha256, size}]`) into the ZIP, verifies the ZIP, and encrypts it to that one key.
   - If not, propose the manual equivalent: build `MANIFEST.json` from the staged files in the same shape, zip the folder, then `gpg --encrypt --recipient <FINGERPRINT> --output compliance/audit/<YYYY-MM-DD>-evidence.zip.gpg <zip>`, and delete the plain ZIP.
5. **Clean up.** Delete the staging copy. Never leave an unencrypted bundle on disk.
6. **Tell the user** the output path, its SHA-256 (printed by the packager), the file count, and how the auditor verifies it: decrypt, then `python verify-evidence.py <zip>` from claude-grc-engineering, or check `MANIFEST.json` hashes with `sha256sum`.

## Output

The bundle path, its SHA-256, files included (count per framework), files skipped and why, and the verification note.

## Guardrails

- Never send, upload or email the bundle. The user delivers it.
- Never package files whose hash doesn't match the index.
- `compliance/audit/` is git-ignored: remind the user not to commit the bundle.
