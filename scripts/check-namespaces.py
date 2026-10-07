#!/usr/bin/env python3
"""Every module's packages start with its namespace — the package-naming rule's "Everywhere" check.

    scripts/check-namespaces.py [repository ...]

A repository is a kit (its prefix is kit.yml's `package`) or an app on build-kit (its prefix is
gradle.properties' `app.namespace`); with none named, every kit next to conventions-kit is checked.
A module's namespace is the prefix plus its directory path below `app.modules.root`, dashes split —
build-kit's derivation. Exit status 1 when a package lies outside its module's namespace.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIPPED = {"build", ".gradle", ".git", ".kotlin", "build-logic", "node_modules", ".idea"}
PACKAGE = re.compile(r"^package\s+([\w.]+)", re.M)


def prefix_of(repository):
    kit = os.path.join(repository, "kit.yml")
    if os.path.isfile(kit):
        match = re.search(r"^package:\s*(\S+)", open(kit).read(), re.M)
        if match:
            return match.group(1)
    properties = os.path.join(repository, "gradle.properties")
    if os.path.isfile(properties):
        match = re.search(r"^app\.namespace=(\S+)", open(properties).read(), re.M)
        if match:
            return match.group(1)
    return None


def modules_root(repository):
    properties = os.path.join(repository, "gradle.properties")
    if not os.path.isfile(properties):
        return []
    match = re.search(r"^app\.modules\.root=(.*)$", open(properties).read(), re.M)
    return [segment for segment in re.split(r"[/:]", match.group(1).strip()) if segment] if match else []


def packages(source_dir):
    found = set()
    for directory, directories, files in os.walk(source_dir):
        directories[:] = [d for d in directories if d not in SKIPPED]
        for name in files:
            if name.endswith(".kt"):
                match = PACKAGE.search(open(os.path.join(directory, name), errors="replace").read())
                if match:
                    found.add(match.group(1))
    return found


def check(repository):
    prefix = prefix_of(repository)
    if not prefix:
        return [f"{repository}: no kit.yml `package` and no `app.namespace`"], 0
    root = modules_root(repository)
    problems, modules = [], 0
    for directory, directories, files in os.walk(repository):
        directories[:] = [d for d in directories if d not in SKIPPED]
        if "build.gradle.kts" not in files or not os.path.isdir(os.path.join(directory, "src")):
            continue
        relative = os.path.relpath(directory, repository)
        if relative == ".":
            continue
        segments = relative.split(os.sep)
        if segments[: len(root)] == root:
            segments = segments[len(root):]
        namespace = ".".join([prefix] + [part for segment in segments for part in segment.split("-") if part])
        modules += 1
        for package in sorted(packages(os.path.join(directory, "src"))):
            if package != namespace and not package.startswith(namespace + "."):
                problems.append(f"{relative}: {package} (namespace {namespace})")
    return problems, modules


def main(argv):
    repositories = argv or [
        os.path.join(os.path.dirname(HERE), entry)
        for entry in sorted(os.listdir(os.path.dirname(HERE)))
        if os.path.isfile(os.path.join(os.path.dirname(HERE), entry, "kit.yml"))
        and os.path.join(os.path.dirname(HERE), entry) != HERE
    ]
    failed = False
    for repository in repositories:
        problems, modules = check(os.path.abspath(repository))
        print(f"{os.path.basename(os.path.abspath(repository)):16} {modules} modules, {len(problems)} off-namespace")
        for line in problems:
            print(f"  {line}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
