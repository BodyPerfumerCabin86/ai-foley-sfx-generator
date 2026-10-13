# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security only |
| < 0.5   | no        |

## Reporting a vulnerability

This tool loads third-party extension modules and runs local ML models. The
realistic attack surface is:

1. **Malicious extension module** — a plugin is arbitrary Python. Only install
   modules you trust, or run the host with `--sandbox` (subprocess worker,
   restricted cwd).
2. **Model file deserialization** — `.pt` / `.ckpt` loaders use `torch.load`
   with `weights_only=True`. Never disable that flag in a plugin.
3. **Path traversal in scene importers** — importer code must resolve paths
   against the project root. Report any importer that doesn't.
4. **Arbitrary file write via render output** — output paths come from user
   config; the host rejects paths outside the configured `renders/` root.

Report vulnerabilities privately to security@<org>.example. We aim to
acknowledge within 72 hours and ship a fix or mitigation within 14 days.

Do **not** open a public issue for a working exploit. Include a minimal
reproducer: host version, plugin manifest, and the exact command sequence.

## Out of scope

- Audio content itself. This tool generates sound; we don't police what you
  synthesize with it.
- Denial of service from a plugin you chose to install.
- Issues that require an already-compromised machine.