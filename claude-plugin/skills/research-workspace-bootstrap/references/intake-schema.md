# Minimal workspace profile

Extract only what is needed to navigate the project and choose safe behavior. PROJECT.md is a workspace map, not a full scientific summary.

## Core fields

| Field | Purpose | When unknown |
|---|---|---|
| project_name | Human-readable project identity | Use the directory name provisionally and label it |
| project_role | Flagship, closure, resource, collaboration, manuscript, grant, analysis, or another user-defined role | Record as unknown; do not force a category |
| knowledgebase_project_page | Long-term scientific state source, if one exists | State that no mapping is confirmed |
| local_paths | Major existing directories and their actual roles | List only verified paths |
| active_workstreams | Work currently in motion | Include only supported workstreams |
| canonical_working_files | Existing files that own current state, plans, claims, drafts, or decisions | Name only files whose role is evident |
| special_constraints | Privacy, unpublished work, compute, collaboration, write, or access boundaries | Ask if ambiguity creates material risk |

Optional task-specific facts such as deliverables, stage, owners, completion criteria, compute environment, and deadlines belong in PROJECT.md or a natural working artifact only when they improve navigation or current work.

## Existing-role mapping

Before creating a preferred file, ask whether an existing file already carries the role. Record:

- role served;
- actual file path;
- why it appears canonical;
- conflicts or uncertainty;
- whether a small navigation link is sufficient.

Do not create a generic task, evidence, state, decision, or summary file merely to hold unknowns. Report non-blocking unknowns in the handoff or place them in an already active project artifact.

## Ask before proceeding when

- the target project root is unclear;
- sensitive or non-deidentified content might need to be opened;
- a proposed change would move, overwrite, or replace useful existing structure;
- two rules conflict in a way that affects safety or scientific interpretation;
- the user has not explicitly opted into a requested Git mutation.

