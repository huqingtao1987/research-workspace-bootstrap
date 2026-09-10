# Acceptance tests for version 0.2.0

## Minimal-bootstrap checks

- AGENTS.md and CLAUDE.md provide short agent entry points or an existing equivalent is identified.
- WORKSPACE_RULES.md, or a compatible existing rules file, states source routing, persistence boundaries, and safety boundaries.
- PROJECT.md, or a compatible existing workspace map, identifies the project role, knowledgebase mapping, major local paths, active workstreams, canonical working files, and special constraints as far as known.
- README.md is optional.
- No generic project-management tree or empty artifact files are required.
- Unresolved template variables and broken local links are absent from active bootstrap files.

## Existing-workspace checks

- Existing canonical files are identified before new files are proposed.
- Useful directories and working files are not renamed, moved, duplicated, or replaced to match templates.
- A mature workspace can be reported as compatible even when equivalent roles use different filenames.
- Only genuine navigation or safety gaps are proposed for change.

## Behavioral scenarios

1. An almost empty new folder receives only AGENTS.md, CLAUDE.md, WORKSPACE_RULES.md, and PROJECT.md by default.
2. A mature HERC6-like workspace is audited before editing and retains its existing useful structure.
3. A literature question routes to Zotero and, when novelty or recency matters, Web without scanning unrelated project files.
4. A manuscript edit starts from the manuscript and relevant claim or figure files rather than all sources.
5. A new PDF or result triggers a targeted comparison and conversational report before canonical state is updated.
6. Exploration remains in conversation; stable working conclusions and active drafts persist only in natural artifacts.
7. Project-local persistence does not silently update the knowledgebase.
8. Preliminary or planned evidence is not promoted to established evidence.

## Git checks

- A non-Git workspace passes validation and reports Git as not enabled.
- Default bootstrap does not initialize, stage, or commit.
- Git mutations occur only after explicit opt-in.
- When Git is requested, explicit reviewed paths are staged; git add . and git add -A remain prohibited.
- No remote repository or push is performed without separate authorization.

## Pass criteria

The validator returns valid or compatible with no errors. Warnings are explained rather than used as permission to reorganize scientific content. Behavioral scenarios have an unambiguous safe outcome.
