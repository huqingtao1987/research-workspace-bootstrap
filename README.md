# Research Workspace Bootstrap

Version 0.1.0

Turn a folder containing existing research material into a durable project workspace for Codex and Claude Code.

The skill performs a read-only inventory, identifies authoritative sources and sensitive boundaries, creates a minimal project-management layer, writes a baseline summary, validates the result, and initializes Git without committing datasets or existing binary material.

The repository contains a Codex skill under skills/ and a Claude Code compatibility copy under claude-plugin/skills/. Their workflow content is identical; only Claude's explicit-invocation frontmatter differs. Run scripts/check_skill_parity.py after edits to prevent drift.

## What it creates

The default research workspace includes:

~~~text
AGENTS.md
CLAUDE.md
WORKSPACE_RULES.md
README.md
项目管理/
├── 当前状态.md
├── 证据索引.md
├── 待办与阻塞.md
├── 决策记录.md
├── 阶段总结.md
├── 模板/分析任务包.md
└── 历史版本/
~~~

The structure is reduced for bounded one-off projects and extended only when the project type requires it.

## Safety defaults

- Existing research files are not moved, deleted, or overwritten.
- Files marked non-deidentified, confidential, restricted, or forbidden remain unread.
- Knowledgebases, Zotero, and external systems remain read-only unless separately authorized.
- Existing rules are archived before substantial revision.
- Git stages only generated governance Markdown and safe configuration files.
- Existing data, PDFs, slides, images, credentials, and analysis outputs remain untracked by default.
- No Git remote is created or pushed by the skill.

## Install in Codex

Use the built-in skill installer and provide the GitHub skill path:

~~~text
$skill-installer Install the research-workspace-bootstrap skill from
https://github.com/huqingtao1987/research-workspace-bootstrap/tree/main/skills/research-workspace-bootstrap
~~~

Then invoke:

~~~text
$research-workspace-bootstrap Initialize the current research project folder.
~~~

Codex installation guidance: https://learn.chatgpt.com/docs/build-skills

## Install in Claude Code

Add the GitHub repository as a marketplace:

~~~text
/plugin marketplace add huqingtao1987/research-workspace-bootstrap
/plugin install research-workspace-bootstrap@huqingtao-research-skills
~~~

If prompted, run:

~~~text
/reload-plugins
~~~

Invoke the installed plugin skill:

~~~text
/research-workspace-bootstrap:research-workspace-bootstrap
~~~

For local development:

~~~bash
claude --plugin-dir ./claude-plugin
~~~

Claude Code plugin guidance: https://code.claude.com/docs/en/plugins

## Expected Git result inside the target project

The Git initialization step applies to the research project folder on which the skill is invoked. If that target project is not already a Git repository, the skill:

1. creates or minimally extends a safe .gitignore;
2. runs git init -b main;
3. validates candidate files and sizes;
4. stages only newly generated governance files by explicit path;
5. attempts an initial commit named chore: initialize research workspace;
6. leaves all pre-existing data and binary material untracked.

If Git author identity is unavailable, the repository is still initialized but the skill does not change global or local identity without permission.

This distribution repository is also a Git repository because GitHub distribution requires it, but that is separate from the target-project initialization behavior above.

## Validate a generated workspace

From this repository:

~~~bash
python3 skills/research-workspace-bootstrap/scripts/validate_workspace.py /absolute/path/to/project
~~~

The validator checks required files, internal Markdown links, unresolved template tokens, merge markers, obvious sensitive-file warnings, and Git repository status.

## Development status

This is an initial version intended to be calibrated on real projects. Add rules only after repeated failures, durable workflow changes, or newly discovered safety invariants.
