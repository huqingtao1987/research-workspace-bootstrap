#!/usr/bin/env python3
"""Verify that Codex and Claude skill payloads differ only by Claude frontmatter."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "skills" / "research-workspace-bootstrap"
CLAUDE = ROOT / "claude-plugin" / "skills" / "research-workspace-bootstrap"


def files_below(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def normalized(path: Path) -> bytes:
    data = path.read_bytes()
    if path.name == "SKILL.md":
        data = data.replace(b"disable-model-invocation: true\n", b"")
    return data.rstrip() + b"\n"


def main() -> int:
    codex_files = files_below(CODEX)
    claude_files = files_below(CLAUDE)
    if codex_files != claude_files:
        print("Skill file sets differ")
        print(f"Only in Codex: {sorted(map(str, codex_files - claude_files))}")
        print(f"Only in Claude: {sorted(map(str, claude_files - codex_files))}")
        return 1

    mismatches = [
        str(relative)
        for relative in sorted(codex_files)
        if normalized(CODEX / relative) != normalized(CLAUDE / relative)
    ]
    if mismatches:
        print(f"Content differs: {mismatches}")
        return 1

    print("Codex and Claude skill payloads are in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
