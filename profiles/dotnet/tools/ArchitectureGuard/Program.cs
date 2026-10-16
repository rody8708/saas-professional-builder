using SaasProfessionalBuilder.Architecture;

if (args.Length != 1)
{
    Console.Error.WriteLine("Usage: ArchitectureGuard <target-project-root>");
    return 2;
}

try
{
    var findings = ArchitectureScanner.Check(args[0]);
    foreach (var finding in findings)
        Console.WriteLine($"[{finding.Code}] {finding.Path}:{finding.Line} {finding.Message}");
    Console.WriteLine(findings.Count == 0
        ? "Architecture source checks passed; see PROFILE.md for their bounded scope."
        : $"Architecture source checks failed: {findings.Count} finding(s).");
    return findings.Count == 0 ? 0 : 1;
}
catch (Exception exception) when (exception is IOException or UnauthorizedAccessException or ArgumentException)
{
    Console.Error.WriteLine($"Unable to inspect source: {exception.Message}");
    return 2;
}
