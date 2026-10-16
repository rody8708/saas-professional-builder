"""Synthetic regression tests for catalog trust boundaries; no profile commands run."""
import importlib.util
import json
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

sys.dont_write_bytecode = True
MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_package.py"
SPEC = importlib.util.spec_from_file_location("package_validator", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="synthetic-saas-catalog-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for folder in ("core", "prompts", "templates", "profiles/alpha", "profiles/beta", "docs"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        for name in VALIDATOR.REQUIRED_FILES:
            if not name.endswith(".json"):
                (self.root / name).write_text("# Synthetic documentation\n", encoding="utf-8")
        self.registry = {
            "schema_version": 1,
            "selection_policy": "explicit-or-detected-never-default",
            "required_project_gates": sorted(VALIDATOR.GATES),
            "profiles": [{"id": key, "path": f"{key}/profile.json"} for key in ("alpha", "beta")],
        }
        self.profiles = {}
        for key in ("alpha", "beta"):
            self.profiles[key] = {
                "id": key, "name": f"Synthetic {key}", "languages": ["Synthetic"],
                "status": "controls-validated", "guide": "PROFILE.md",
                "templates": ["control.py"], "tests": ["test_control.py"],
                "implemented_controls": ["synthetic-control"],
                "project_gates": sorted(VALIDATOR.GATES),
                "validation": {"environment": "isolated fixture", "command": "documented only",
                               "result": "fixture evidence", "limitations": ["not an application"]},
            }
            for name in ("PROFILE.md", "control.py", "test_control.py"):
                (self.root / "profiles" / key / name).write_text("# Synthetic fixture\n", encoding="utf-8")

    def validate(self):
        (self.root / "profiles/registry.json").write_text(json.dumps(self.registry), encoding="utf-8")
        for key, profile in self.profiles.items():
            (self.root / "profiles" / key / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
        return VALIDATOR.validate(self.root)

    def test_multiple_profiles_preserve_all_gates(self):
        self.assertEqual([], self.validate())

    def test_registry_cannot_silently_default_to_a_language(self):
        self.registry["default_profile"] = "alpha"
        self.assertTrue(any("default stack" in e for e in self.validate()))

    def test_selection_must_not_be_implicit(self):
        self.registry["selection_policy"] = "use-alpha"
        self.assertTrue(any("selection" in e for e in self.validate()))

    def test_duplicate_profile_rejected(self):
        self.registry["profiles"].append(self.registry["profiles"][0].copy())
        self.assertTrue(any("duplicate profile" in e for e in self.validate()))

    def test_profile_cannot_drop_tenant_isolation(self):
        self.profiles["beta"]["project_gates"].remove("tenant-isolation")
        self.assertTrue(any("seven project gates" in e for e in self.validate()))

    def test_registry_cannot_weaken_required_gates(self):
        self.registry["required_project_gates"].remove("retry-safety")
        self.assertTrue(any("seven required project gates" in e for e in self.validate()))

    def test_validated_status_needs_tests_and_named_controls(self):
        self.profiles["alpha"]["tests"] = []
        self.profiles["alpha"]["implemented_controls"] = []
        self.assertTrue(any("executable tests" in e for e in self.validate()))

    def test_validation_evidence_cannot_be_blank(self):
        self.profiles["beta"]["validation"]["result"] = "  "
        self.assertTrue(any("validation.result" in e for e in self.validate()))

    def test_guidance_only_can_have_no_controls(self):
        profile = self.profiles["alpha"]
        profile.update(status="guidance-only", tests=[], implemented_controls=[])
        profile["validation"]["result"] = "No executable controls supplied"
        self.assertEqual([], self.validate())

    def test_missing_referenced_test_fails(self):
        (self.root / "profiles/alpha/test_control.py").unlink()
        self.assertTrue(any("referenced file" in e for e in self.validate()))

    def test_manifest_paths_cannot_escape_their_profile(self):
        for bad in ("../beta/PROFILE.md", "/etc/passwd", "C:/Windows/system.ini", "C:relative", "..\\beta\\PROFILE.md"):
            with self.subTest(path=bad):
                self.profiles["alpha"]["guide"] = bad
                self.assertTrue(any("unsafe path" in e for e in self.validate()))

    def test_manifest_command_is_never_executed(self):
        marker = self.root / "unwanted.txt"
        self.profiles["alpha"]["validation"]["command"] = (
            f"python -c \"open({str(marker)!r}, 'w').write('unexpected')\""
        )
        self.assertEqual([], self.validate())
        self.assertFalse(marker.exists())

    def test_common_requirements_cannot_introduce_stack_commands(self):
        (self.root / "core/architecture.md").write_text("Run composer install for every project.", encoding="utf-8")
        self.assertTrue(any("stack-specific" in e for e in self.validate()))

    def test_stack_commands_allowed_in_profile(self):
        (self.root / "profiles/alpha/PROFILE.md").write_text("Run composer install here.", encoding="utf-8")
        self.assertEqual([], self.validate())

    def test_broken_local_link_fails_but_link_inside_example_is_not_resolved(self):
        path = self.root / "README.md"
        path.write_text("```markdown\n[example](not-real.md)\n```\n", encoding="utf-8")
        self.assertEqual([], self.validate())
        path.write_text("[missing](not-real.md)\n", encoding="utf-8")
        self.assertTrue(any("Markdown link" in e for e in self.validate()))

    def test_unclosed_fence_rejected(self):
        (self.root / "README.md").write_text("```text\nmissing closing fence\n", encoding="utf-8")
        self.assertTrue(any("code fence" in e for e in self.validate()))

    def test_operational_files_and_generated_directories_rejected(self):
        (self.root / ".env").write_text("SYNTHETIC=1\n", encoding="utf-8")
        (self.root / "profiles/alpha/obj").mkdir()
        errors = self.validate()
        self.assertTrue(any("artifact" in e for e in errors))
        self.assertTrue(any("operational directory" in e for e in errors))

    def test_malformed_profile_field_does_not_crash_validator(self):
        self.profiles["alpha"]["templates"] = [{"bad": "shape"}]
        self.profiles["beta"]["project_gates"] = "wrong-type"
        self.assertGreaterEqual(len(self.validate()), 2)

    def test_status_with_wrong_type_is_a_validation_error(self):
        for value in ({"bad": "shape"}, ["controls-validated"], None, 1):
            with self.subTest(value=value):
                self.profiles["alpha"]["status"] = value
                self.assertTrue(any("validation status" in e for e in self.validate()))

    def test_recognized_secret_is_checked_in_every_text_extension(self):
        for name in ("capture.txt", ".env.example", "custom.unknown"):
            with self.subTest(name=name):
                path = self.root / name
                path.write_text("ghp_" + "A" * 36, encoding="utf-8")
                try:
                    self.assertTrue(any("possible credential" in e for e in self.validate()))
                finally:
                    path.unlink()

    def test_malformed_url_is_reported_and_other_findings_are_preserved(self):
        (self.root / "README.md").write_text("[broken](http://[)\n[missing](absent.md)\n", encoding="utf-8")
        errors = self.validate()
        self.assertTrue(any("malformed Markdown link" in e for e in errors))
        self.assertTrue(any("local Markdown link" in e for e in errors))

    def test_windows_reparse_attribute_is_recognized_without_following(self):
        with patch.object(Path, "lstat", return_value=SimpleNamespace(st_mode=0, st_file_attributes=0x400)):
            self.assertTrue(VALIDATOR.is_linklike(self.root / "junction"))

    def test_linklike_directory_is_rejected_before_traversal(self):
        # The validator resolves the supplied root, including Windows 8.3
        # aliases. The mock must identify the same canonical fixture target.
        canonical_root = self.root.resolve()
        linked = canonical_root / "linklike-fixture"
        linked.mkdir()
        alias_hop = canonical_root / "normalization-hop"
        alias_hop.mkdir()
        aliased_root = alias_hop / ".."
        self.assertNotEqual(aliased_root, canonical_root)
        self.assertEqual(canonical_root, aliased_root.resolve())
        original_iterdir = Path.iterdir
        original_detector = VALIDATOR.is_linklike

        def guarded_iterdir(path):
            if path == linked:
                raise AssertionError("must never enumerate the linked target")
            return original_iterdir(path)

        for supplied_root in (self.root, aliased_root):
            with self.subTest(root=supplied_root):
                with patch.object(self, "root", supplied_root):
                    with patch.object(VALIDATOR, "is_linklike", side_effect=lambda p: p == linked or original_detector(p)) as detector:
                        with patch.object(Path, "iterdir", guarded_iterdir):
                            errors = self.validate()
                        detector.assert_any_call(linked)
                        self.assertTrue(any("reparse point" in e for e in errors))

if __name__ == "__main__":
    unittest.main(verbosity=2)
