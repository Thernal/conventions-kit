---
name: conventions-review
description: Reviews Kotlin and Compose Multiplatform code against the Thernal kits' conventions (the `conventions` skill's rules) and reports every finding by rule, file and line, with the fix. Use it when asked to review a branch, a pull request, a diff, a module or a whole kit against the conventions — "review this against our rules", "conventions review", "check the branch before I push", "does this kit follow the conventions". Reports; changes nothing unless asked to fix. Not for bug hunting or general code review, and not for projects that do not use the kits.
---

# conventions-review

Checks code against the rules in the `conventions` skill and reports what breaks them. It does
not hunt for bugs — a correctness review is a different job.

## 1. Scope

- **A diff** (default): the current branch against `main` — `git diff main...HEAD` plus uncommitted
  changes. Review the changed lines and what they touch (a renamed type's callers, a moved file's
  package), not the untouched rest of the file.
- **A path or module**: every file under it.
- **A whole kit**: every module, its sample, docs and `kit.yml`.

## 2. Load the rules

Read `../conventions/SKILL.md`, then every reference the scope touches — for a whole kit, all of
them. Do not review from memory: the reference files are the rules.

## 3. Mechanical checks first

Run what can be counted before reading code:

```sh
grep -rn --include=*.kt -E "class Default\w+|object Default\w+" .                 # Impl, never Default
grep -rn --include=*.kt -E "interface \w+(Wiring|Bindings)\b" .                    # …Module names
grep -rn --include=*.kt -E "^(private )?const val" .                               # constants: where in the file?
grep -rn -E '=\s*"[^"]*\+"' gradle/libs.versions.toml                               # dynamic versions
grep -rn --include=*Test.kt -A1 "@Test" . | grep "fun [a-z]"                         # test names not in backticks
grep -rn --include='*.kt' "androidx.compose.material" designsystem/ features/        # no Material in an app (design-system rule 2)
```

and count top-level declarations per file (more than one non-private one, outside a sealed
hierarchy or a type with its factory/`remember`/`Local`, is a finding). In a kit next to
conventions-kit, its `scripts/check-namespaces.py <kit>` and `scripts/sync-kits.py --check <kit>`
cover packages, build-logic drift and the catalog.

## 4. Read the code, rule by rule

For each file in scope: package and file shape, names, constants, comments; then by kind — a
screen against presentation-structure, a component against components and previews, data and
domain types against data-and-domain, routes and graphs against navigation, binding containers
against di-modules, tests against tests, UI in a kit against kit-styling. Measure complexity
when a function reads as long: more than 8 (Detekt `CognitiveComplexMethod`) is split.

## 5. Report

One line per finding, most important first, grouped by rule:

```
package-naming · media/ui/src/…/crop/ImageCropScreen.kt:1 · package repeats the layer · drop `.presentation`
files-and-names · …/SessionManager.kt:12 · six declarations in one file · one file each (Tokens.kt, TokenStore.kt, …)
```

Then a short summary: findings per rule, and what the fix would break for code that uses it (a
renamed public type is a breaking change: say so, and the grep that finds its users). When asked
to fix, fix by rule, re-run the checks of §3 and the project's build, and report what changed.
