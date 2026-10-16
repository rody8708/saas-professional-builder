<?php

declare(strict_types=1);

use PHPUnit\Framework\AssertionFailedError;
use PHPUnit\Framework\ExpectationFailedException;
use PHPUnit\Framework\TestCase;

/**
 * Run with --no-configuration and a PHPUnit vendor/autoload.php only.
 * SAAS_GUARD_TEMPLATE may select an older template for before/after evidence.
 * Fixtures are synthetic and never read a project bootstrap or environment file.
 */
final class ArchitectureTemplateRegressionTest extends TestCase
{
    private static int $sequence = 0;

    public function testRootDiscoveryAtCommonAndDeeperLocations(): void
    {
        foreach (['tests/Unit/Guardrails', 'tests/Guardrails', 'tests/Unit/Guardrails/Nested'] as $location) {
            $this->withFixture([], function (TestCase $guard, string $root): void {
                $method = new ReflectionMethod($guard, 'phpFiles');
                $files = $method->invoke($guard, ['app']);
                self::assertArrayHasKey('app/Application/Fixture.php', $files, $root);
                $guard->testEveryPhpFileDeclaresStrictTypes();
            }, $location);
        }
    }

    public function testMissingRequiredSourceRootFailsClosed(): void
    {
        $this->withFixture([], function (TestCase $guard, string $root): void {
            $this->removeOwnedTree($root . '/app/Application', $root);
            $this->assertGuardFails(fn () => $guard->testApplicationServicesDoNotUseRawSql(), 'source root');
        });
    }

    public function testEmptyRequiredSourceRootFailsClosed(): void
    {
        $this->withFixture([], function (TestCase $guard, string $root): void {
            unlink($root . '/app/Application/Fixture.php');
            $this->assertGuardFails(fn () => $guard->testApplicationServicesDoNotUseRawSql(), 'No PHP files');
        });
    }

    public function testMissingRootMarkerFailsClosed(): void
    {
        $this->withFixture([], function (TestCase $guard, string $root): void {
            unlink($root . '/composer.json');
            $this->assertGuardFails(fn () => $guard->testEveryPhpFileDeclaresStrictTypes(), 'composer.json');
        });
    }

    public function testSqlInApplicationUseCaseIsDetected(): void
    {
        $this->assertSqlRejectedAt('app/Application/UseCases/Bad.php');
    }

    public function testSqlInModuleUseCaseIsDetected(): void
    {
        $this->assertSqlRejectedAt('modules/example/Application/UseCases/Bad.php');
    }

    public function testSqlInModuleServiceIsDetected(): void
    {
        $this->assertSqlRejectedAt('modules/example/Application/Services/Bad.php');
    }

    private function assertSqlRejectedAt(string $path): void
    {
        $this->withFixture([$path => '<?php declare(strict_types=1); $pdo?->query("SELECT 1");'], function (TestCase $guard) use ($path): void {
            $this->assertGuardFails(fn () => $guard->testApplicationServicesDoNotUseRawSql(), $path);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testSqlMentionsInCommentsAndStringsDoNotFail(): void
    {
        $source = <<<'PHP'
<?php declare(strict_types=1);
// $pdo->prepare('SELECT 1');
$example = '$pdo->query("SELECT 1")';
$answer = 42;
PHP;
        $this->withFixture(['app/Application/Services/Good.php' => $source], function (TestCase $guard): void {
            $guard->testApplicationServicesDoNotUseRawSql();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testLongControllerWithQuotedClosingBraceIsDetected(): void
    {
        $source = $this->controller('$label = "}";' . "\n" . str_repeat('$value = 1;' . "\n", 40));
        $this->withFixture(['app/Presentation/Controllers/LongController.php' => $source], function (TestCase $guard): void {
            $this->assertGuardFails(fn () => $guard->testControllerMethodsStayShort(), 'LongController.php');
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testLongControllerWithCommentOpeningBraceIsDetected(): void
    {
        $source = $this->controller('/* { */' . "\n" . str_repeat('$value = 1;' . "\n", 40));
        $this->withFixture(['modules/example/Controllers/LongController.php' => $source], function (TestCase $guard): void {
            $this->assertGuardFails(fn () => $guard->testControllerMethodsStayShort(), 'LongController.php');
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testShortControllerWithHeredocInterpolationAndBracesPasses(): void
    {
        $body = <<<'PHP'
$literal = '}';
/* { } { */
$name = 'synthetic';
$text = "hello {$name} } {";
$heredoc = <<<TEXT
{$name} } {
TEXT;
if ($name !== '') { $result = 1; }
PHP;
        $this->withFixture(['app/Presentation/Controllers/TextController.php' => $this->controller($body)], function (TestCase $guard): void {
            $guard->testControllerMethodsStayShort();
            self::assertTrue(true);
        });
    }

    public function testLongControllerWithHeredocInterpolationIsDetected(): void
    {
        $body = <<<'PHP'
$name = 'synthetic';
$text = <<<TEXT
{$name} } {
TEXT;
PHP;
        $this->withFixture(['app/Presentation/Controllers/LongController.php' => $this->controller($body . "\n" . str_repeat('$value = 1;' . "\n", 40))], function (TestCase $guard): void {
            $this->assertGuardFails(fn () => $guard->testControllerMethodsStayShort(), 'LongController.php');
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testVendorInsideModulesIsNotApplicationSource(): void
    {
        $this->withFixture(['modules/example/vendor/package/ThirdParty.php' => '<?php $pdo->query("SELECT 1");'], function (TestCase $guard): void {
            $guard->testEveryPhpFileDeclaresStrictTypes();
            $guard->testApplicationServicesDoNotUseRawSql();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testStaleAllowlistEntryFails(): void
    {
        $this->withFixture([], function (TestCase $guard): void {
            $this->assertGuardFails(fn () => $guard->testApplicationServicesDoNotUseRawSql(), 'stale');
        }, 'tests/Unit/Guardrails/Nested', ['RAW_SQL_IN_SERVICES_ALLOWLIST' => ['app/Application/Removed.php']]);
    }

    public function testExistingViolationInAllowlistPasses(): void
    {
        $path = 'app/Application/Services/Legacy.php';
        $this->withFixture([$path => '<?php declare(strict_types=1); $pdo->query("SELECT 1");'], function (TestCase $guard): void {
            $guard->testApplicationServicesDoNotUseRawSql();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested', ['RAW_SQL_IN_SERVICES_ALLOWLIST' => [$path]]);
    }

    public function testDuplicateAllowlistEntryFails(): void
    {
        $path = 'app/Application/Services/Legacy.php';
        $this->withFixture([$path => '<?php declare(strict_types=1); $pdo->query("SELECT 1");'], function (TestCase $guard): void {
            $this->assertGuardFails(fn () => $guard->testApplicationServicesDoNotUseRawSql(), 'duplicate');
        }, 'tests/Unit/Guardrails/Nested', ['RAW_SQL_IN_SERVICES_ALLOWLIST' => [$path, $path]]);
    }

    public function testConfiguredProviderHostOutsideAdapterFails(): void
    {
        $path = 'app/Application/UseCases/Provider.php';
        $this->withFixture([$path => '<?php declare(strict_types=1); \\curl_init("https://api.provider.com/v1/synthetic");'], function (TestCase $guard) use ($path): void {
            $this->assertGuardFails(fn () => $guard->testProviderHttpOnlyInsidePaymentsAdapter(), $path);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testProviderInsideAdapterAndCommentsPass(): void
    {
        $this->withFixture([
            'app/Infrastructure/Payments/Adapter.php' => '<?php declare(strict_types=1); curl_init("https://api.provider.com/v1/synthetic");',
            'app/Application/UseCases/Example.php' => '<?php declare(strict_types=1); /* curl_init("https://api.provider.com"); */',
        ], function (TestCase $guard): void {
            $guard->testProviderHttpOnlyInsidePaymentsAdapter();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testControllerThresholdBoundary(): void
    {
        foreach ([29 => false, 30 => true] as $bodyLines => $mustFail) {
            $body = implode("\n", array_fill(0, $bodyLines, '$value = 1;'));
            $this->withFixture(['app/Presentation/Controllers/Boundary.php' => $this->controller($body)], function (TestCase $guard) use ($mustFail): void {
                if ($mustFail) {
                    $this->assertGuardFails(fn () => $guard->testControllerMethodsStayShort(), 'Boundary.php');
                } else {
                    $guard->testControllerMethodsStayShort();
                    self::assertTrue(true);
                }
            }, 'tests/Unit/Guardrails/Nested');
        }
    }

    public function testStrictTypesMentionInCommentDoesNotCountAsDeclaration(): void
    {
        $path = 'app/Application/FakeStrict.php';
        $this->withFixture([$path => '<?php /* declare(strict_types=1); */ $value = 1;'], function (TestCase $guard) use ($path): void {
            $this->assertGuardFails(fn () => $guard->testEveryPhpFileDeclaresStrictTypes(), $path);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testSpacedStrictDeclarationAfterLongHeaderPasses(): void
    {
        $source = '<?php /* ' . str_repeat('Synthetic license header. ', 25) . ' */ declare ( strict_types = 1 ) ;';
        $this->withFixture(['app/Application/SpacedStrict.php' => $source], function (TestCase $guard): void {
            $guard->testEveryPhpFileDeclaresStrictTypes();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testServiceLocatorWithSpacesAndCaseVariationIsDetected(): void
    {
        $path = 'modules/example/Application/Services/Locator.php';
        $source = '<?php declare(strict_types=1); ModuleRegistry /* synthetic */ :: bInDSeRvIcE ("synthetic");';
        $this->withFixture([$path => $source], function (TestCase $guard) use ($path): void {
            $this->assertGuardFails(fn () => $guard->testModulesDoNotUseServiceLocator(), $path);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testFullyQualifiedServiceLocatorIsDetected(): void
    {
        $path = 'modules/example/Application/Services/Locator.php';
        $source = '<?php declare(strict_types=1); \\Acme\\Core\\ModuleRegistry :: gEtPlAtFoRmSeRvIcE ("synthetic");';
        $this->withFixture([$path => $source], function (TestCase $guard) use ($path): void {
            $this->assertGuardFails(fn () => $guard->testModulesDoNotUseServiceLocator(), $path);
        }, 'tests/Unit/Guardrails/Nested');
    }

    public function testServiceLocatorMentionsInCommentsAndStringsPass(): void
    {
        $source = <<<'PHP'
<?php declare(strict_types=1);
/* ModuleRegistry::getPlatformService('synthetic'); */
$example = 'ModuleRegistry::bindService("synthetic")';
PHP;
        $this->withFixture(['modules/example/Application/Services/Example.php' => $source], function (TestCase $guard): void {
            $guard->testModulesDoNotUseServiceLocator();
            self::assertTrue(true);
        }, 'tests/Unit/Guardrails/Nested');
    }

    private function controller(string $body): string
    {
        return "<?php\ndeclare(strict_types=1);\nclass SyntheticController {\npublic function handle(): void {\n" . $body . "\n}\n}\n";
    }

    private function assertGuardFails(callable $action, string $message): void
    {
        $failure = null;
        try {
            $action();
        } catch (AssertionFailedError $exception) {
            $failure = $exception;
        }
        self::assertNotNull($failure, 'The guard must reject this fixture.');
        $diff = $failure instanceof ExpectationFailedException ? ($failure->getComparisonFailure()?->getDiff() ?? '') : '';
        self::assertStringContainsString($message, $failure->getMessage() . $diff);
    }

    /** @param array<string,string> $files @param array<string,list<string>> $allowlists */
    private function withFixture(array $files, callable $check, string $location = 'tests/Unit/Guardrails', array $allowlists = []): void
    {
        $root = sys_get_temp_dir() . '/saas-guard-regression-' . bin2hex(random_bytes(8));
        mkdir($root, 0700, true);
        try {
            $files += [
                'composer.json' => '{"name":"synthetic/guard-fixture"}',
                'app/Application/Fixture.php' => '<?php declare(strict_types=1);',
                'app/Presentation/Controllers/Fixture.php' => $this->controller('$value = 1;'),
            ];
            foreach ($files as $path => $contents) {
                if (!is_dir(dirname($root . '/' . $path))) {
                    mkdir(dirname($root . '/' . $path), 0700, true);
                }
                file_put_contents($root . '/' . $path, $contents);
            }
            $templatePath = getenv('SAAS_GUARD_TEMPLATE') ?: dirname(__DIR__) . '/templates/ArchitectureBoundaryGuardTest.template.php';
            $source = file_get_contents($templatePath);
            self::assertNotFalse($source);
            $namespace = 'SyntheticGuardFixture' . ++self::$sequence;
            $source = preg_replace('/namespace\s+[^;]+;/', 'namespace ' . $namespace . ';', $source, 1);
            foreach ($allowlists as $name => $entries) {
                $source = str_replace('private const ' . $name . ' = [];', 'private const ' . $name . ' = ' . var_export($entries, true) . ';', $source);
            }
            $guardPath = $root . '/' . $location . '/ArchitectureBoundaryGuardTest.php';
            mkdir(dirname($guardPath), 0700, true);
            file_put_contents($guardPath, $source);
            require $guardPath;
            $class = $namespace . '\\ArchitectureBoundaryGuardTest';
            $check(new $class('testEveryPhpFileDeclaresStrictTypes'), $root);
        } finally {
            $this->removeOwnedTree($root, $root);
            self::assertDirectoryDoesNotExist($root, 'Synthetic fixture cleanup must complete.');
        }
    }

    private function removeOwnedTree(string $path, string $ownedRoot): void
    {
        $normal = str_replace('\\', '/', $path);
        $owned = str_replace('\\', '/', $ownedRoot);
        if ($normal !== $owned && !str_starts_with($normal, $owned . '/')) {
            throw new RuntimeException('Cleanup escaped its owned fixture root.');
        }
        if (is_link($path) || is_file($path)) {
            unlink($path);
            return;
        }
        if (!is_dir($path)) {
            return;
        }
        foreach (new DirectoryIterator($path) as $entry) {
            if (!$entry->isDot()) {
                $this->removeOwnedTree($entry->getPathname(), $ownedRoot);
            }
        }
        rmdir($path);
    }
}
