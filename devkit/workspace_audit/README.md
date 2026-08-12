# Workspace Audit

This DevKit slice gives an LLM a reproducible, read-only map of the SoD Modern
Mount and Blade 1.011 module system before it diagnoses source, generated
compile modules, or game exports.

It reports:

- modular source volume by area;
- source-to-compile-to-export pipeline stages;
- manifest and folder-driven ordering contracts;
- generated entity and export counts;
- direct-input freshness, generated/export mtime relationships, and Git
  worktree caution;
- static cross-reference-operation volume and validation-surface size.

The primary interface is the typed MCP tool named workspace_audit. The
deterministic CLI is its offline fallback.

## CLI

From the module root:

~~~powershell
py -3 devkit\workspace_audit\workspace_audit.py summary
py -3 devkit\workspace_audit\workspace_audit.py summary --format markdown
py -3 devkit\workspace_audit\workspace_audit.py summary --output devkit\output\workspace-audit.json
py -3 devkit\workspace_audit\workspace_audit.py summary --format markdown --output devkit\output\workspace-audit.md
~~~

JSON is the default output. Samples are bounded by --max-items; the tool does
not run a builder, processor, doctor pass, or export step. An explicit output
path is allowed outside _export only.

## Verify

~~~powershell
py -3 -B devkit\workspace_audit\test_workspace_audit.py
~~~
