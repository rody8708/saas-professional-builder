[CmdletBinding()]
param(
    [ValidateSet('Test', 'Check')][string]$Mode = 'Test',
    [string]$ProjectRoot
)

$ErrorActionPreference = 'Stop'
$profileRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if ($Mode -eq 'Check' -and [string]::IsNullOrWhiteSpace($ProjectRoot)) {
    throw 'Check requires -ProjectRoot pointing to the target project with architecture-guard.json.'
}
$targetRoot = if ($Mode -eq 'Check') { [IO.Path]::GetFullPath($ProjectRoot) } else { $null }
$temporaryParent = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$temporaryRoot = Join-Path $temporaryParent ('saas-dotnet-build-' + [guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $temporaryRoot
$savedEnvironment = @{}
$environmentValues = @{
    DOTNET_CLI_HOME = (Join-Path $temporaryRoot 'cli')
    NUGET_PACKAGES = (Join-Path $temporaryRoot 'packages')
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    DOTNET_NOLOGO = '1'
    DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = '1'
    MSBUILDDISABLENODEREUSE = '1'
}
$resultCode = 2
Push-Location $profileRoot
try {
    foreach ($name in $environmentValues.Keys) {
        $savedEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
        [Environment]::SetEnvironmentVariable($name, $environmentValues[$name], 'Process')
    }
    $projectFile = if ($Mode -eq 'Test') { 'tests/ArchitectureGuard.Regression.csproj' } else { 'tools/ArchitectureGuard/ArchitectureGuard.csproj' }
    $assemblyName = if ($Mode -eq 'Test') { 'ArchitectureGuard.Regression' } else { 'ArchitectureGuard' }
    $artifacts = Join-Path $temporaryRoot 'artifacts'
    & dotnet build $projectFile --artifacts-path $artifacts --configfile tools/NuGet.Offline.Config --disable-build-servers -p:UseSharedCompilation=false -nodeReuse:false --nologo
    if ($LASTEXITCODE -ne 0) { throw "dotnet build failed with exit code $LASTEXITCODE" }
    $assembly = Join-Path $artifacts "bin/$assemblyName/debug/$assemblyName.dll"
    if (-not (Test-Path -LiteralPath $assembly -PathType Leaf)) { throw "Expected build output missing: $assembly" }
    if ($Mode -eq 'Test') { & dotnet $assembly } else { & dotnet $assembly $targetRoot }
    $resultCode = $LASTEXITCODE
}
finally {
    foreach ($name in $savedEnvironment.Keys) { [Environment]::SetEnvironmentVariable($name, $savedEnvironment[$name], 'Process') }
    Pop-Location
    $resolvedTemporary = (Resolve-Path -LiteralPath $temporaryRoot).Path
    $resolvedParent = [IO.Path]::TrimEndingDirectorySeparator([IO.Path]::GetDirectoryName($resolvedTemporary))
    if ($resolvedParent -ne [IO.Path]::TrimEndingDirectorySeparator($temporaryParent) -or
        -not [IO.Path]::GetFileName($resolvedTemporary).StartsWith('saas-dotnet-build-')) {
        throw "Refusing cleanup outside the owned temporary build directory: $resolvedTemporary"
    }
    Remove-Item -LiteralPath $resolvedTemporary -Recurse -Force
    if (Test-Path -LiteralPath $resolvedTemporary) { throw 'Temporary build cleanup failed.' }
    Write-Output 'Temporary build, restore and CLI-home directories removed and verified.'
}
exit $resultCode
