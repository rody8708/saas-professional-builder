#!/usr/bin/env python3
"""Validate packaging as data, without executing profile commands.

This verifies declared evidence is present, not that its claims are true.
Run the documented profile tests separately to verify their results.
"""
from __future__ import annotations
import argparse
import json
import re
import stat
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urlsplit

GATES = {"architecture", "tenant-isolation", "authorization", "data-integrity",
         "retry-safety", "real-entrypoint", "operations"}
REQUIRED_FILES = ("SKILL.md", "README.md", "profiles/README.md", "profiles/registry.json",
                  "docs/validation.md", "docs/provenance.md")
GENERATED_DIRS = {"vendor", "node_modules", "__pycache__", ".venv", "bin", "obj", "build",
                  "coverage", ".phpunit.cache", "logs", "backups", "private"}
FORBIDDEN_SUFFIXES = {".zip", ".7z", ".tar", ".gz", ".sql", ".db", ".sqlite", ".sqlite3", ".log", ".pyc",
                      ".pem", ".key", ".p12", ".pfx", ".dll", ".exe", ".pdb"}
STACK_PATTERN = re.compile(
    r"\b(?:composer|phpunit|phpstan|PDO|curl_init|pubspec|flutter|pytest|mypy|"
    r"artisan|symfony|laravel|nestjs|django)\b|"
    r"\b(?:npm|pnpm|yarn|pip|dotnet)\s+(?:run|test|install|build|add|restore)\b|"
    r"declare\s*\(\s*strict_types", re.IGNORECASE)
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    re.compile(r"\bsk-(?:proj-|live_)[A-Za-z0-9_-]{24,}\b"),
)

def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())

def strings(value: object, allow_empty: bool = False) -> bool:
    return (isinstance(value, list) and (allow_empty or bool(value))
            and all(nonempty(item) for item in value) and len(value) == len(set(value)))

def is_linklike(path: Path) -> bool:
    """Include Windows junctions/reparse points without following their targets."""
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    return (stat.S_ISLNK(metadata.st_mode)
            or bool(getattr(metadata, "st_file_attributes", 0) & 0x400))

def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return ["Package root is missing or is not a directory"]

    def error(where: str, message: str) -> None:
        errors.append(f"{where}: {message}")

    def safe_file(base: Path, value: object, where: str) -> Path | None:
        if not nonempty(value):
            error(where, "expected a nonempty relative file path")
            return None
        posix, windows = PurePosixPath(value), PureWindowsPath(value)
        if (posix.is_absolute() or windows.is_absolute() or windows.drive
                or "\\" in value or ".." in posix.parts or ":" in value):
            error(where, "unsafe path; use a relative path inside its profile")
            return None
        candidate = base.joinpath(*posix.parts)
        if any(is_linklike(p) for p in [candidate, *candidate.parents]):
            error(where, "symbolic links and reparse points are not allowed")
            return None
        resolved = candidate.resolve()
        if not resolved.is_relative_to(base.resolve()) or not resolved.is_relative_to(root):
            error(where, "path escapes its allowed directory")
            return None
        if not resolved.is_file():
            error(where, "referenced file does not exist")
            return None
        return resolved

    def read_json(path: Path, where: str) -> dict | None:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            error(where, "expected valid UTF-8 JSON")
            return None
        if not isinstance(value, dict):
            error(where, "expected a JSON object")
            return None
        return value

    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            error(name, "required file is missing")
    for name in ("core", "prompts", "templates"):
        if not (root / name).is_dir():
            error(name, "required shared directory is missing")
    registry_path = safe_file(root, "profiles/registry.json", "registry")
    registry = read_json(registry_path, "registry") if registry_path is not None else None
    if registry is not None:
        if type(registry.get("schema_version")) is not int or registry["schema_version"] != 1:
            error("registry", "unsupported schema_version")
        if registry.get("selection_policy") != "explicit-or-detected-never-default":
            error("registry", "stack selection must be explicit or detected, never default")
        if any("default" in key.lower() for key in registry if key != "selection_policy"):
            error("registry", "a default stack is not allowed")
        gates = registry.get("required_project_gates")
        if not strings(gates) or set(gates) != GATES:
            error("registry", "all seven required project gates must be preserved")
        entries = registry.get("profiles")
        if not isinstance(entries, list) or not entries:
            error("registry", "profiles must be a nonempty list")
            entries = []
        seen: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict) or not nonempty(entry.get("id")):
                error("registry", "each profile needs an id and path")
                continue
            profile_id = entry["id"]
            if not re.fullmatch(r"[a-z][a-z0-9-]*", profile_id):
                error("registry", "invalid profile id")
                continue
            if profile_id in seen:
                error(profile_id, "duplicate profile id")
            seen.add(profile_id)
            if entry.get("path") != f"{profile_id}/profile.json":
                error(profile_id, "manifest path must match its profile id")
                continue
            manifest_path = safe_file(root / "profiles", entry["path"], profile_id)
            if manifest_path is None:
                continue
            profile = read_json(manifest_path, profile_id)
            if profile is None:
                continue
            if profile.get("id") != profile_id:
                error(profile_id, "manifest id differs from registry")
            if not nonempty(profile.get("name")) or not strings(profile.get("languages")):
                error(profile_id, "name and languages are required")
            if any("default" in key.lower() for key in profile):
                error(profile_id, "a default stack is not allowed")
            status = profile.get("status")
            if not isinstance(status, str) or status not in {"controls-validated", "guidance-only"}:
                error(profile_id, "invalid validation status")
            base = manifest_path.parent
            safe_file(base, profile.get("guide"), f"{profile_id}.guide")
            for key in ("templates", "tests"):
                values = profile.get(key)
                if not strings(values, allow_empty=True):
                    error(profile_id, f"{key} must be an array of unique relative paths")
                    continue
                for value in values:
                    safe_file(base, value, f"{profile_id}.{key}")
            controls = profile.get("implemented_controls")
            if not strings(controls, allow_empty=True):
                error(profile_id, "implemented_controls must be an array of unique names")
            profile_gates = profile.get("project_gates")
            if not strings(profile_gates) or set(profile_gates) != GATES:
                error(profile_id, "all seven project gates are required")
            evidence = profile.get("validation")
            if not isinstance(evidence, dict):
                error(profile_id, "validation evidence is required")
                evidence = {}
            for key in ("environment", "command", "result"):
                if not nonempty(evidence.get(key)):
                    error(profile_id, f"validation.{key} must be nonempty")
            if not strings(evidence.get("limitations")):
                error(profile_id, "validation limitations must be explicit")
            if status == "controls-validated" and (
                not strings(profile.get("tests")) or not strings(controls)
            ):
                error(profile_id, "validated controls require executable tests and named controls")

    def walk(directory: Path):
        try:
            children = sorted(directory.iterdir())
        except OSError:
            error(directory.relative_to(root).as_posix(), "directory cannot be inspected")
            return
        for child in children:
            if child.name == ".git":
                continue
            if is_linklike(child):
                error(child.relative_to(root).as_posix(), "symbolic link or reparse point is not allowed")
                continue
            yield child
            if child.is_dir() and child.name not in GENERATED_DIRS:
                yield from walk(child)

    for path in walk(root):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        name = relative.as_posix()
        if path.is_dir():
            if path.name in GENERATED_DIRS:
                error(name, "generated or operational directory is present")
            continue
        if (path.suffix.lower() in FORBIDDEN_SUFFIXES
                or path.name.startswith(".env") and path.name != ".env.example"
                or path.name == ".phpunit.result.cache"):
            error(name, "operational, binary or generated artifact is present")
            continue
        # Every delivered file is inspected, including .txt and .env.example.
        # Binary assets require an explicit future packaging policy, not a skip.
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            error(name, "file is not readable UTF-8 text")
            continue
        if "\x00" in content or "\ufffd" in content:
            error(name, "invalid text characters")
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            error(name, "possible credential/private key detected; inspect locally")
        if relative.parts[0] in {"core", "prompts", "templates"} and STACK_PATTERN.search(content):
            error(name, "stack-specific tooling belongs in a technical profile")
        if path.suffix.lower() != ".md":
            continue
        fence = None
        for line in content.splitlines():
            match = FENCE.match(line)
            if match:
                mark, remainder = match.groups()
                if fence is None:
                    fence = mark
                elif mark[0] == fence[0] and len(mark) >= len(fence) and not remainder.strip():
                    fence = None
                continue
            if fence is not None:
                continue
            for match in LINK.finditer(line):
                target = match.group(1).strip("<>")
                try:
                    scheme = urlsplit(target).scheme
                except ValueError:
                    error(name, "malformed Markdown link")
                    continue
                if target.startswith("#") or scheme:
                    continue
                decoded = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not decoded:
                    continue
                destination = (path.parent / decoded).resolve()
                if not destination.is_relative_to(root) or not destination.exists():
                    error(name, "local Markdown link is missing or escapes the package")
        if fence is not None:
            error(name, "unclosed Markdown code fence")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    errors = validate(parser.parse_args().root)
    for finding in errors:
        print(f"ERROR {finding}")
    if errors:
        print(f"Package validation failed: {len(errors)} finding(s)")
        return 1
    print("Package structure, profile declarations, shared neutrality and local file links: PASS")
    print("Application behavior and declared test results are not executed or certified by this check.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
