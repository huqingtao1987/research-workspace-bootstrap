---
name: research-workspace-bootstrap
description: Minimally initialize, audit, or adapt a research project directory as a durable AI workspace. Use when a new folder needs essential agent navigation and safety rules, or when an established workspace needs a light governance audit. Grow project-specific state, analysis, writing, and decision artifacts only when real work requires them. Do not use for scientific analysis itself or wholesale directory reorganization.
disable-model-invocation: true
---

# Research Workspace Bootstrap

Make a research directory understandable and safe for continued AI-assisted work with the least necessary structure.

## Core posture

Apply three principles together:

- minimal bootstrap;
- grow on demand from real work;
- preserve useful existing structure.

Prefer adapting to an existing useful project structure over imposing the skill's preferred structure. Templates are defaults for missing structure, not schemas that every project must conform to.

This skill establishes navigation, operating boundaries, and source routing. It does not perform the project's scientific analysis.

## Authorization boundary

When the user asks to initialize or update a workspace, that authorizes a read-only inventory and creation or focused revision of bootstrap files. Before changing an existing governance file, preserve a dated rollback copy unless the project already has a safer versioning convention.

It does not authorize:

- reading sensitive or non-deidentified content without explicit permission;
- changing scientific data, results, manuscripts, knowledgebase pages, Zotero, or external systems;
- moving, renaming, deleting, or broadly reorganizing existing project materials;
- scanning the whole project, knowledgebase, raw archive, or Zotero library;
- initializing Git, staging, committing, creating a remote, or pushing unless separately requested.

Stop and ask when a required action crosses these boundaries.

## Choose a mode

- Minimal bootstrap: create or complete only the missing navigation layer in a new or lightly organized directory.
- Existing-workspace mode: audit a mature directory, identify files already serving canonical roles, and fill only genuine navigation or safety gaps.
- Audit only: report compatibility, gaps, and suggested changes without writing files.
- Focused update: revise the workspace layer after real usage exposes a durable need.

Existing useful structure takes precedence over bootstrap templates.

## Workflow

### 1. Resolve scope without broad scanning

Confirm the project root and read existing AGENTS.md, CLAUDE.md, WORKSPACE_RULES.md, PROJECT.md, README.md, or obvious equivalents first. Check Git status without changing it.

Inventory filenames, paths, types, sizes, and dates only as needed to understand the workspace. Do not open large binaries, raw archives, or potentially sensitive files merely to classify them.

When new Word, PowerPoint, PDF, figure, or result files appear, inspect only the materials relevant to the current task. Determine whether they may change current state, report the difference in conversation, and update a canonical working file only after user confirmation or when existing workspace rules already authorize it.

### 2. Identify existing canonical roles

Before creating anything, map which existing files already provide:

- Codex and Claude entry points;
- shared working and safety rules;
- a workspace map;
- active scientific state or current deliverables;
- project-specific plans, drafts, decisions, or evidence records.

Do not rename, move, duplicate, or replace a useful file simply to match a template. In an established workspace, add only the missing bootstrap or navigation layer.

### 3. Build the minimum project profile

Read references/intake-schema.md. Use only facts supported by the user's message or project materials. Keep unsupported fields unknown; do not invent sample counts, endpoints, project stage, target journal, storage paths, owners, deadlines, or permissions.

Read references/project-type-routing.md only when choosing project-specific artifacts or source routes would materially improve the result.

### 4. Announce the change set

Before editing, state:

- operating mode and existing canonical files found;
- files to create, revise, or archive;
- materials that will remain untouched;
- Git state and whether Git was explicitly requested.

### 5. Create only the minimal bootstrap

For missing structure, adapt assets/base to create or complete:

~~~text
AGENTS.md
CLAUDE.md
WORKSPACE_RULES.md
PROJECT.md
~~~

- AGENTS.md is a short Codex entry point.
- CLAUDE.md is a short Claude Code entry point.
- WORKSPACE_RULES.md contains shared operating, safety, persistence, and source-routing rules.
- PROJECT.md maps the current workspace: project name and role, related knowledgebase project page, major local directories and their roles, active workstreams, existing canonical working files, and current special constraints.

PROJECT.md is navigation, not a duplicate scientific record. Scientific current state remains in the related knowledgebase project page or existing project working files. README.md is optional and may remain the human-facing overview when it already serves that role.

Do not create empty project-management directories or generic evidence, task, decision, or stage-summary files during bootstrap.

### 6. Route retrieval by task

Progressive retrieval is task-routed, not a mandatory linear cascade. Select the smallest useful source set:

- project status or scientific question: PROJECT.md, current working files, and the related knowledgebase project page;
- local analysis: relevant data inventory, analysis files, outputs, and logs;
- historical decision: the specific decision record or raw history only when needed;
- literature evidence: Zotero;
- novelty, current landscape, or completeness: Zotero and Web in the combination needed;
- manuscript revision: the manuscript and relevant figure or claim files, expanding only if required.

The user normally does not need to name the source. Do not default to full-project, full-knowledgebase, full-raw, full-Zotero, or open-world discovery.

### 7. Apply the artifact persistence gate

- Exploration: ordinary discussion, alternatives, and unconfirmed reasoning stay in conversation.
- Stable working conclusion: create or update the relevant project-local plan or state file when the conclusion must survive across conversations.
- Active artifact production: create or update the relevant draft when sustained writing, grant, analysis-plan, or other formal production has begun.
- Long-term scientific state change: suggest promotion to the related knowledgebase project page, but do not modify the knowledgebase without separate authorization.

Project-local persistence is not knowledgebase promotion. The latter requires a higher threshold: stable, important, cross-session scientific state that belongs in the user's long-term knowledge system.

Use natural artifacts for the work. Examples include claim-evidence.md or manuscript.md for papers; grant-plan.md for funding proposals; analysis-plan.md or data-inventory.md for analysis; and database-state.md or release-plan.md for resources. These are examples, not a required schema.

### 8. Preserve evidence status

Keep these categories distinct:

- direct project observation or result;
- literature-supported interpretation;
- Agent inference;
- hypothesis or planned work;
- user-confirmed decision.

Never promote preliminary or planned evidence to established evidence.

### 9. Treat Git as explicit opt-in

Always inspect and report Git status. If the project is not a repository, report: 当前项目尚未启用 Git，如需可显式初始化。

Do not run git init, stage, or commit unless the user explicitly asks to enable Git. If requested:

- preserve any existing branch, history, staging area, and ignore rules;
- never use git add . or git add -A;
- stage only reviewed explicit paths;
- do not include data, binaries, sensitive files, credentials, or unrelated existing work;
- do not create a GitHub repository or push unless separately requested.

### 10. Validate and hand off

Run scripts/validate_workspace.py against the target and use references/acceptance-tests.md for behavioral checks. A non-Git workspace and a workspace without a standard project-management tree can still be valid.

Report the selected mode, canonical roles found, files created or revised, rollback path, validator status, Git status, unresolved facts, and the next useful action.

## Maintenance rule

Update the workspace layer only when real work reveals a repeated failure, a durable workflow change, or a safety invariant. Avoid turning one project's structure into a universal rule.
