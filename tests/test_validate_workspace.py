#!/usr/bin/env python3

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills" / "research-workspace-bootstrap" / "scripts" / "validate_workspace.py"
SPEC = importlib.util.spec_from_file_location("workspace_validator", VALIDATOR)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


RULES = """# Rules

## Task-routed source routing
Use task-routed retrieval and the minimum source set.

## Persistence
Exploration stays in conversation; knowledgebase promotion needs separate authorization.

## Safety
Do not read sensitive material without permission.
"""

PROJECT = """# Project

## Project role
Collaboration project.

## Related knowledgebase project page
Not yet mapped.

## Workspace map
The local data directory contains inputs.

## Active workstreams
One active workstream.

## Existing canonical working files
The analysis plan is canonical.

## Special constraints
No sensitive data access.
"""


class ValidatorTests(unittest.TestCase):
    def write(self, root: Path, name: str, text: str) -> None:
        (root / name).write_text(text, encoding="utf-8")

    def test_minimal_workspace_without_git_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "WORKSPACE_RULES.md", RULES)
            self.write(root, "PROJECT.md", PROJECT)
            self.write(root, "AGENTS.md", "Read WORKSPACE_RULES.md before Codex work.\n")
            self.write(root, "CLAUDE.md", "Read WORKSPACE_RULES.md before Claude work.\n")

            result = MODULE.validate(root)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["errors"], [])
            self.assertFalse(result["info"]["git"]["initialized"])

    def test_mature_workspace_with_equivalent_files_is_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "AI_RULES.md", RULES)
            self.write(root, "WORKSPACE.md", PROJECT)
            self.write(
                root,
                "AI_ENTRY.md",
                "Codex and Claude should read AI_RULES.md before work.\n",
            )

            result = MODULE.validate(root)

            self.assertEqual(result["status"], "compatible")
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["info"]["roles"]["rules"], "AI_RULES.md")
            self.assertEqual(result["info"]["roles"]["project_map"], "WORKSPACE.md")

    def test_missing_project_map_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "WORKSPACE_RULES.md", RULES)
            self.write(root, "AGENTS.md", "Read WORKSPACE_RULES.md before Codex work.\n")
            self.write(root, "CLAUDE.md", "Read WORKSPACE_RULES.md before Claude work.\n")

            result = MODULE.validate(root)

            self.assertEqual(result["status"], "invalid")
            self.assertTrue(
                any("project_map" in error for error in result["errors"])
            )


if __name__ == "__main__":
    unittest.main()
