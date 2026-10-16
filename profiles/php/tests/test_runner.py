"""Regresiones del aislamiento y de los fallos del runner, sin instalar paquetes."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("php_profile_runner", Path(__file__).resolve().parents[1] / "tools" / "run-tests.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RunnerTest(unittest.TestCase):
    def invoke(self, *, failing_stage=None, exception=None, source_environment=None):
        calls = []
        roots = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            root = kwargs["cwd"].parent
            roots.append(root)
            self.assertTrue((kwargs["cwd"] / "composer.lock").is_file())
            self.assertEqual(subprocess.DEVNULL, kwargs["stdin"])
            self.assertFalse(kwargs["check"])
            # Simula resultados de dependencias y fixtures para probar teardown.
            (root / "fixtures" / "synthetic.txt").write_text("synthetic", encoding="utf-8")
            if len(calls) == failing_stage:
                if exception is not None:
                    raise exception
                return subprocess.CompletedProcess(command, 17)
            return subprocess.CompletedProcess(command, 0)

        with tempfile.TemporaryDirectory(prefix="saas-php-runner-test-") as parent:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                status = MODULE.run_profile("/synthetic/php", ["/synthetic/php", "/synthetic/composer.phar"],
                    runner=fake_run, source_environment=source_environment or {}, temp_parent=parent)
            self.assertEqual([], list(Path(parent).iterdir()))
            for root in roots:
                self.assertFalse(root.exists())
        self.assertFalse(Path(parent).exists())
        return status, calls

    def test_success_audits_before_install_and_uses_own_autoloader(self):
        status, calls = self.invoke()
        self.assertEqual(0, status)
        self.assertEqual(8, len(calls))
        commands = [command for command, _ in calls]
        self.assertIn("audit", commands[3])
        self.assertIn("--locked", commands[3])
        self.assertIn("install", commands[4])
        self.assertIn("--no-scripts", commands[4])
        self.assertTrue(all("--no-plugins" in command for command in commands[1:6]))
        self.assertIn("--no-configuration", commands[6])
        self.assertIn(str(calls[6][1]["cwd"] / "vendor" / "autoload.php"), commands[6])

    def test_every_command_failure_stops_and_keeps_original_status(self):
        for stage in range(1, 9):
            with self.subTest(stage=stage):
                status, calls = self.invoke(failing_stage=stage)
                self.assertEqual(17, status)
                self.assertEqual(stage, len(calls))

    def test_timeout_still_cleans_dependencies_and_fixtures(self):
        status, calls = self.invoke(failing_stage=5, exception=subprocess.TimeoutExpired("synthetic", 900))
        self.assertEqual(124, status)
        self.assertEqual(5, len(calls))

    def test_spawn_failure_still_cleans_dependencies_and_fixtures(self):
        status, calls = self.invoke(failing_stage=5, exception=OSError("synthetic spawn failure"))
        self.assertEqual(1, status)
        self.assertEqual(5, len(calls))

    def test_environment_drops_external_composer_configuration_and_template_override(self):
        source = {"PATH": "synthetic-system-path", "COMPOSER_AUTH": "synthetic-auth",
                  "COMPOSER": "outside.json", "COMPOSER_HOME": "outside-home",
                  "COMPOSER_CACHE_DIR": "outside-cache", "COMPOSER_IGNORE_PLATFORM_REQS": "1",
                  "COMPOSER_NO_AUDIT": "1", "PHPUNIT_BOOTSTRAP": "outside.php",
                  "SAAS_GUARD_TEMPLATE": "outside.php", "PHP_BINARY": "outside-php"}
        status, calls = self.invoke(source_environment=source)
        self.assertEqual(0, status)
        for _, kwargs in calls:
            env = kwargs["env"]
            root = kwargs["cwd"].parent
            self.assertEqual("synthetic-system-path", env["PATH"])
            self.assertEqual("/synthetic/php", env["PHP_BINARY"])
            for forbidden in ("COMPOSER_AUTH", "COMPOSER_IGNORE_PLATFORM_REQS", "COMPOSER_NO_AUDIT", "PHPUNIT_BOOTSTRAP", "SAAS_GUARD_TEMPLATE"):
                self.assertNotIn(forbidden, env)
            for key in ("COMPOSER", "COMPOSER_HOME", "COMPOSER_CACHE_DIR", "TMP", "TEMP", "TMPDIR"):
                self.assertTrue(Path(env[key]).is_relative_to(root))
        self.assertEqual("synthetic-auth", source["COMPOSER_AUTH"])

    def test_missing_manifest_fails_and_cleans_before_spawning(self):
        with tempfile.TemporaryDirectory(prefix="saas-php-missing-manifest-") as parent:
            tools = Path(parent) / "missing"
            tools.mkdir()
            with patch.object(MODULE.subprocess, "run") as runner:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    status = MODULE.run_profile("php", ["composer"], tools_directory=tools, runner=runner, temp_parent=parent)
                runner.assert_not_called()
            self.assertEqual(1, status)
            self.assertEqual([tools], list(Path(parent).iterdir()))

    def test_phar_uses_explicit_php_without_shell(self):
        with tempfile.TemporaryDirectory(prefix="saas-composer-resolve-") as temporary:
            phar = Path(temporary) / "composer.phar"
            phar.write_text("synthetic", encoding="utf-8")
            self.assertEqual(["chosen-php", str(phar.resolve())], MODULE.composer_command(str(phar), "chosen-php"))

    def test_windows_wrapper_uses_sibling_phar_without_shell(self):
        with tempfile.TemporaryDirectory(prefix="saas-composer-resolve-") as temporary:
            wrapper = Path(temporary) / "composer.bat"
            phar = Path(temporary) / "composer.phar"
            wrapper.write_text("synthetic", encoding="utf-8")
            phar.write_text("synthetic", encoding="utf-8")
            with patch.object(MODULE, "resolve_executable", return_value=str(wrapper)):
                self.assertEqual(["chosen-php", str(phar)], MODULE.composer_command("composer", "chosen-php"))
            phar.unlink()
            with patch.object(MODULE, "resolve_executable", return_value=str(wrapper)):
                with self.assertRaisesRegex(ValueError, "--composer"):
                    MODULE.composer_command("composer", "chosen-php")

    def test_unix_php_script_without_extension_uses_explicit_php(self):
        with tempfile.TemporaryDirectory(prefix="saas-composer-resolve-") as temporary:
            executable = Path(temporary) / "composer"
            executable.write_text("#!/usr/bin/env php\n<?php echo PHP_BINARY;\n", encoding="utf-8")
            with patch.object(MODULE, "resolve_executable", return_value=str(executable)):
                self.assertEqual(["chosen-php", str(executable)], MODULE.composer_command("composer", "chosen-php"))

    def test_arbitrary_composer_shell_wrapper_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="saas-composer-resolve-") as temporary:
            executable = Path(temporary) / "composer"
            executable.write_text("#!/bin/sh\nexec php /other/composer.phar\n", encoding="utf-8")
            with patch.object(MODULE, "resolve_executable", return_value=str(executable)):
                with self.assertRaisesRegex(ValueError, "--composer"):
                    MODULE.composer_command("composer", "chosen-php")

    def test_real_command_preserves_nonzero_exit_and_cleans(self):
        def real_run(command, **kwargs):
            return MODULE.run_command([sys.executable, "-B", "-c", "raise SystemExit(19)"], **kwargs)

        with tempfile.TemporaryDirectory(prefix="saas-php-real-exit-") as parent:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                status = MODULE.run_profile(sys.executable, ["synthetic-composer"],
                    runner=real_run, temp_parent=parent, command_timeout=5)
            self.assertEqual(19, status)
            self.assertEqual([], list(Path(parent).iterdir()))

    def test_real_timeout_kills_child_before_cleanup_and_late_write(self):
        # El hijo conserva cwd=work y escribiría después del timeout. Matar
        # solo al padre deja ese proceso activo y bloquea cleanup en Windows.
        with tempfile.TemporaryDirectory(prefix="saas-php-process-tree-") as temporary:
            outer = Path(temporary)
            runner_parent = outer / "runner"
            runner_parent.mkdir()
            child_pid = outer / "child.pid"
            parent_pid = outer / "parent.pid"
            late_write = outer / "late-write.txt"
            script = outer / "synthetic_process.py"
            script.write_text(
                "import os, pathlib, subprocess, sys, time\n"
                "root = pathlib.Path(sys.argv[1])\n"
                "if len(sys.argv) > 2:\n"
                "    (root / 'child.pid').write_text(str(os.getpid()))\n"
                "    time.sleep(2)\n"
                "    (root / 'late-write.txt').write_text('synthetic')\n"
                "else:\n"
                "    (root / 'parent.pid').write_text(str(os.getpid()))\n"
                "    subprocess.Popen([sys.executable, '-B', __file__, str(root), 'child'], "
                "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
                "    time.sleep(10)\n", encoding="utf-8")

            def real_run(command, **kwargs):
                return MODULE.run_command([sys.executable, "-B", str(script), str(outer)], **kwargs)

            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    status = MODULE.run_profile(sys.executable, ["synthetic-composer"],
                        runner=real_run, temp_parent=str(runner_parent), command_timeout=1)
                self.assertEqual(124, status)
                self.assertTrue(child_pid.is_file(), "El hijo sintético debe haber arrancado antes del timeout.")
                self.assertEqual([], list(runner_parent.iterdir()), "Cleanup debe terminar antes del retorno.")
                time.sleep(2.5)
                self.assertFalse(late_write.exists(), "El hijo no debe poder escribir después del retorno.")
            finally:
                # Teardown defensivo incluso si una regresión deja un proceso
                # vivo. Solo se consideran los PID de esta fixture sintética.
                for pid_file in (parent_pid, child_pid):
                    if not pid_file.is_file():
                        continue
                    pid = int(pid_file.read_text())
                    if os.name == "nt":
                        taskkill = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe"
                        subprocess.run([str(taskkill), "/PID", str(pid), "/T", "/F"],
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, check=False, timeout=10)
                    else:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
        self.assertFalse(outer.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
