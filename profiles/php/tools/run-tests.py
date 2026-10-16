#!/usr/bin/env python3
"""Instala herramientas bloqueadas y prueba el perfil en un temporal propio.

Python 3.10+, PHP 8.2+ y Composer deben estar instalados. No modifica Composer
global, no carga un bootstrap de aplicación y no desactiva auditorías.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile


TOOLS = Path(__file__).resolve().parent


class CommandFailure(Exception):
    def __init__(self, returncode: int):
        self.returncode = returncode


def resolve_executable(value: str) -> str:
    resolved = shutil.which(value)
    if resolved is None:
        raise ValueError(f"No se encuentra el ejecutable: {value}")
    return str(Path(resolved).resolve())


def composer_command(value: str, php: str) -> list[str]:
    # El instalador oficial de Windows ofrece .bat + .phar. Usar el PHAR
    # elimina el shell y garantiza que Composer use el PHP seleccionado.
    candidate = Path(value)
    if candidate.suffix.lower() == ".phar":
        if not candidate.is_file():
            raise ValueError(f"No se encuentra Composer PHAR: {value}")
        return [php, str(candidate.resolve())]
    executable = Path(resolve_executable(value))
    if executable.suffix.lower() in {".bat", ".cmd"}:
        phar = executable.with_name("composer.phar")
        if not phar.is_file():
            raise ValueError("El wrapper de Composer no tiene composer.phar; usa --composer con la ruta al PHAR.")
        return [php, str(phar)]
    # Composer Unix suele ser un PHAR sin extensión con shebang. Ejecutarlo
    # directamente escogería PHP desde PATH, ignorando el --php explícito.
    with executable.open("rb") as source:
        beginning = source.read(512)
    if beginning.startswith(b"#!"):
        beginning = beginning.partition(b"\n")[2]
    if re.match(br"\s*<\?php\b", beginning):
        return [php, str(executable)]
    raise ValueError("Composer debe ser un PHAR o script PHP; usa --composer con la ruta al PHAR, sin wrappers de shell.")


def terminate_process_tree(process: subprocess.Popen) -> None:
    """Termina descendientes antes que el padre y espera antes de limpiar."""
    if os.name == "nt":
        # taskkill necesita que el padre siga vivo para encontrar el árbol;
        # no usar process.kill() antes de /T. Sin shell ni datos interpolados.
        taskkill = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe"
        result = subprocess.run(
            [str(taskkill), "/PID", str(process.pid), "/T", "/F"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=False, timeout=30)
        if result.returncode != 0 and process.poll() is None:
            raise OSError("No se pudo terminar el árbol de procesos del comando.")
    else:
        # Cada comando crea una sesión propia, que incluye sus descendientes.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=30)


def run_command(arguments: list[str], *, cwd: Path, env: dict[str, str],
                stdin, check: bool, timeout: float) -> subprocess.CompletedProcess:
    """Como run(check=False), con teardown del árbol ante timeout/interrupción."""
    process = subprocess.Popen(arguments, cwd=cwd, env=env, stdin=stdin,
                               start_new_session=(os.name != "nt"))
    try:
        returncode = process.wait(timeout=timeout)
    except BaseException:
        terminate_process_tree(process)
        raise
    if check and returncode:
        raise subprocess.CalledProcessError(returncode, arguments)
    return subprocess.CompletedProcess(arguments, returncode)


def isolated_environment(source: dict[str, str], root: Path, php: str) -> dict[str, str]:
    # Se conservan PATH, certificados y proxy del sistema. Toda configuración
    # de Composer y los overrides de las pruebas se reemplazan o descartan.
    environment = {
        key: value for key, value in source.items()
        if not key.upper().startswith(("COMPOSER", "PHPUNIT_"))
        and key.upper() not in {"SAAS_GUARD_TEMPLATE", "PHP_BINARY"}
    }
    environment.update({
        "COMPOSER_HOME": str(root / "composer-home"),
        "COMPOSER_CACHE_DIR": str(root / "composer-cache"),
        "COMPOSER": str(root / "work" / "composer.json"),
        "COMPOSER_NO_INTERACTION": "1",
        "COMPOSER_ALLOW_SUPERUSER": "1",
        "PHP_BINARY": php,
        "PYTHONDONTWRITEBYTECODE": "1",
        # Los fixtures de las suites también quedan dentro del área propia.
        "TMP": str(root / "fixtures"),
        "TEMP": str(root / "fixtures"),
        "TMPDIR": str(root / "fixtures"),
    })
    return environment


def run_profile(php: str, composer: list[str], *, tools_directory: Path = TOOLS,
                runner=run_command, source_environment: dict[str, str] | None = None,
                temp_parent: str | None = None, command_timeout: float = 900) -> int:
    """Retorna el fallo original y siempre verifica la limpieza del temporal."""
    owned = tempfile.TemporaryDirectory(prefix="saas-php-profile-", dir=temp_parent)
    root = Path(owned.name)
    status = 0
    try:
        work = root / "work"
        for directory in (work, root / "composer-home", root / "composer-cache", root / "fixtures"):
            directory.mkdir()
        for filename in ("composer.json", "composer.lock"):
            shutil.copyfile(tools_directory / filename, work / filename)
        environment = isolated_environment(
            dict(os.environ) if source_environment is None else source_environment, root, php)

        def execute(arguments: list[str]) -> None:
            result = runner(arguments, cwd=work, env=environment,
                            stdin=subprocess.DEVNULL, check=False, timeout=command_timeout)
            if result.returncode != 0:
                raise CommandFailure(result.returncode)

        base = [*composer, "--no-interaction", "--no-plugins"]
        execute([php, "--version"])
        execute([*base, "--version"])
        execute([*base, "validate", "--strict"])
        execute([*base, "audit", "--locked"])
        execute([*base, "install", "--no-scripts", "--prefer-dist", "--no-progress"])
        execute([*base, "check-platform-reqs"])
        profile = tools_directory.parent.resolve()
        vendor = work / "vendor"
        execute([php, str(vendor / "phpunit" / "phpunit" / "phpunit"),
                 "--no-configuration", "--bootstrap", str(vendor / "autoload.php"),
                 "--do-not-cache-result", str(profile / "tests" / "ArchitectureTemplateRegressionTest.php")])
        execute([sys.executable, "-B", str(profile / "tests" / "test_coverage_cli.py")])
    except CommandFailure as error:
        status = error.returncode
        print(f"Fallo de un comando del perfil PHP (exit {status}).", file=sys.stderr)
    except subprocess.TimeoutExpired:
        status = 124
        print(f"Un comando del perfil PHP superó el tiempo máximo de {command_timeout:g} segundos.", file=sys.stderr)
    except (OSError, ValueError) as error:
        status = 1
        print(f"No se pudo ejecutar el perfil PHP: {error}", file=sys.stderr)
    finally:
        try:
            owned.cleanup()
            if root.exists():
                raise OSError("el directorio temporal sigue presente")
            print("Limpieza verificada: dependencias, caché y fixtures temporales eliminados.", flush=True)
        except OSError as error:
            print(f"ERROR de limpieza del temporal {root}: {error}", file=sys.stderr)
            status = status or 1
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--php", default="php", help="Ejecutable PHP (predeterminado: php en PATH)")
    parser.add_argument("--composer", default="composer", help="Ejecutable Composer o ruta a composer.phar")
    arguments = parser.parse_args(argv)
    try:
        php = resolve_executable(arguments.php)
        composer = composer_command(arguments.composer, php)
    except ValueError as error:
        parser.error(str(error))
    return run_profile(php, composer)


if __name__ == "__main__":
    raise SystemExit(main())
