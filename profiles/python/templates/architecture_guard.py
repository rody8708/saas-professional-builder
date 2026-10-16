#!/usr/bin/env python3
"""Bounded AST dependency checks; never import or execute application modules."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import sys
from typing import Any

EXCLUDED_DIRECTORIES = {"__pycache__", ".venv", "venv", ".git", "vendor"}


class PolicyError(ValueError):
    """Configuration or source cannot be inspected reliably."""


def string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise PolicyError(f"{label} must be a list of nonempty strings")
    return value


def inside_path(root: Path, value: str, label: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise PolicyError(f"{label} must be a relative path")
    unresolved = root / value
    if any(part == ".." for part in Path(value).parts):
        raise PolicyError(f"{label} must not contain '..'")
    current = root
    for part in Path(value).parts:
        current = current / part
        if current.is_symlink():
            raise PolicyError(f"{label} must not traverse symlinks")
    resolved = unresolved.resolve()
    if not resolved.is_relative_to(root):
        raise PolicyError(f"{label} escapes project root")
    return resolved


def source_files(directory: Path) -> list[Path]:
    result: list[Path] = []
    for item in sorted(directory.iterdir()):
        if item.name in EXCLUDED_DIRECTORIES:
            continue
        if item.is_symlink():
            raise PolicyError(f"source symlink is not inspected: {item.name}")
        if item.is_dir():
            result.extend(source_files(item))
        elif item.suffix == ".py":
            result.append(item)
    return result


def matches_prefix(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(prefix + ".")


def module_context(file: Path, source: Path, package: str) -> str:
    pieces = list(file.relative_to(source).with_suffix("").parts)
    if pieces[-1] == "__init__":
        pieces.pop()
    else:
        pieces = pieces[:-1]
    return ".".join([package, *pieces])


def resolve_relative(module: str, level: int, context: str) -> str:
    parts = context.split(".")
    if level > len(parts):
        raise PolicyError("relative import escapes the configured package")
    return ".".join([*parts[:len(parts) - level + 1], *([module] if module else [])])


def imports(tree: ast.AST, context: str) -> list[tuple[int, str]]:
    """Static imports and literal known dynamic loaders, including common aliases."""
    found: list[tuple[int, str]] = []
    importlib_names = {"importlib"}
    loader_names = {"__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((node.lineno, alias.name))
                if alias.name == "importlib":
                    importlib_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            base = resolve_relative(node.module or "", node.level, context) if node.level else (node.module or "")
            found.append((node.lineno, base))
            for alias in node.names:
                if alias.name != "*":
                    found.append((node.lineno, ".".join(filter(None, [base, alias.name]))))
                if base == "importlib" and alias.name == "import_module":
                    loader_names.add(alias.asname or alias.name)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        known_loader = isinstance(function, ast.Name) and function.id in loader_names
        known_loader |= (isinstance(function, ast.Attribute) and function.attr == "import_module"
                         and isinstance(function.value, ast.Name) and function.value.id in importlib_names)
        if not known_loader:
            continue
        argument = node.args[0] if node.args else next((kw.value for kw in node.keywords if kw.arg == "name"), None)
        if not isinstance(argument, ast.Constant) or not isinstance(argument.value, str):
            found.append((node.lineno, "<unresolved-dynamic-import>"))
        elif argument.value.startswith("."):
            # Runtime package arguments and importlib resolution need a semantic tool.
            found.append((node.lineno, "<unresolved-dynamic-import>"))
        else:
            found.append((node.lineno, argument.value))
    return found


def inspect(root: Path, policy: dict[str, Any]) -> tuple[int, list[str]]:
    if not isinstance(policy, dict):
        raise PolicyError("policy must be a JSON object")
    package = policy.get("package")
    if not isinstance(package, str) or not package or any(not part.isidentifier() for part in package.split(".")):
        raise PolicyError("package must be a dotted Python package name")
    source = inside_path(root, policy.get("source_root"), "source_root")
    if not source.is_dir():
        raise PolicyError("required source_root is missing")
    layers = policy.get("layers")
    if not isinstance(layers, dict) or set(layers) != {"domain", "application"}:
        raise PolicyError("layers must configure domain and application")
    count = 0
    violations: list[str] = []
    for layer, rules in layers.items():
        if not isinstance(rules, dict):
            raise PolicyError(f"{layer} policy must be an object")
        internal = string_list(rules.get("forbidden_internal_layers"), f"{layer}.forbidden_internal_layers")
        external = string_list(rules.get("forbidden_imports"), f"{layer}.forbidden_imports")
        directory = inside_path(source, layer, layer)
        if not directory.is_dir():
            raise PolicyError(f"required layer root is missing: {layer}")
        files = source_files(directory)
        if not files:
            raise PolicyError(f"no Python files inspected in required layer: {layer}")
        forbidden = [*external, *(f"{package}.{name}" for name in internal)]
        for file in files:
            relative = file.relative_to(root).as_posix()
            try:
                tree = ast.parse(file.read_text(encoding="utf-8-sig"), filename=relative)
            except (SyntaxError, UnicodeError) as error:
                raise PolicyError(f"cannot parse {relative}: {type(error).__name__}") from error
            count += 1
            for line, module in imports(tree, module_context(file, source, package)):
                if module == "<unresolved-dynamic-import>" or any(matches_prefix(module, prefix) for prefix in forbidden):
                    violations.append(f"{relative}:{line}: {layer} imports forbidden/unresolved dependency {module}")
    return count, sorted(set(violations))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    try:
        root = args.project_root.resolve(strict=True)
        if not root.is_dir():
            raise PolicyError("project-root is not a directory")
        policy = json.loads(args.config.read_text(encoding="utf-8"))
        count, violations = inspect(root, policy)
    except (OSError, ValueError, PolicyError) as error:
        print(f"Architecture inspection failed: {error}", file=sys.stderr)
        return 2
    if violations:
        print("\n".join(violations), file=sys.stderr)
        return 1
    print(f"Architecture controls passed: {count} Python files inspected; configured imports only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
