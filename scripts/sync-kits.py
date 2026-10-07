#!/usr/bin/env python3
"""Sync conventions-kit's build logic into the sibling kits, renamed — or, with --check, report drift.

    scripts/sync-kits.py [--check] [kit ...]

Kits are the directories next to this repository that hold a kit.yml (all of them when none is named).
Each gets `build-logic/` rendered from this repository's: `io.thernal.conventionskit` becomes the kit's
`package`, `conventionskit` its `alias` (kit.yml), and `build-logic/SYNCED` records a SHA-256 per file,
which the kit's own build verifies (`verifyBuildLogic`). build-kit has a build logic of its own and takes
only `detekt-rules` (D26 C1).

--check changes nothing. It reports, per kit: synced files that differ from what a sync would write,
catalog aliases the synced build logic reads but the kit's `gradle/libs.versions.toml` lacks, a missing
`app.namespace`, and dynamic versions in the catalog. Exit status 1 when anything is reported.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMEWORK = os.path.dirname(HERE)
MASTER_PACKAGE = "io.thernal.conventionskit"
MASTER_ALIAS = "conventionskit"
IGNORED = {"build", ".gradle", ".kotlin", ".idea"}
MANIFEST = "SYNCED"
FULL_PARTS = ["convention", "detekt-rules", "settings.gradle.kts"]
PARTS = {"build-kit": ["detekt-rules"]}


def kit_yml(kit_dir):
    text = open(os.path.join(kit_dir, "kit.yml")).read()

    def field(name):
        match = re.search(r"^" + name + r":\s*(\S+)", text, re.M)
        return match.group(1) if match else None

    return field("package"), field("alias")


def master_files(parts):
    root = os.path.join(HERE, "build-logic")
    for part in parts:
        path = os.path.join(root, part)
        if os.path.isfile(path):
            yield part
            continue
        for directory, directories, files in os.walk(path):
            directories[:] = sorted(d for d in directories if d not in IGNORED)
            for name in sorted(files):
                if name == ".DS_Store":
                    continue
                yield os.path.relpath(os.path.join(directory, name), root)


def render(relative, package, alias):
    source = os.path.join(HERE, "build-logic", relative)
    target_path = relative.replace(
        MASTER_PACKAGE.replace(".", "/"), package.replace(".", "/")
    )
    data = open(source, "rb").read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return target_path, data
    text = text.replace(MASTER_PACKAGE, package).replace(MASTER_ALIAS, alias)
    return target_path, text.encode("utf-8")


def rendered(kit_dir, parts):
    package, alias = kit_yml(kit_dir)
    if not package or not alias:
        raise SystemExit(f"{kit_dir}/kit.yml names no package or alias")
    return dict(render(relative, package, alias) for relative in master_files(parts))


def existing(kit_dir, parts):
    root = os.path.join(kit_dir, "build-logic")
    found = {}
    for part in parts:
        path = os.path.join(root, part)
        if os.path.isfile(path):
            found[part] = open(path, "rb").read()
            continue
        for directory, directories, files in os.walk(path):
            directories[:] = [d for d in directories if d not in IGNORED]
            for name in files:
                if name == ".DS_Store":
                    continue
                full = os.path.join(directory, name)
                found[os.path.relpath(full, root)] = open(full, "rb").read()
    return found


def master_commit():
    def git(*args):
        return subprocess.run(["git", "-C", HERE, *args], capture_output=True, text=True).stdout.strip()

    commit = git("rev-parse", "--short", "HEAD") or "uncommitted"
    if git("status", "--porcelain", "--", "build-logic"):
        commit += "+local changes"
    return commit


def manifest_text(files):
    lines = [
        f"# Synced from conventions-kit {master_commit()} by scripts/sync-kits.py.",
        "# Do not edit build-logic/ here: change conventions-kit and sync again.",
        "# The kit's build checks every file below (verifyBuildLogic).",
    ]
    for path in sorted(files):
        lines.append(f"{hashlib.sha256(files[path]).hexdigest()}  {path}")
    return "\n".join(lines) + "\n"


def write(kit_dir, parts, files):
    root = os.path.join(kit_dir, "build-logic")
    for path in existing(kit_dir, parts):
        os.remove(os.path.join(root, path))
    for path, data in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "wb").write(data)
    for part in parts:
        top = os.path.join(root, part)
        for directory, directories, _ in os.walk(top, topdown=False):
            if not os.listdir(directory):
                os.rmdir(directory)
    open(os.path.join(root, MANIFEST), "w").write(manifest_text(files))


def required_aliases(files):
    """Catalog aliases the rendered build logic reads: build-file accessors and runtime lookups."""
    build, runtime = set(), set()
    for path, data in files.items():
        text = data.decode("utf-8", "replace")
        if path.endswith(".gradle.kts"):
            for accessor in re.findall(r"\blibs\.((?:versions|plugins)\.)?([a-z0-9]+(?:\.[a-z0-9]+)*)", text):
                kind, name = accessor
                if name.endswith(".get"):
                    name = name[: -len(".get")]
                if name == "toml":
                    continue
                build.add(((kind or "libraries.").rstrip("."), name.replace(".", "-")))
        for kind, name in re.findall(r"(?:catalog|libs)\.(library|version)\(\"([^\"]+)\"\)", text):
            runtime.add(("libraries" if kind == "library" else "versions", name))
    return build, runtime


def catalog_aliases(kit_dir):
    path = os.path.join(kit_dir, "gradle", "libs.versions.toml")
    section, aliases, dynamic = None, set(), []
    for line in open(path):
        stripped = line.strip()
        header = re.match(r"^\[(\w+)\]", stripped)
        if header:
            section = header.group(1)
            continue
        entry = re.match(r"^([A-Za-z0-9_.-]+)\s*=", stripped)
        if entry and section:
            aliases.add((section, entry.group(1).replace("_", "-").replace(".", "-")))
        if section == "versions" and re.search(r'=\s*"[^"]*(\+|latest\.)', stripped):
            dynamic.append(stripped)
    return aliases, dynamic


def check(kit_dir, parts, files):
    name = os.path.basename(kit_dir)
    problems = []
    current = existing(kit_dir, parts)
    for path in sorted(set(files) | set(current)):
        if path not in current:
            problems.append(f"missing  build-logic/{path}")
        elif path not in files:
            problems.append(f"extra    build-logic/{path}")
        elif current[path] != files[path]:
            problems.append(f"differs  build-logic/{path}")
    manifest = os.path.join(kit_dir, "build-logic", MANIFEST)
    if not os.path.isfile(manifest):
        problems.append(f"missing  build-logic/{MANIFEST}")
    aliases, dynamic = catalog_aliases(kit_dir)
    build, runtime = required_aliases(files)
    for section, alias in sorted(build):
        if (section, alias) not in aliases:
            problems.append(f"catalog  [{section}] {alias} — the build logic does not compile without it")
    warnings = [
        f"catalog  [{section}] {alias} — read when a module applies the plugin that needs it"
        for section, alias in sorted(runtime)
        if (section, alias) not in aliases
    ]
    for line in dynamic:
        problems.append(f"version  dynamic: {line}")
    properties = os.path.join(kit_dir, "gradle.properties")
    if name != "build-kit" and "app.namespace=" not in (open(properties).read() if os.path.isfile(properties) else ""):
        problems.append("property app.namespace is not set in gradle.properties")
    return problems, warnings


def kits(names):
    found = []
    for entry in sorted(os.listdir(FRAMEWORK)):
        path = os.path.join(FRAMEWORK, entry)
        if path == HERE or not os.path.isfile(os.path.join(path, "kit.yml")):
            continue
        if not os.path.isdir(os.path.join(path, "build-logic")):
            continue
        if names and entry not in names:
            continue
        found.append(path)
    missing = set(names) - {os.path.basename(path) for path in found}
    if missing:
        raise SystemExit("no such kit next to conventions-kit: " + ", ".join(sorted(missing)))
    return found


def main(argv):
    checking = "--check" in argv
    names = [arg for arg in argv if not arg.startswith("--")]
    failed = False
    for kit_dir in kits(names):
        name = os.path.basename(kit_dir)
        parts = PARTS.get(name, FULL_PARTS)
        files = rendered(kit_dir, parts)
        if not checking:
            write(kit_dir, parts, files)
        problems, warnings = check(kit_dir, parts, files)
        status = "drift" if problems else "in sync"
        print(f"{name:16} {status}" + ("" if checking else f" (wrote {len(files)} files)"))
        for line in problems + warnings:
            print(f"  {line}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
