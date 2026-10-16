"""Synthetic subprocess regressions; no application imports, database, or network."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROFILE = Path(__file__).resolve().parents[1]
GUARD = PROFILE / "templates" / "architecture_guard.py"
POLICY = PROFILE / "templates" / "architecture-policy.json"


class ArchitectureGuardTests(unittest.TestCase):
    def run_guard(self, files=None, missing=None, policy_change=None):
        with tempfile.TemporaryDirectory(prefix="saas-python-guard-") as temporary:
            root = Path(temporary)
            source_files = {
                "src/example_saas/domain/entity.py": "from dataclasses import dataclass\n",
                "src/example_saas/application/use_case.py": "from example_saas.domain import entity\n",
            }
            source_files.update(files or {})
            for relative, source in source_files.items():
                if missing and relative.startswith(missing):
                    continue
                file = root / relative
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(source, encoding="utf-8")
            policy = json.loads(POLICY.read_text(encoding="utf-8"))
            if policy_change:
                policy_change(policy, root)
            config = root / "architecture-policy.json"
            config.write_text(json.dumps(policy), encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(GUARD), "--project-root", str(root), "--config", str(config)],
                                    capture_output=True, text=True, timeout=20, cwd=root)
        self.assertFalse(root.exists(), "Temporary fixture must be removed")
        return result

    def assert_rejected(self, files, expected, code=1):
        result = self.run_guard(files)
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        self.assertIn(expected, result.stderr)

    def test_allowed_domain_and_application_imports(self):
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("2 Python files inspected", result.stdout)

    def test_missing_source_root_fails_closed(self):
        result = self.run_guard(missing="src/")
        self.assertEqual(2, result.returncode)
        self.assertIn("required source_root", result.stderr)

    def test_missing_layer_root_fails_closed(self):
        result = self.run_guard(missing="src/example_saas/domain/")
        self.assertEqual(2, result.returncode)
        self.assertIn("required layer root", result.stderr)

    def test_empty_layer_fails_closed(self):
        def empty(policy, root):
            (root / "src/example_saas/domain/entity.py").unlink()
        result = self.run_guard(policy_change=empty)
        self.assertEqual(2, result.returncode)
        self.assertIn("no Python files", result.stderr)

    def test_domain_cannot_import_application(self):
        self.assert_rejected({"src/example_saas/domain/bad.py": "from example_saas.application import use_case\n"}, "example_saas.application")

    def test_application_cannot_import_persistence(self):
        self.assert_rejected({"src/example_saas/application/bad.py": "import sqlalchemy.orm\n"}, "sqlalchemy.orm")

    def test_application_cannot_import_transport(self):
        self.assert_rejected({"src/example_saas/application/bad.py": "from fastapi import Request\n"}, "fastapi")

    def test_absolute_internal_infrastructure_import_rejected(self):
        self.assert_rejected({"src/example_saas/application/bad.py": "from example_saas.infrastructure.persistence import Repo\n"}, "example_saas.infrastructure")

    def test_relative_import_from_nested_package_rejected(self):
        self.assert_rejected({"src/example_saas/application/nested/use_case.py": "from ...infrastructure import repo\n"}, "example_saas.infrastructure")

    def test_relative_import_in_package_init_rejected(self):
        self.assert_rejected({"src/example_saas/application/__init__.py": "from .. import infrastructure\n"}, "example_saas.infrastructure")

    def test_comments_and_strings_are_not_imports(self):
        source = '# import sqlalchemy\nexample = "from fastapi import Request"\ntext = """import sqlite3"""\n'
        result = self.run_guard({"src/example_saas/domain/example.py": source})
        self.assertEqual(0, result.returncode, result.stderr)

    def test_dynamic_literal_import_rejected(self):
        self.assert_rejected({"src/example_saas/application/bad.py": 'import importlib as il\nil.import_module("sqlalchemy")\n'}, "sqlalchemy")

    def test_dynamic_loader_alias_rejected(self):
        self.assert_rejected({"src/example_saas/application/bad.py": 'from importlib import import_module as load\nload("sqlite3")\n'}, "sqlite3")

    def test_nonliteral_dynamic_import_fails_closed(self):
        self.assert_rejected({"src/example_saas/application/bad.py": '__import__(configured_module)\n'}, "unresolved-dynamic-import")

    def test_syntax_error_fails_closed(self):
        self.assert_rejected({"src/example_saas/application/bad.py": 'def invalid(:\n'}, "cannot parse", code=2)

    def test_policy_path_escape_fails_closed(self):
        result = self.run_guard(policy_change=lambda policy, root: policy.update(source_root="../outside"))
        self.assertEqual(2, result.returncode)
        self.assertIn("must not contain", result.stderr)

    def test_incomplete_policy_fails_closed(self):
        result = self.run_guard(policy_change=lambda policy, root: policy["layers"].pop("domain"))
        self.assertEqual(2, result.returncode)
        self.assertIn("layers must configure", result.stderr)

    def test_configured_prefix_does_not_match_unrelated_package(self):
        result = self.run_guard({"src/example_saas/domain/example.py": "import sqlalchemy_helpers\n"})
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
