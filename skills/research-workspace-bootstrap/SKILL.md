---
name: research-workspace-bootstrap
description: Initialize, audit, or reorganize a research project workspace so its rules, evidence sources, status, decisions, tasks, stage summaries, and Git history can grow safely over time. Use when starting a project folder from existing materials, standardizing an established research folder, or updating its workspace governance. Do not use for scientific analysis itself, manuscript drafting, or unrestricted bulk file reorganization.
---

# Research Workspace Bootstrap

Create a durable research workspace around the user's existing materials. Preserve scientific content, make uncertainty visible, and leave a small auditable governance layer that works in both Codex and Claude Code.

## Authorization boundary

Explicit invocation authorizes:

- read-only inventory of the target project;
- creation or revision of governance Markdown files;
- dated rollback copies of governance files being replaced;
- local validation;
- Git initialization when the target is not already a repository;
- an initial commit containing only newly generated, safe governance files.

It does not authorize:

- opening sensitive or non-deidentified data without explicit permission;
- changing scientific data, analyses, results, manuscripts, the user's knowledge base, or Zotero library;
- moving, deleting, or overwriting existing source materials;
- staging datasets, binaries, credentials, secrets, or unrelated pre-existing files;
- creating a remote repository, adding a remote, or pushing to a remote.

Stop and ask when a required action crosses this boundary.

## Operating modes

- Initialize: add governance to a new or lightly organized folder.
- Audit: inspect an existing governance layer and report gaps without changing files unless asked.
- Update: revise governance after the workflow has been tested in real work.

Infer the mode from the request. If ambiguity changes whether files will be written, state the assumed mode before proceeding.

## Workflow

### 1. Resolve the project root and governing instructions

Confirm the target directory. Read any existing AGENTS.md, CLAUDE.md, WORKSPACE_RULES.md, README.md, or equivalent before other work. Check whether the directory is already inside a Git worktree.

Inventory names, paths, types, sizes, and dates with read-only tools. Prefer rg --files and targeted metadata commands. Do not open large binaries or potentially sensitive content merely to classify it.

### 2. Build the minimum project profile

Use references/intake-schema.md. Extract only facts supported by the user's message or project files. Never invent sample counts, endpoints, project stage, target journal, storage paths, owners, deadlines, or data permissions.

Record unknown but non-blocking fields in the task-and-blocker file. Ask the user only when an unknown materially changes safety or project structure.

### 3. Choose the appropriate modules

Use references/project-type-routing.md. Apply the smallest useful combination of portfolio-role and work-type modules. A one-off task should not receive the same structure as a long-running flagship project.

### 4. Announce the proposed change set

Before editing, state:

- files to create or revise;
- how revised governance files will be archived;
- current Git state;
- which generated files would enter an initial commit;
- which existing and untracked files will remain untouched.

### 5. Create a minimal governance layer

Adapt the files in assets/base rather than copying placeholders unchanged. The normal structure is:

~~~text
AGENTS.md
CLAUDE.md
WORKSPACE_RULES.md
README.md
项目管理/
  当前状态.md
  证据索引.md
  待办与阻塞.md
  决策记录.md
  阶段总结.md
  模板/分析任务包.md
  历史版本/
~~~

AGENTS.md and CLAUDE.md should be short entry points. WORKSPACE_RULES.md is the single canonical rules document; avoid copying the same detailed rules into multiple files.

### 6. Preserve existing work

Do not move or rename source materials by default. Before replacing an existing governance file, copy it to 项目管理/历史版本 with a date and a superseded suffix. If the intended archive path already exists, choose a unique timestamped name.

Modify only the smallest necessary surface. When existing rules conflict, report the conflict and preserve the stricter safety constraint until the user decides.

### 7. Define evidence routing and write-back

Set the default evidence order to:

1. project-local files and results;
2. the user's designated knowledge base;
3. Zotero;
4. authoritative online sources.

Treat this as a search order, not automatic permission to write to those systems. Distinguish observed result, literature-supported interpretation, hypothesis, and decision. Require provenance for consequential claims.

Use balanced write-back by default: do not create a note for every conversation, but update the governance layer when a milestone, decision, reusable method, durable conclusion, or important blocker emerges.

### 8. Capture a baseline

Summarize the current stage, known inputs, existing outputs, active question, next action, and blockers. Keep unsupported claims explicitly marked as unknown or provisional.

### 9. Establish Git safely

If the project is already a Git repository, preserve its branch, ignore rules, staging area, and history. Do not commit unless explicitly requested; report git status and the proposed diff instead.

If the project is not a Git repository:

1. minimally create or extend .gitignore without overwriting existing entries;
2. run git init -b main;
3. inspect candidate files and their sizes;
4. stage explicit generated governance paths only;
5. never use git add . or git add -A;
6. verify the staged list before committing;
7. commit with message chore: initialize research workspace.

Never stage pre-existing datasets, binaries, sensitive files, credentials, or unrelated work. If Git identity is missing, do not set it silently; leave the safe files staged or unstaged and report the exact blocker. Do not create or push a remote unless the user separately asks.

### 10. Validate

Run scripts/validate_workspace.py against the target project and apply references/acceptance-tests.md. Resolve structural errors. Treat warnings as review items, not automatic permission to alter scientific content.

### 11. Hand off

Report:

- operating mode and project type selected;
- files created, revised, and archived;
- how to roll back;
- validation results;
- Git branch and commit hash, or the precise reason no commit was made;
- untracked existing materials deliberately left outside Git;
- unresolved facts and the next recommended action.

## Maintenance rule

Evolve the workspace rules from observed friction. Promote a lesson into a durable rule or template when it recurs, affects safety or reproducibility, or saves meaningful future effort. Record substantive rule changes in the decision log and archive the superseded version.
