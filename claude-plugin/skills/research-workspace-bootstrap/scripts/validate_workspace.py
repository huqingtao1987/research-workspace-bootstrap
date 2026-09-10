#!/usr/bin/env python3
"""Validate a bootstrapped research workspace using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "WORKSPACE_RULES.md",
    "README.md",
    "项目管理/当前状态.md",
    "项目管理/证据索引.md",
    "项目管理/待办与阻塞.md",
)

OPTIONAL_GOVERNANCE = (
    "项目管理/决策记录.md",
    "项目管理/阶段总结.md",
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"<PROJECT_[A-Z0-9_]+>"),
)

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
SENSITIVE_NAME = re.compile(
    r"(?:非脱敏|未脱敏|not[-_ ]?de[-_ ]?identified|confidential|credentials?|secret|\.env(?:\.|$))",
    re.IGNORECASE,
)
DATA_SUFFIXES = {
    ".bam", ".bai", ".cram", ".fastq", ".fq", ".vcf", ".bcf",
    ".xlsx", ".xls", ".csv", ".tsv", ".pdf", ".pptx", ".docx",
}


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in REQUIRED_FILES + OPTIONAL_GOVERNANCE:
        path = root / relative
        if path.is_file():
            files.append(path)
    management = root / "项目管理"
    if management.is_dir():
        for path in management.rglob("*.md"):
            if "历史版本" not in path.parts and path not in files:
                files.append(path)
    return files


def local_links(text: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        found.append(target.strip("<>"))
    return found


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    info: dict[str, object] = {}

    if not root.is_dir():
        return {"errors": [f"Not a directory: {root}"], "warnings": [], "info": {}}

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    for entry in ("AGENTS.md", "CLAUDE.md"):
        path = root / entry
        if path.is_file() and "WORKSPACE_RULES.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"{entry} does not point to WORKSPACE_RULES.md")

    for path in markdown_files(root):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Not valid UTF-8: {path.relative_to(root)}")
            continue
        relative = path.relative_to(root)
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(content):
                errors.append(f"Unresolved template token in {relative}")
                break
        if any(marker in content for marker in CONFLICT_MARKERS):
            errors.append(f"Merge conflict marker in {relative}")
        for link in local_links(content):
            destination = (path.parent / link).resolve()
            try:
                destination.relative_to(root.resolve())
            except ValueError:
                warnings.append(f"Link leaves project root: {relative} -> {link}")
                continue
            if not destination.exists():
                errors.append(f"Broken local link: {relative} -> {link}")

    for path in root.rglob("*"):
        if path.is_file() and SENSITIVE_NAME.search(str(path.relative_to(root))):
            warnings.append(f"Potentially sensitive filename; review access and Git status: {path.relative_to(root)}")

    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        errors.append("Target is not a Git worktree")
        info["git"] = {"initialized": False}
    else:
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        head = run_git(root, "rev-parse", "--short", "HEAD")
        tracked = run_git(root, "ls-files", "-z")
        tracked_names = [item for item in tracked.stdout.split("\0") if item]
        info["git"] = {
            "initialized": True,
            "branch": branch or None,
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "tracked_count": len(tracked_names),
        }
        for name in tracked_names:
            path = root / name
            lower_name = name.lower()
            suffix = path.suffix.lower()
            if SENSITIVE_NAME.search(name):
                warnings.append(f"Potentially sensitive tracked file: {name}")
            if suffix in DATA_SUFFIXES or lower_name.endswith((".fastq.gz", ".fq.gz", ".vcf.gz")):
                warnings.append(f"Data or document file is tracked; confirm intent: {name}")
            if path.is_file() and path.stat().st_size > 10 * 1024 * 1024:
                warnings.append(f"Tracked file exceeds 10 MiB; confirm intent: {name}")

    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings)), "info": info}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a bootstrapped research workspace")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = args.project_root.expanduser().resolve()
    result = validate(root)
    errors = result["errors"]
    warnings = result["warnings"]

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Workspace: {root}")
        print(f"Errors: {len(errors)}")
        for item in errors:
            print(f"  ERROR: {item}")
        print(f"Warnings: {len(warnings)}")
        for item in warnings:
            print(f"  WARN: {item}")
        git_info = result["info"].get("git", {})
        if git_info:
            print(f"Git: {git_info}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
