#!/usr/bin/env python3
"""Validate a minimal or compatible research workspace."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


PREFERRED = {
    "codex_entry": "AGENTS.md",
    "claude_entry": "CLAUDE.md",
    "rules": "WORKSPACE_RULES.md",
    "project_map": "PROJECT.md",
}

NAMED_CANDIDATES = {
    "rules": ("WORKSPACE_RULES.md", "PROJECT_RULES.md", "RULES.md", "CONTRIBUTING.md"),
    "project_map": ("PROJECT.md", "PROJECT_OVERVIEW.md", "WORKSPACE.md", "README.md"),
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"<PROJECT_[A-Z0-9_]+>"),
)
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")

SOURCE_PATTERN = re.compile(
    r"source[- ]?routing|task[- ]?routed|retrieval|信息源|来源|检索",
    re.IGNORECASE,
)
PERSISTENCE_PATTERN = re.compile(
    r"persistence|write[- ]?back|knowledgebase promotion|写回|沉淀|持久|知识库",
    re.IGNORECASE,
)
SAFETY_PATTERN = re.compile(
    r"safety|privacy|sensitive|deidentified|安全|隐私|脱敏|禁止|不得",
    re.IGNORECASE,
)
PROJECT_SIGNALS = (
    re.compile(r"project (?:name|role)|项目(?:名称|定位|角色)", re.IGNORECASE),
    re.compile(r"knowledgebase|知识库", re.IGNORECASE),
    re.compile(r"workspace map|local (?:path|directory)|目录|路径", re.IGNORECASE),
    re.compile(r"active workstream|当前工作流|活跃工作流", re.IGNORECASE),
    re.compile(r"canonical working file|canonical file|权威文件|标准工作文件", re.IGNORECASE),
    re.compile(r"special constraint|当前约束|特殊约束", re.IGNORECASE),
)

SENSITIVE_NAME = re.compile(
    r"(?:非脱敏|未脱敏|not[-_ ]?de[-_ ]?identified|confidential|credentials?|secret|\.env(?:\.|$))",
    re.IGNORECASE,
)
DATA_SUFFIXES = {
    ".bam", ".bai", ".cram", ".fastq", ".fq", ".vcf", ".bcf",
    ".xlsx", ".xls", ".csv", ".tsv", ".pdf", ".pptx", ".docx",
}
MAX_TEXT_BYTES = 512 * 1024


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_text(path: Path) -> str | None:
    try:
        if not path.is_file() or path.stat().st_size > MAX_TEXT_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def root_markdown(root: Path) -> list[Path]:
    return sorted(path for path in root.glob("*.md") if path.is_file())


def rules_score(text: str) -> int:
    return sum(
        bool(pattern.search(text))
        for pattern in (SOURCE_PATTERN, PERSISTENCE_PATTERN, SAFETY_PATTERN)
    )


def project_score(text: str) -> int:
    return sum(bool(pattern.search(text)) for pattern in PROJECT_SIGNALS)


def local_links(text: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        found.append(target.strip("<>"))
    return found


def choose_named(root: Path, names: tuple[str, ...], scorer, minimum: int) -> Path | None:
    for name in names:
        path = root / name
        text = read_text(path)
        if text is not None and scorer(text) >= minimum:
            return path
    for path in root_markdown(root):
        text = read_text(path)
        if text is not None and scorer(text) >= minimum:
            return path
    return None


def choose_entry(root: Path, preferred: str, client_name: str, rules: Path | None) -> Path | None:
    preferred_path = root / preferred
    preferred_text = read_text(preferred_path)
    if preferred_text is not None and preferred_text.strip():
        return preferred_path
    for path in root_markdown(root):
        text = read_text(path)
        if text is None or client_name.lower() not in text.lower():
            continue
        if rules is None or rules.name in text or "rules" in text.lower() or "规则" in text:
            return path
    return None


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    compatible_roles: list[str] = []
    info: dict[str, object] = {}

    if not root.is_dir():
        return {
            "status": "invalid",
            "errors": [f"Not a directory: {root}"],
            "warnings": [],
            "info": {},
        }

    rules = choose_named(root, NAMED_CANDIDATES["rules"], rules_score, 3)
    project_map = choose_named(root, NAMED_CANDIDATES["project_map"], project_score, 3)
    codex_entry = choose_entry(root, PREFERRED["codex_entry"], "Codex", rules)
    claude_entry = choose_entry(root, PREFERRED["claude_entry"], "Claude", rules)
    resolved = {
        "codex_entry": codex_entry,
        "claude_entry": claude_entry,
        "rules": rules,
        "project_map": project_map,
    }

    for role, path in resolved.items():
        if path is None:
            errors.append(f"No compatible file found for role: {role}")
            continue
        relative = str(path.relative_to(root))
        if relative != PREFERRED[role]:
            compatible_roles.append(role)
            warnings.append(
                f"Using compatible {role} file {relative}; preferred name is {PREFERRED[role]}"
            )

    info["roles"] = {
        role: (str(path.relative_to(root)) if path is not None else None)
        for role, path in resolved.items()
    }

    if rules is not None:
        for role in ("codex_entry", "claude_entry"):
            entry = resolved[role]
            if entry is None or entry == rules:
                continue
            text = read_text(entry) or ""
            rules_relative = str(rules.relative_to(root))
            if rules.name not in text and rules_relative not in text:
                warnings.append(
                    f"{entry.relative_to(root)} does not explicitly point to {rules_relative}"
                )

    selected = {path for path in resolved.values() if path is not None}
    for path in sorted(selected):
        content = read_text(path)
        relative = path.relative_to(root)
        if content is None:
            errors.append(f"Cannot read governance file as UTF-8 text: {relative}")
            continue
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

    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        info["git"] = {
            "initialized": False,
            "message": "当前项目尚未启用 Git，如需可显式初始化。",
        }
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

    status = "invalid" if errors else ("compatible" if compatible_roles else "valid")
    info["compatible_roles"] = sorted(compatible_roles)
    return {
        "status": status,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "info": info,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a research workspace")
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
        print(f"Status: {result['status']}")
        print(f"Errors: {len(errors)}")
        for item in errors:
            print(f"  ERROR: {item}")
        print(f"Warnings: {len(warnings)}")
        for item in warnings:
            print(f"  WARN: {item}")
        print(f"Roles: {result['info'].get('roles', {})}")
        print(f"Git: {result['info'].get('git', {})}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
