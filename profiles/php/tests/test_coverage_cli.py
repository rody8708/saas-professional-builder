"""Exercise the supplied coverage checker with isolated, synthetic reports."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "templates" / "check-coverage.template.php"
PHP = os.environ.get("PHP_BINARY", "php")


class CoverageCliTest(unittest.TestCase):
    def run_checker(self, xml, threshold="80"):
        with tempfile.TemporaryDirectory(prefix="saas-coverage-test-") as directory:
            report = Path(directory) / "coverage.xml"
            if xml is not None:
                report.write_text(xml, encoding="utf-8")
            result = subprocess.run(
                [PHP, str(CHECKER), str(report), threshold],
                capture_output=True, text=True, timeout=20, check=False,
            )
        self.assertFalse(Path(directory).exists())
        return result

    @staticmethod
    def report(total, covered):
        return (
            '<?xml version="1.0"?><coverage><project>'
            f'<metrics statements="{total}" coveredstatements="{covered}"/>'
            '</project></coverage>'
        )

    def test_above_threshold_passes(self):
        result = self.run_checker(self.report(100, 81))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("81.00%", result.stdout)

    def test_exact_threshold_passes(self):
        result = self.run_checker(self.report(100, 80))
        self.assertEqual(0, result.returncode, result.stderr)

    def test_fractional_coverage_does_not_round_up_to_pass(self):
        result = self.run_checker(self.report(100000, 79999))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("below", result.stderr)

    def test_below_threshold_fails(self):
        result = self.run_checker(self.report(100, 79))
        self.assertNotEqual(0, result.returncode)

    def test_missing_report_fails(self):
        result = self.run_checker(None)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing", result.stderr)

    def test_empty_and_malformed_report_fail(self):
        for xml in ("", "<coverage>", "not XML"):
            with self.subTest(xml=xml):
                self.assertNotEqual(0, self.run_checker(xml).returncode)

    def test_missing_and_duplicate_metrics_fail(self):
        for xml in (
            '<coverage><project/></coverage>',
            '<coverage><project><metrics/><metrics/></project></coverage>',
            '<coverage><project><metrics statements="100"/></project></coverage>',
        ):
            with self.subTest(xml=xml):
                self.assertNotEqual(0, self.run_checker(xml).returncode)

    def test_zero_source_statements_fail(self):
        self.assertNotEqual(0, self.run_checker(self.report(0, 0)).returncode)

    def test_invalid_statement_counts_fail(self):
        for total, covered in ((1, 2), (-1, 0), (100, -1), ("NaN", 1), ("1.5", 1), (100, "")):
            with self.subTest(total=total, covered=covered):
                self.assertNotEqual(0, self.run_checker(self.report(total, covered)).returncode)

    def test_invalid_thresholds_fail(self):
        for threshold in ("0", "-1", "101", "NaN", "1e999", ""):
            with self.subTest(threshold=threshold):
                self.assertNotEqual(0, self.run_checker(self.report(100, 100), threshold).returncode)

    def test_doctype_rejected_without_resolving_entity(self):
        xml = '<!DOCTYPE coverage [<!ENTITY example "synthetic">]>' + self.report(100, 100).split('?>')[1]
        result = self.run_checker(xml)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("DOCTYPE", result.stderr)

    def test_nested_file_metrics_cannot_override_project_total(self):
        xml = ('<coverage><project><file><metrics statements="1" coveredstatements="1"/></file>'
               '<metrics statements="100" coveredstatements="1"/></project></coverage>')
        self.assertNotEqual(0, self.run_checker(xml).returncode)


if __name__ == "__main__":
    unittest.main(verbosity=2)
