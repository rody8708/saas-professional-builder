<?php

declare(strict_types=1);

namespace Acme\Tests\Unit\Guardrails;

use PHPUnit\Framework\TestCase;
use RecursiveCallbackFilterIterator;
use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;
use SplFileInfo;

/**
 * Copy into your PHPUnit test tree and adapt the namespace and paths below.
 * The nearest ancestor composer.json defines the project root. app is required;
 * modules and bin are optional. No deployment configuration is read.
 *
 * These are bounded source checks, not a PHP type/dependency analyzer. SQL checks
 * recognize literal ->prepare/exec/query calls (including ?->); dynamic dispatch
 * and concrete Infrastructure dependencies require review/static analysis.
 * Service-locator names are checked literally; aliases/dynamic names need review.
 * Provider HTTP detection is a literal-host heuristic; configure its hosts.
 *
 * Start with empty allowlists. Stale/duplicate entries fail. Growth requires
 * explicit review of the diff against main; this file cannot enforce history.
 */
final class ArchitectureBoundaryGuardTest extends TestCase
{
    private const OPTIONAL_ROOTS = ['modules', 'bin'];
    private const EXCLUDED_DIRECTORIES = ['vendor', 'node_modules', '.git'];
    private const PROVIDER_HOSTS = ['api.provider.com', 'connect.provider.com'];
    private const PAYMENTS_ADAPTER_PREFIX = 'app/Infrastructure/Payments/';

    private const GATEWAY_CURL_ALLOWLIST = [];
    private const RAW_SQL_IN_SERVICES_ALLOWLIST = [];
    private const LONG_CONTROLLER_ALLOWLIST = [];
    private const MAX_CONTROLLER_METHOD_LINES = 30;

    public function testProviderHttpOnlyInsidePaymentsAdapter(): void
    {
        $violations = [];
        foreach ($this->phpFiles(['app', 'modules']) as $rel => $src) {
            if (str_starts_with($rel, self::PAYMENTS_ADAPTER_PREFIX)) {
                continue;
            }
            // Bounded heuristic: curl_init and a literal configured host in the
            // same file. It cannot resolve variables or HTTP client types.
            $tokens = $this->significantTokens($src);
            $hasCurl = false;
            $hasHost = false;
            foreach ($tokens as $index => $token) {
                if (is_array($token) && in_array($token[0], [T_STRING, T_NAME_FULLY_QUALIFIED], true)
                    && strtolower(ltrim($token[1], '\\')) === 'curl_init' && ($tokens[$index + 1] ?? null) === '(') {
                    $hasCurl = true;
                }
                if (is_array($token) && $token[0] === T_CONSTANT_ENCAPSED_STRING) {
                    foreach (self::PROVIDER_HOSTS as $host) {
                        $hasHost = $hasHost || str_contains($token[1], $host);
                    }
                }
            }
            if ($hasCurl && $hasHost) {
                $violations[] = $rel;
            }
        }
        $this->assertAllowed($violations, self::GATEWAY_CURL_ALLOWLIST, 'Provider HTTP must go through the gateway adapter.');
    }

    public function testApplicationServicesDoNotUseRawSql(): void
    {
        $violations = [];
        foreach ($this->phpFiles(['app/Application', 'modules']) as $rel => $src) {
            // Standard layouts: app/Application/** and modules/<slug>/Application/**.
            if (preg_match('~^(?:app/Application/|modules/[^/]+/Application/)~', $rel) !== 1) {
                continue;
            }
            $tokens = $this->significantTokens($src);
            foreach ($tokens as $index => $token) {
                $method = $tokens[$index + 1] ?? null;
                if (is_array($token) && in_array($token[0], [T_OBJECT_OPERATOR, T_NULLSAFE_OBJECT_OPERATOR], true)
                    && is_array($method) && $method[0] === T_STRING
                    && in_array(strtolower($method[1]), ['prepare', 'exec', 'query'], true)
                    && ($tokens[$index + 2] ?? null) === '(') {
                    $violations[] = $rel;
                    break;
                }
            }
        }
        $this->assertAllowed($violations, self::RAW_SQL_IN_SERVICES_ALLOWLIST, 'Use Domain repository interfaces instead of direct SQL in Application.');
    }

    public function testModulesDoNotUseServiceLocator(): void
    {
        $violations = [];
        foreach ($this->phpFiles(['modules']) as $rel => $src) {
            $tokens = $this->significantTokens($src);
            foreach ($tokens as $index => $token) {
                if (!is_array($token) || !in_array($token[0], [T_STRING, T_NAME_QUALIFIED, T_NAME_FULLY_QUALIFIED, T_NAME_RELATIVE], true)) {
                    continue;
                }
                $nameParts = explode('\\', $token[1]);
                $operator = $tokens[$index + 1] ?? null;
                $method = $tokens[$index + 2] ?? null;
                if (strtolower($nameParts[count($nameParts) - 1]) === 'moduleregistry'
                    && is_array($operator) && $operator[0] === T_DOUBLE_COLON
                    && is_array($method) && $method[0] === T_STRING
                    && in_array(strtolower($method[1]), ['getplatformservice', 'bindservice'], true)
                    && ($tokens[$index + 3] ?? null) === '(') {
                    $violations[] = $rel;
                    break;
                }
            }
        }
        self::assertSame([], $violations, 'Modules receive dependencies through PlatformBridge.');
    }

    public function testControllerMethodsStayShort(): void
    {
        $violations = [];
        foreach ($this->phpFiles(['app/Presentation', 'modules']) as $rel => $src) {
            if (preg_match('~^(?:app/Presentation/Controllers/|modules/[^/]+/(?:Presentation/)?Controllers/)~', $rel) !== 1) {
                continue;
            }
            if ($this->longestMethodLines($src) > self::MAX_CONTROLLER_METHOD_LINES) {
                $violations[] = $rel;
            }
        }
        $this->assertAllowed($violations, self::LONG_CONTROLLER_ALLOWLIST, 'Move orchestration into a *UseCase.');
    }

    public function testEveryPhpFileDeclaresStrictTypes(): void
    {
        $missing = [];
        foreach ($this->phpFiles(['app', 'modules', 'bin']) as $rel => $src) {
            if (!$this->hasStrictTypesDeclaration($src)) {
                $missing[] = $rel;
            }
        }
        self::assertSame([], $missing);
    }

    private function hasStrictTypesDeclaration(string $source): bool
    {
        $tokens = $this->significantTokens($source);
        foreach ($tokens as $index => $token) {
            $directive = $tokens[$index + 2] ?? null;
            $value = $tokens[$index + 4] ?? null;
            if (is_array($token) && $token[0] === T_DECLARE
                && ($tokens[$index + 1] ?? null) === '('
                && is_array($directive) && $directive[0] === T_STRING && $directive[1] === 'strict_types'
                && ($tokens[$index + 3] ?? null) === '='
                && is_array($value) && $value[0] === T_LNUMBER && $value[1] === '1'
                && ($tokens[$index + 5] ?? null) === ')'
                && ($tokens[$index + 6] ?? null) === ';') {
                return true;
            }
        }
        return false;
    }

    private function projectRoot(): string
    {
        $directory = __DIR__;
        while (true) {
            if (is_file($directory . '/composer.json')) {
                self::assertDirectoryExists($directory . '/app', 'The nearest composer.json must belong to the application root.');
                return $directory;
            }
            $parent = dirname($directory);
            self::assertNotSame($directory, $parent, 'Cannot locate composer.json above the guard; configure its placement.');
            $directory = $parent;
        }
    }

    /** @param list<string> $roots @return array<string,string> relative path => source */
    private function phpFiles(array $roots): array
    {
        $base = $this->projectRoot();
        $out = [];
        foreach ($roots as $root) {
            $dir = $base . '/' . $root;
            $optional = in_array($root, self::OPTIONAL_ROOTS, true);
            if ($optional && !file_exists($dir)) {
                continue;
            }
            self::assertDirectoryExists($dir, 'Missing configured source root: ' . $root);
            self::assertFalse(is_link($dir), 'Source roots must not be symlinks: ' . $root);
            $iterator = new RecursiveIteratorIterator(new RecursiveCallbackFilterIterator(
                new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
                static fn (SplFileInfo $file): bool => !$file->isLink()
                    && (!$file->isDir() || !in_array($file->getFilename(), self::EXCLUDED_DIRECTORIES, true)),
            ));
            $count = 0;
            foreach ($iterator as $file) {
                if ($file->isFile() && strtolower($file->getExtension()) === 'php') {
                    $relative = str_replace('\\', '/', substr($file->getPathname(), strlen($base) + 1));
                    $source = file_get_contents($file->getPathname());
                    self::assertNotFalse($source, 'Cannot read source file: ' . $relative);
                    $out[$relative] = $source;
                    $count++;
                }
            }
            if (!$optional) {
                self::assertGreaterThan(0, $count, 'No PHP files inspected in required source root: ' . $root);
            }
        }
        ksort($out);
        return $out;
    }

    /** @param list<string> $violations @param list<string> $allowlist */
    private function assertAllowed(array $violations, array $allowlist, string $message): void
    {
        self::assertSame(array_values(array_unique($allowlist)), $allowlist, 'Remove duplicate allowlist entries.');
        self::assertSame([], array_values(array_diff($allowlist, $violations)), 'Remove stale allowlist entries.');
        self::assertSame([], array_values(array_diff($violations, $allowlist)), $message);
    }

    /** @return list<array{int,string,int}|string> */
    private function significantTokens(string $source): array
    {
        return array_values(array_filter(token_get_all($source, TOKEN_PARSE), static fn (array|string $token): bool =>
            !is_array($token) || !in_array($token[0], [T_WHITESPACE, T_COMMENT, T_DOC_COMMENT], true)));
    }

    private function longestMethodLines(string $source): int
    {
        $tokens = token_get_all($source, TOKEN_PARSE);
        $line = 1;
        $maximum = 0;
        $awaitingBody = false;
        $depth = 0;
        $start = 0;
        foreach ($tokens as $token) {
            $id = is_array($token) ? $token[0] : null;
            $text = is_array($token) ? $token[1] : $token;
            if ($depth === 0 && $id === T_FUNCTION) {
                $awaitingBody = true;
            } elseif ($awaitingBody && $token === ';') {
                $awaitingBody = false; // Abstract/interface method.
            } elseif ($awaitingBody && $token === '{') {
                $awaitingBody = false;
                $depth = 1;
                $start = $line;
            } elseif ($depth > 0) {
                // Interpolation opens a brace as a token and closes it as a
                // literal character; balancing both keeps strings/heredocs safe.
                if ($token === '{' || $id === T_CURLY_OPEN || $id === T_DOLLAR_OPEN_CURLY_BRACES) {
                    $depth++;
                } elseif ($token === '}' && --$depth === 0) {
                    $maximum = max($maximum, $line - $start);
                }
            }
            $line += substr_count($text, "\n");
        }
        return $maximum;
    }
}
