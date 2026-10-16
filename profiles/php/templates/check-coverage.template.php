<?php

declare(strict_types=1);

// Copy to tools/check-coverage.php in the destination project.
// Usage: php tools/check-coverage.php build/coverage.xml 80
// The percentage is an example policy; agree it in the destination project.

function coverageError(string $message): never
{
    fwrite(STDERR, $message . PHP_EOL);
    exit(1);
}

if ($argc !== 3 || !is_numeric($argv[2])) {
    coverageError('Usage: php check-coverage.php <clover.xml> <minimum-percent>');
}

$minimum = (float) $argv[2];
if (!is_finite($minimum) || $minimum <= 0 || $minimum > 100) {
    coverageError('The minimum percentage must be greater than 0 and at most 100.');
}
if (!class_exists(DOMDocument::class)) {
    coverageError('The PHP DOM extension is required.');
}
if (!is_file($argv[1]) || !is_readable($argv[1])) {
    coverageError('Coverage report is missing or unreadable.');
}
$xml = file_get_contents($argv[1]);
if ($xml === false || $xml === '' || stripos($xml, '<!DOCTYPE') !== false) {
    coverageError('Coverage report must be nonempty XML without a DOCTYPE.');
}

libxml_use_internal_errors(true);
$document = new DOMDocument();
$loaded = $document->loadXML($xml, LIBXML_NONET);
libxml_clear_errors();
if (!$loaded) {
    coverageError('Coverage report is malformed XML.');
}
$nodes = (new DOMXPath($document))->query('/coverage/project/metrics');
if ($nodes === false || $nodes->length !== 1) {
    coverageError('Expected exactly one project metrics element in the Clover report.');
}
$metrics = $nodes->item(0);
if (!$metrics instanceof DOMElement) {
    coverageError('Missing project metrics.');
}
$totalText = $metrics->getAttribute('statements');
$coveredText = $metrics->getAttribute('coveredstatements');
if (!preg_match('/^[0-9]+$/D', $totalText) || !preg_match('/^[0-9]+$/D', $coveredText)) {
    coverageError('Statement counts must be nonnegative integers.');
}
$total = filter_var($totalText, FILTER_VALIDATE_INT);
$covered = filter_var($coveredText, FILTER_VALIDATE_INT);
if ($total === false || $covered === false || $total <= 0 || $covered > $total) {
    coverageError('Invalid statement counts or no source statements measured.');
}
$percentage = 100.0 * $covered / $total;
printf('Statement coverage: %.2f%% (%d/%d); required: %.2f%%%s', $percentage, $covered, $total, $minimum, PHP_EOL);
if ($percentage < $minimum) {
    coverageError('Statement coverage is below the required threshold.');
}
