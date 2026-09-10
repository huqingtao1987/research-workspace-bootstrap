# Research Workspace Bootstrap

Version 0.2.0

Turn an existing research directory into a durable AI workspace with the least necessary structure, then let it grow only when real scientific work creates a reason to persist something.

The governing principles are:

- minimal bootstrap;
- grow on demand;
- adapt to useful existing structure.

Prefer adapting to an existing useful project structure over imposing the skill's preferred structure. Templates are defaults for missing structure, not schemas that every project must conform to.

The skill organizes navigation, working boundaries, source routing, and persistence. It does not execute the project's scientific analysis.

## Default bootstrap

A new or lightly organized project receives only four files by default:

~~~text
AGENTS.md
CLAUDE.md
WORKSPACE_RULES.md
PROJECT.md
~~~

- AGENTS.md is the short Codex entry point.
- CLAUDE.md is the short Claude Code entry point.
- WORKSPACE_RULES.md contains shared operating, safety, persistence, and source-routing rules.
- PROJECT.md maps the concrete workspace: project name and role, related knowledgebase project page, major local paths and their roles, active workstreams, canonical working files, and current special constraints.

PROJECT.md is a navigation map. It does not copy the project's complete scientific state. That state remains in the related knowledgebase project page or in established project-local working files.

README.md is optional and may remain the human-facing overview when it is already useful.

## Grow-on-demand artifacts

The skill does not create an empty universal project-management tree. Artifacts appear only when real work crosses a persistence threshold.

Examples include:

- paper: claim-evidence.md, figure-plan.md, manuscript.md;
- grant: grant-plan.md, grant-draft.md;
- analysis: analysis-plan.md, data-inventory.md, analysis-task.md;
- database or resource: database-state.md, data-pipeline.md, release-plan.md.

These names are examples, not required structure. Existing equivalent files and locations take precedence.

## Artifact persistence gate

### Exploration

Ordinary discussion, alternatives, and unconfirmed reasoning stay in conversation.

### Stable working conclusion

A conclusion that must survive across conversations may be written to the natural project-local plan or state file.

### Active artifact production

When sustained drafting of a manuscript, grant, analysis plan, release plan, or other formal output has begun, the relevant draft may be created or updated.

### Long-term scientific state change

The skill may suggest updating the related knowledgebase project page when an important scientific change is stable. It does not modify the knowledgebase without separate authorization.

Project-local persistence is not knowledgebase promotion. They use different thresholds.

## Existing-workspace mode

For a mature project, the skill first audits what already works:

1. identify existing files that serve canonical roles;
2. preserve useful directories and working files;
3. fill only genuine navigation or safety gaps;
4. avoid renaming, moving, duplicating, or recreating structure to match templates.

A HERC6-like mature workspace should therefore remain recognizably itself. The 生命组学 workspace is one useful example of a project-specific implementation, not a schema that HERC6, sc-eQTL, COReD, or other projects must follow.

## Task-routed progressive retrieval

Progressive retrieval is task-routed, not a mandatory local-to-knowledgebase-to-Zotero-to-Web cascade.

- Current project status: PROJECT.md, relevant working files, and the related knowledgebase project page.
- Local analysis: relevant data and analysis files.
- Historical decisions: the specific decision record or raw history only when needed.
- Literature evidence: Zotero.
- Novelty, current landscape, or completeness: Zotero and Web as needed.
- Manuscript revision: manuscript plus the relevant figure or claim files before expanding scope.

The skill does not default to scanning the whole project, knowledgebase, raw archive, Zotero library, or open Web.

## New materials

When a new Word document, presentation, PDF, figure, or result enters the project, the skill reads only what the active task requires. It reports whether the material changes current state before updating a canonical file. Such an update requires user confirmation or an existing rule that already authorizes it.

Direct project results, literature-supported interpretations, Agent inferences, hypotheses or planned work, and user-confirmed decisions remain distinct. Preliminary or planned evidence is not established evidence.

## Git is opt-in

Version 0.2.0 changes Git from automatic initialization to explicit opt-in.

By default, the skill checks and reports Git status only. A non-Git project remains valid and receives this message:

~~~text
当前项目尚未启用 Git，如需可显式初始化。
~~~

Only a request such as 初始化 workspace，并启用 Git authorizes initialization, staging, or committing. When Git is requested, the existing safety rules remain:

- never use git add . or git add -A;
- stage only reviewed explicit paths;
- do not add data, binaries, sensitive files, credentials, or unrelated work;
- protect existing branch, history, staging, and ignore rules;
- do not create a GitHub repository or push without separate authorization.

## Install in Codex

Use the built-in installer with the GitHub skill path:

~~~text
$skill-installer Install the research-workspace-bootstrap skill from
https://github.com/huqingtao1987/research-workspace-bootstrap/tree/main/skills/research-workspace-bootstrap
~~~

Invoke it with:

~~~text
$research-workspace-bootstrap Minimally initialize the current research folder.
~~~

## Install in Claude Code

~~~text
/plugin marketplace add huqingtao1987/research-workspace-bootstrap
/plugin install research-workspace-bootstrap@huqingtao-research-skills
~~~

Invoke the installed plugin skill with:

~~~text
/research-workspace-bootstrap:research-workspace-bootstrap
~~~

For local plugin development:

~~~bash
claude --plugin-dir ./claude-plugin
~~~

## Validation

~~~bash
python3 skills/research-workspace-bootstrap/scripts/validate_workspace.py /absolute/path/to/project
python3 scripts/check_skill_parity.py
~~~

The workspace validator accepts both the preferred four-file bootstrap and mature compatible workspaces using equivalent files. It does not require a project-management tree or Git repository.

The repository carries a Codex skill under skills/ and a Claude Code compatibility copy under claude-plugin/skills/. Their workflow is identical; only Claude's explicit-invocation frontmatter differs.
