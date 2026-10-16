using System.Text.Json;
using System.Diagnostics;
using System.Reflection;
using SaasProfessionalBuilder.Architecture;

var scenarios = new (string Name, Action<Fixture> Arrange, string? ExpectedCode)[]
{
    ("Permitted contracts and Application-to-Domain dependency", fixture =>
        fixture.Project("Application", "<ProjectReference Include=\"../Example.Domain/Example.Domain.csproj\" />"), null),
    ("ASP.NET and EF Core permitted in external layers", fixture => fixture.Write("src/Example.Infrastructure/Adapter.cs",
        "using Microsoft.AspNetCore.Http; using Microsoft.EntityFrameworkCore; namespace Example.Infrastructure; public class Adapter {}"), null),
    ("Comments, strings, raw strings and literal text are not dependencies", fixture => fixture.Domain(""""
        namespace Example.Domain;
        // using Microsoft.EntityFrameworkCore;
        /* Example.Infrastructure.Fake */
        public class Model {
            public string Text = "System.Data.SqlClient.SqlConnection";
            public string Raw = """using Example.Persistence;""";
            public string Literal = $"Example.Infrastructure literal {42}";
        }
        """"), null),
    ("Namespace segment boundaries avoid prefix false positives", fixture =>
        fixture.Domain("using Example.InfrastructureLike; namespace Example.Domain; public class Model {}"), null),
    ("Domain import of infrastructure rejected", fixture =>
        fixture.Domain("using Example.Infrastructure; namespace Example.Domain; public class Model {}"), "DEPENDENCY"),
    ("Application persistence import rejected", fixture =>
        fixture.Application("using Example.Persistence; namespace Example.Application; public class Handler {}"), "DEPENDENCY"),
    ("EF Core dependency in Domain rejected", fixture =>
        fixture.Domain("using Microsoft.EntityFrameworkCore; namespace Example.Domain; public class Model {}"), "DEPENDENCY"),
    ("Qualified type dependency rejected", fixture =>
        fixture.Domain("namespace Example.Domain; public class Model { public global::System.Data.IDbConnection? Connection; }"), "DEPENDENCY"),
    ("Qualified expression dependency rejected", fixture =>
        fixture.Domain("namespace Example.Domain; public class Model { public void Run() { Example.Infrastructure.Store.Save(); } }"), "DEPENDENCY"),
    ("Namespace aliases cannot hide infrastructure", fixture =>
        fixture.Domain("using Alias = Example; namespace Example.Domain; public class Model { public Alias.Infrastructure.Store? Store; }"), "DEPENDENCY"),
    ("Global aliases used across source files", fixture => {
        fixture.Write("src/Example.Domain/Aliases.cs", "global using Alias = Example;");
        fixture.Domain("namespace Example.Domain; public class Model { public Alias.Infrastructure.Store? Store; }");
    }, "DEPENDENCY"),
    ("Using parent namespace cannot hide infrastructure", fixture =>
        fixture.Domain("using Example; namespace Example.Domain; public class Model { public Infrastructure.Store? Store; }"), "DEPENDENCY"),
    ("Nested namespace blocks cannot hide a sibling infrastructure dependency", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company { namespace Product { namespace Domain { public class Model { public Infrastructure.Store? Store; } } } }");
        CheckCli(fixture, 1);
    }, "DEPENDENCY"),
    ("File-scoped equivalent rejects the same sibling infrastructure dependency", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company.Product.Domain; public class Model { public Infrastructure.Store? Store; }");
    }, "DEPENDENCY"),
    ("Multi-segment nested namespace blocks compose for expression dependencies", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Platform.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company.Platform { namespace Product.Domain { public class Model { public void Save() { Infrastructure.Store.Save(); } } } }");
    }, "DEPENDENCY"),
    ("Application nested namespaces compose for persistence dependencies", fixture => {
        fixture.Rules.Layers[1].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[1].ForbiddenNamespacePrefixes, "Company.Product.Persistence"];
        fixture.SaveConfig();
        fixture.Application("namespace Company { namespace Product.UseCases { public class Handler { public Persistence.Store? Store; } } }");
    }, "DEPENDENCY"),
    ("Nested namespace blocks permit sibling contracts", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company { namespace Product { namespace Domain { public class Model { public Contracts.Record? Record; } } } }");
    }, null),
    ("Multi-segment nested namespaces preserve namespace segment boundaries", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Platform.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company.Platform { namespace Product.Domain { public class Model { public InfrastructureLike.Store? Store; } } }");
    }, null),
    ("Separate namespace blocks do not inherit unrelated enclosing names", fixture => {
        fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = [.. fixture.Rules.Layers[0].ForbiddenNamespacePrefixes, "Company.Product.Infrastructure"];
        fixture.SaveConfig();
        fixture.Domain("namespace Company.Product.Domain { public class Model {} } namespace Other { namespace Product { namespace Domain { public class Model { public Infrastructure.Store? Store; } } } }");
    }, null),
    ("Whitespace and comments inside qualified names", fixture =>
        fixture.Domain("using Example /* synthetic */ . Infrastructure; namespace Example.Domain; public class Model {}"), "DEPENDENCY"),
    ("Code inside interpolation is inspected", fixture =>
        fixture.Domain("namespace Example.Domain; public class Model { public string Text = $\"{Example.Infrastructure.Store.Name}\"; }"), "DEPENDENCY"),
    ("Direct project dependency rejected", fixture =>
        fixture.Project("Domain", "<ProjectReference Include=\"../Example.Infrastructure/Example.Infrastructure.csproj\" />"), "DEPENDENCY"),
    ("Domain-to-Application dependency rejected when configured", fixture => {
        fixture.Rules.Layers[0].ForbiddenProjectNameFragments = ["Application", "Infrastructure", "Persistence"];
        fixture.SaveConfig();
        fixture.Project("Domain", "<ProjectReference Include=\"../Example.Application/Example.Application.csproj\" />");
    }, "DEPENDENCY"),
    ("Transitive project dependency rejected", fixture => {
        fixture.Write("src/Example.Contracts/Example.Contracts.csproj", "<Project><ItemGroup><ProjectReference Include=\"../Example.Infrastructure/Example.Infrastructure.csproj\" /></ItemGroup></Project>");
        fixture.Project("Domain", "<ProjectReference Include=\"../Example.Contracts/Example.Contracts.csproj\" />");
    }, "DEPENDENCY"),
    ("Renamed project with forbidden identity rejected", fixture => {
        fixture.Write("src/Adapter/Adapter.csproj", "<Project><PropertyGroup><RootNamespace>Example.Infrastructure</RootNamespace></PropertyGroup></Project>");
        fixture.Project("Domain", "<ProjectReference Include=\"../Adapter/Adapter.csproj\" />");
    }, "DEPENDENCY"),
    ("Package dependency rejected", fixture =>
        fixture.Project("Application", "<PackageReference Include=\"Microsoft.EntityFrameworkCore.SqlServer\" Version=\"8.0.0\" />"), "DEPENDENCY"),
    ("Framework dependency rejected", fixture =>
        fixture.Project("Application", "<FrameworkReference Include=\"Microsoft.AspNetCore.App\" />"), "DEPENDENCY"),
    ("Assembly dependency rejected", fixture =>
        fixture.Project("Domain", "<Reference Include=\"Example.Infrastructure, Version=1.0.0.0\" />"), "DEPENDENCY"),
    ("Missing source directory fails closed", fixture => fixture.RemoveOwnedDirectory("src/Example.Domain"), "SOURCE"),
    ("Empty source directory fails closed", fixture => File.Delete(fixture.PathOf("src/Example.Domain/Model.cs")), "SOURCE"),
    ("Empty C# file fails closed", fixture => fixture.Domain(""), "SOURCE"),
    ("Comment-only C# file fails closed", fixture => fixture.Domain("// synthetic comment only"), "SOURCE"),
    ("Generated obj source does not make an empty layer pass", fixture => {
        File.Delete(fixture.PathOf("src/Example.Domain/Model.cs"));
        fixture.Write("src/Example.Domain/obj/Generated.cs", "namespace Example.Domain; public class Generated {}");
    }, "SOURCE"),
    ("Missing project file fails closed", fixture => File.Delete(fixture.PathOf("src/Example.Domain/Example.Domain.csproj")), "PROJECT"),
    ("Missing config fails closed", fixture => File.Delete(fixture.PathOf("architecture-guard.json")), "CONFIG"),
    ("Malformed config fails closed", fixture => fixture.Write("architecture-guard.json", "not json"), "CONFIG"),
    ("Empty rules cannot disable checking", fixture => { fixture.Rules.Layers[0].ForbiddenNamespacePrefixes = []; fixture.SaveConfig(); }, "CONFIG"),
    ("Escaping source root fails closed", fixture => { fixture.Rules.Layers[0].SourceRoot = "../outside"; fixture.SaveConfig(); }, "SOURCE"),
    ("Missing referenced project fails closed", fixture =>
        fixture.Project("Domain", "<ProjectReference Include=\"../Missing/Missing.csproj\" />"), "PROJECT"),
    ("Dynamic project reference requires evaluation", fixture =>
        fixture.Project("Domain", "<ProjectReference Include=\"$(ExternalProject)\" />"), "PROJECT"),
    ("Malformed project XML fails closed", fixture =>
        fixture.Write("src/Example.Domain/Example.Domain.csproj", "<Project>"), "PROJECT"),
    ("Project XML cannot load external entities", fixture =>
        fixture.Write("src/Example.Domain/Example.Domain.csproj", "<!DOCTYPE Project [<!ENTITY local SYSTEM 'file:///synthetic-never-read'>]><Project>&local;</Project>"), "PROJECT"),
    ("Syntax errors fail closed", fixture => fixture.Domain("public class {"), "SYNTAX"),
    ("Inactive conditional code is explicitly unresolved", fixture =>
        fixture.Domain("#if SOME_BUILD\nusing Example.Infrastructure;\n#endif\nnamespace Example.Domain; public class Model {}"), "CONDITIONAL_SOURCE"),
    ("CLI returns zero for permitted source", fixture => CheckCli(fixture, 0), null),
    ("CLI returns one for a forbidden dependency", fixture => {
        fixture.Domain("using Example.Infrastructure; namespace Example.Domain; public class Model {}");
        CheckCli(fixture, 1);
    }, "DEPENDENCY"),
    ("CLI returns one for missing configuration", fixture => {
        File.Delete(fixture.PathOf("architecture-guard.json"));
        CheckCli(fixture, 1);
    }, "CONFIG"),
    ("CLI rejects a missing target argument", fixture => CheckCli(fixture, 2, omitTarget: true), null),
};

var failures = 0;
var cleaned = 0;
foreach (var scenario in scenarios)
{
    var fixture = new Fixture();
    try
    {
        scenario.Arrange(fixture);
        var findings = ArchitectureScanner.Check(fixture.Root);
        var passed = scenario.ExpectedCode is null ? findings.Count == 0 : findings.Any(item => item.Code == scenario.ExpectedCode);
        if (!passed)
        {
            failures++;
            Console.Error.WriteLine($"FAIL {scenario.Name}: expected {scenario.ExpectedCode ?? "no findings"}; got {string.Join(" | ", findings)}");
        }
        else Console.WriteLine($"PASS {scenario.Name}");
    }
    catch (Exception exception)
    {
        failures++;
        Console.Error.WriteLine($"FAIL {scenario.Name}: {exception}");
    }
    finally
    {
        fixture.Dispose();
        if (Directory.Exists(fixture.Root)) throw new InvalidOperationException("Synthetic fixture was not removed.");
        cleaned++;
    }
}
Console.WriteLine($"{scenarios.Length} scenarios; {failures} failures; {cleaned} synthetic fixture directories removed and verified.");
return failures == 0 ? 0 : 1;

static void CheckCli(Fixture fixture, int expectedExit, bool omitTarget = false)
{
    var executing = Assembly.GetExecutingAssembly().Location;
    var start = new ProcessStartInfo("dotnet") { RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false, CreateNoWindow = true };
    foreach (var argument in new[] { "exec", "--runtimeconfig", Path.ChangeExtension(executing, ".runtimeconfig.json"),
        "--depsfile", Path.ChangeExtension(executing, ".deps.json"), typeof(ArchitectureScanner).Assembly.Location })
        start.ArgumentList.Add(argument);
    if (!omitTarget) start.ArgumentList.Add(fixture.Root);
    using var process = Process.Start(start) ?? throw new InvalidOperationException("Could not start the real guard CLI.");
    var output = process.StandardOutput.ReadToEndAsync();
    var error = process.StandardError.ReadToEndAsync();
    if (!process.WaitForExit(20_000))
    {
        process.Kill(entireProcessTree: true);
        process.WaitForExit();
        throw new InvalidOperationException("Guard CLI timeout; owned process terminated.");
    }
    if (process.ExitCode != expectedExit)
        throw new InvalidOperationException($"CLI expected {expectedExit}, got {process.ExitCode}: {output.GetAwaiter().GetResult()} {error.GetAwaiter().GetResult()}");
}

sealed class Fixture : IDisposable
{
    private readonly string tempParent = Path.GetFullPath(Path.GetTempPath());
    public string Root { get; }
    public GuardConfiguration Rules { get; }

    public Fixture()
    {
        Root = Path.Combine(tempParent, "saas-dotnet-regression-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Root);
        Rules = new GuardConfiguration { Layers = new[] { "Domain", "Application" }.Select(layer => new LayerRule {
            Name = layer,
            SourceRoot = "src/Example." + layer,
            ForbiddenNamespacePrefixes = ["Example.Infrastructure", "Example.Persistence", "Microsoft.AspNetCore", "Microsoft.EntityFrameworkCore", "System.Data", "Dapper", "Npgsql"],
            ForbiddenProjectNameFragments = ["Infrastructure", "Persistence"]
        }).ToArray() };
        SaveConfig();
        Domain("namespace Example.Domain; public interface IEntity { int Id { get; } }");
        Application("using Example.Domain; namespace Example.Application; public class Handler { public IEntity? Entity; }");
        Project("Domain", "");
        Project("Application", "");
        Write("src/Example.Infrastructure/Example.Infrastructure.csproj", "<Project />");
    }

    public string PathOf(string relative) => Path.Combine(Root, relative.Replace('/', Path.DirectorySeparatorChar));
    public void Write(string relative, string source)
    {
        var path = PathOf(relative);
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, source);
    }
    public void Domain(string source) => Write("src/Example.Domain/Model.cs", source);
    public void Application(string source) => Write("src/Example.Application/Handler.cs", source);
    public void Project(string layer, string items) => Write($"src/Example.{layer}/Example.{layer}.csproj", $"<Project><ItemGroup>{items}</ItemGroup></Project>");
    public void SaveConfig() => Write("architecture-guard.json", JsonSerializer.Serialize(Rules));
    public void RemoveOwnedDirectory(string relative)
    {
        var path = Path.GetFullPath(PathOf(relative));
        if (!path.StartsWith(Root + Path.DirectorySeparatorChar, StringComparison.Ordinal))
            throw new InvalidOperationException("Refusing removal outside owned fixture.");
        Directory.Delete(path, recursive: true);
    }
    public void Dispose()
    {
        var full = Path.GetFullPath(Root);
        if (Path.TrimEndingDirectorySeparator(Path.GetDirectoryName(full)!) != Path.TrimEndingDirectorySeparator(tempParent) ||
            !Path.GetFileName(full).StartsWith("saas-dotnet-regression-", StringComparison.Ordinal))
            throw new InvalidOperationException("Refusing cleanup outside owned temporary directory.");
        Directory.Delete(full, recursive: true);
    }
}
