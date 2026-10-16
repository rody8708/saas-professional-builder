using System.Text.Json;
using System.Xml;
using System.Xml.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace SaasProfessionalBuilder.Architecture;

public sealed record Finding(string Code, string Path, int Line, string Message);

public sealed class GuardConfiguration
{
    public LayerRule[] Layers { get; set; } = [];
}

public sealed class LayerRule
{
    public string Name { get; set; } = "";
    public string SourceRoot { get; set; } = "";
    public string[] ForbiddenNamespacePrefixes { get; set; } = [];
    public string[] ForbiddenProjectNameFragments { get; set; } = [];
}

public static class ArchitectureScanner
{
    private static readonly StringComparison PathComparison = OperatingSystem.IsWindows()
        ? StringComparison.OrdinalIgnoreCase : StringComparison.Ordinal;

    public static IReadOnlyList<Finding> Check(string projectRoot)
    {
        var root = Path.GetFullPath(projectRoot);
        var findings = new List<Finding>();
        void Add(string code, string path, int line, string message) =>
            findings.Add(new Finding(code, Path.GetRelativePath(root, path), line, message));

        var configurationPath = Path.Combine(root, "architecture-guard.json");
        if (!Directory.Exists(root) || !File.Exists(configurationPath))
        {
            Add("CONFIG", configurationPath, 1, "A real project root and architecture-guard.json are required.");
            return findings;
        }

        GuardConfiguration? config;
        try
        {
            config = JsonSerializer.Deserialize<GuardConfiguration>(File.ReadAllText(configurationPath),
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true,
                    UnmappedMemberHandling = System.Text.Json.Serialization.JsonUnmappedMemberHandling.Disallow });
        }
        catch (JsonException exception)
        {
            Add("CONFIG", configurationPath, 1, $"Invalid configuration: {exception.Message}");
            return findings;
        }

        if (config?.Layers is null || config.Layers.Length != 2 ||
            !config.Layers.Select(layer => layer?.Name).Order().SequenceEqual(new[] { "Application", "Domain" }))
        {
            Add("CONFIG", configurationPath, 1, "Configure exactly one Domain and one Application layer.");
            return findings;
        }

        foreach (var rule in config.Layers)
        {
            if (string.IsNullOrWhiteSpace(rule.SourceRoot) ||
                rule.ForbiddenNamespacePrefixes is null || rule.ForbiddenNamespacePrefixes.Length == 0 ||
                rule.ForbiddenNamespacePrefixes.Any(string.IsNullOrWhiteSpace) ||
                rule.ForbiddenProjectNameFragments is null || rule.ForbiddenProjectNameFragments.Length == 0 ||
                rule.ForbiddenProjectNameFragments.Any(string.IsNullOrWhiteSpace))
            {
                Add("CONFIG", configurationPath, 1, $"{rule.Name}: source root and nonempty forbidden rules are required.");
                continue;
            }

            var sourceRoot = Path.GetFullPath(Path.Combine(root, rule.SourceRoot));
            if (Path.IsPathRooted(rule.SourceRoot) || !IsWithin(root, sourceRoot) || !Directory.Exists(sourceRoot) || HasLinkedAncestor(root, sourceRoot))
            {
                Add("SOURCE", sourceRoot, 1, $"{rule.Name}: source must be an existing directory inside the project.");
                continue;
            }

            var sourceFiles = EnumerateSource(sourceRoot, Add).ToArray();
            var csharpFiles = sourceFiles.Where(path => path.EndsWith(".cs", StringComparison.OrdinalIgnoreCase)).ToArray();
            if (csharpFiles.Length == 0)
                Add("SOURCE", sourceRoot, 1, $"{rule.Name}: no C# source files were inspected.");

            var trees = csharpFiles.Select(path => CSharpSyntaxTree.ParseText(File.ReadAllText(path), path: path)).ToArray();
            if (csharpFiles.Length > 0 && !trees.Any(tree => tree.GetRoot().DescendantNodes()
                .Any(node => node is BaseTypeDeclarationSyntax or DelegateDeclarationSyntax or GlobalStatementSyntax)))
                Add("SOURCE", sourceRoot, 1, $"{rule.Name}: source contains no type declarations or executable statements.");
            var globalUsings = trees.SelectMany(tree => tree.GetCompilationUnitRoot().Usings)
                .Where(directive => directive.GlobalKeyword.IsKind(SyntaxKind.GlobalKeyword)).ToArray();
            foreach (var tree in trees)
                InspectSyntax(rule, tree, globalUsings, Add);

            var projects = sourceFiles.Where(path => path.EndsWith(".csproj", StringComparison.OrdinalIgnoreCase)).ToArray();
            if (projects.Length == 0)
                Add("PROJECT", sourceRoot, 1, $"{rule.Name}: a separate .csproj is required so project dependencies can be inspected.");
            foreach (var project in projects)
                InspectProjectGraph(root, project, rule, new HashSet<string>(OperatingSystem.IsWindows()
                    ? StringComparer.OrdinalIgnoreCase : StringComparer.Ordinal), Add);
        }

        return findings.Distinct().OrderBy(item => item.Path, StringComparer.Ordinal)
            .ThenBy(item => item.Line).ThenBy(item => item.Code, StringComparer.Ordinal).ToArray();
    }

    private static IEnumerable<string> EnumerateSource(string directory, Action<string, string, int, string> add)
    {
        if ((File.GetAttributes(directory) & FileAttributes.ReparsePoint) != 0)
        {
            add("SOURCE", directory, 1, "Linked source directories are not inspected; use a concrete source tree.");
            yield break;
        }
        foreach (var path in Directory.EnumerateFileSystemEntries(directory).Order(StringComparer.Ordinal))
        {
            var attributes = File.GetAttributes(path);
            if ((attributes & FileAttributes.ReparsePoint) != 0)
            {
                add("SOURCE", path, 1, "Linked source files/directories are not supported.");
                continue;
            }
            if ((attributes & FileAttributes.Directory) != 0)
            {
                if (Path.GetFileName(path) is "bin" or "obj" or ".git") continue;
                foreach (var child in EnumerateSource(path, add)) yield return child;
            }
            else if (path.EndsWith(".cs", StringComparison.OrdinalIgnoreCase) ||
                     path.EndsWith(".csproj", StringComparison.OrdinalIgnoreCase)) yield return path;
        }
    }

    private static void InspectSyntax(LayerRule rule, SyntaxTree tree, UsingDirectiveSyntax[] globalUsings,
        Action<string, string, int, string> add)
    {
        var syntax = tree.GetRoot();
        foreach (var diagnostic in tree.GetDiagnostics().Where(item => item.Severity == DiagnosticSeverity.Error))
            add("SYNTAX", tree.FilePath, diagnostic.Location.GetLineSpan().StartLinePosition.Line + 1, diagnostic.GetMessage());
        foreach (var trivia in syntax.DescendantTrivia().Where(item => item.IsKind(SyntaxKind.DisabledTextTrivia)))
            if (!string.IsNullOrWhiteSpace(trivia.ToString()))
                add("CONDITIONAL_SOURCE", tree.FilePath, trivia.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                    "Inactive conditional source cannot be certified by this configuration-independent check.");

        foreach (var name in syntax.DescendantNodes().Where(node => node is NameSyntax or MemberAccessExpressionSyntax))
        {
            if (name.Parent is NameSyntax) continue;
            // Only visible usings apply: compilation unit, enclosing namespaces and global usings.
            var usings = globalUsings.Concat(name.Ancestors().SelectMany(node => node switch
            {
                CompilationUnitSyntax unit => unit.Usings,
                BaseNamespaceDeclarationSyntax space => space.Usings,
                _ => default(SyntaxList<UsingDirectiveSyntax>)
            })).ToArray();
            var raw = CanonicalName(name);
            var candidates = new HashSet<string>(StringComparer.Ordinal) { raw };
            foreach (var directive in usings.Where(item => item.Name is not null))
            {
                var imported = CanonicalName(directive.Name!);
                if (directive.Alias is not null)
                {
                    var alias = directive.Alias.Name.Identifier.ValueText;
                    if (raw == alias) candidates.Add(imported);
                    else if (raw.StartsWith(alias + ".", StringComparison.Ordinal))
                        candidates.Add(imported + raw[alias.Length..]);
                    else if (raw.StartsWith(alias + "::", StringComparison.Ordinal))
                        candidates.Add(imported + "." + raw[(alias.Length + 2)..]);
                }
                else if (!directive.StaticKeyword.IsKind(SyntaxKind.StaticKeyword)) candidates.Add(imported + "." + raw);
            }
            // C# composes nested namespace blocks. Resolve their complete outer-to-inner
            // name before considering parent scopes, just as for a dotted/file-scoped name.
            var enclosingNamespace = string.Join(".", name.Ancestors().OfType<BaseNamespaceDeclarationSyntax>()
                .Reverse().Select(enclosing => CanonicalName(enclosing.Name)));
            while (enclosingNamespace.Length > 0)
            {
                candidates.Add(enclosingNamespace + "." + raw);
                var dot = enclosingNamespace.LastIndexOf('.');
                enclosingNamespace = dot < 0 ? "" : enclosingNamespace[..dot];
            }
            var forbidden = candidates.FirstOrDefault(candidate => ForbiddenNamespace(candidate, rule));
            if (forbidden is not null)
                add("DEPENDENCY", tree.FilePath, name.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                    $"{rule.Name} references forbidden namespace/type '{forbidden}'.");
        }
    }

    private static string CanonicalName(SyntaxNode name) =>
        string.Concat(name.DescendantTokens().Select(token => token.ValueText)).Replace("global::", "", StringComparison.Ordinal);

    private static bool ForbiddenNamespace(string name, LayerRule rule) =>
        rule.ForbiddenNamespacePrefixes.Any(prefix => name == prefix || name.StartsWith(prefix + ".", StringComparison.Ordinal));

    private static void InspectProjectGraph(string root, string project, LayerRule rule, HashSet<string> visited,
        Action<string, string, int, string> add)
    {
        project = Path.GetFullPath(project);
        if (!visited.Add(project)) return;
        if (!IsWithin(root, project) || !File.Exists(project))
        {
            add("PROJECT", project, 1, "Referenced project is missing or outside the inspected project root.");
            return;
        }
        if (HasLinkedAncestor(root, project))
        {
            add("PROJECT", project, 1, "Linked project files are not inspected.");
            return;
        }

        XDocument document;
        try
        {
            using var reader = XmlReader.Create(project, new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null });
            document = XDocument.Load(reader, LoadOptions.SetLineInfo);
        }
        catch (XmlException exception)
        {
            add("PROJECT", project, exception.LineNumber, $"Malformed project XML: {exception.Message}");
            return;
        }
        if (document.Root?.Name.LocalName != "Project")
        {
            add("PROJECT", project, 1, "Expected an MSBuild Project element.");
            return;
        }
        foreach (var element in document.Descendants())
        {
            var line = ((IXmlLineInfo)element).LineNumber;
            var kind = element.Name.LocalName;
            if (kind is "PackageReference" or "Reference" or "FrameworkReference")
            {
                var value = (string?)element.Attribute("Include") ?? (string?)element.Attribute("Update") ?? "";
                if (Unresolved(value)) add("PROJECT", project, line, "Dependency identifier requires MSBuild evaluation; it was not inspected.");
                else if (ForbiddenNamespace(value.Split(',')[0].Trim(), rule))
                    add("DEPENDENCY", project, line, $"{rule.Name} depends on forbidden {kind} '{value}'.");
            }
            if (kind != "ProjectReference") continue;
            var include = (string?)element.Attribute("Include") ?? "";
            if (Unresolved(include))
            {
                add("PROJECT", project, line, "ProjectReference must be a literal path for this source check.");
                continue;
            }
            var portable = include.Replace('\\', Path.DirectorySeparatorChar).Replace('/', Path.DirectorySeparatorChar);
            var dependency = Path.GetFullPath(Path.Combine(Path.GetDirectoryName(project)!, portable));
            var dependencyName = Path.GetFileNameWithoutExtension(dependency);
            if (rule.ForbiddenProjectNameFragments.Any(fragment => dependencyName.Contains(fragment, StringComparison.OrdinalIgnoreCase)))
                add("DEPENDENCY", project, line, $"{rule.Name} has a project dependency on '{dependencyName}'.");
            InspectProjectGraph(root, dependency, rule, visited, add);
        }
        // Project identity catches a differently named csproj with an Infrastructure assembly/namespace.
        foreach (var identity in document.Descendants().Where(element => element.Name.LocalName is "RootNamespace" or "AssemblyName"))
            if (ForbiddenNamespace(identity.Value.Trim(), rule))
                add("DEPENDENCY", project, ((IXmlLineInfo)identity).LineNumber,
                    $"{rule.Name} reaches forbidden project identity '{identity.Value.Trim()}'.");
    }

    private static bool Unresolved(string value) => string.IsNullOrWhiteSpace(value) || value.IndexOfAny(['$', '@', '*', '?', ';']) >= 0;

    private static bool IsWithin(string root, string path) =>
        path.StartsWith(Path.TrimEndingDirectorySeparator(root) + Path.DirectorySeparatorChar, PathComparison);

    private static bool HasLinkedAncestor(string root, string path)
    {
        var cursor = path;
        while (IsWithin(root, cursor))
        {
            if ((File.GetAttributes(cursor) & FileAttributes.ReparsePoint) != 0) return true;
            cursor = Path.GetDirectoryName(cursor)!;
        }
        return (File.GetAttributes(root) & FileAttributes.ReparsePoint) != 0;
    }
}
