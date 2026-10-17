---
name: code-review
description: Reviews a branch, a merge or pull request, a diff, a module or a whole kit in a Compose Multiplatform project on the Thernal kits, in two passes — the rules (the conventions skill — names, packages, file shape, components, state reads, comments) and correctness (bugs, Compose state and recomposition, lifecycle and coroutines, multiplatform pitfalls, accessibility, API design, build, security, tests) — and reports each finding with file, line and fix, most severe first. Use it for "review the MR", "review this branch", "code review", "check the diff before I push", "review this against our rules", "does this kit follow the conventions", "MR-a bax", "review et", "branch-ı yoxla". Both passes run unless the request names one. Reports; changes nothing unless asked to fix. Not for projects that do not use the kits.
---

# code-review

One review, two passes: **rules** — what the `conventions` skill says — and **correctness** — what is wrong
whatever the rules say. Both run unless the request names one ("only the rules", "only bugs").

## 1. Scope

- **A diff** (default): the current branch against its base — the base branch the project's
  `.agents/workspace.md` names, else `main` — `git diff <base>...HEAD` plus uncommitted changes. Review the
  changed lines and what they touch (a renamed type's callers, a moved file's package), not the untouched rest.
- **A merge or pull request**: `git fetch`, then `git diff origin/<base>...origin/<branch>`; prefer the fresh
  `origin/<branch>` to a stale local MR ref. `git log origin/<base>..origin/<branch>` says who wrote what and
  whether it carries another MR's commits (review only the new ones, and say so). Listing MRs, reading their
  discussions and approvals is the project's tracker skill (`gitlab`, or whatever the project uses).
- **A path or module**: every file under it. **A whole kit**: every module, its sample, docs and `kit.yml`.

Read each changed file whole, not only the hunks.

## 2. Load the rules

Read `../conventions/SKILL.md`, then every reference the scope touches — for a whole kit, all of them. Do not
review from memory: the reference files are the rules.

## 3. Pass one — the rules

### Mechanical checks first

Run what can be counted before reading code:

```sh
grep -rn --include=*.kt -E "class Default\w+|object Default\w+" .                 # Impl, never Default
grep -rn --include=*.kt -E "interface \w+(Wiring|Bindings)\b" .                    # …Module names
grep -rn --include=*.kt -E "^(private )?const val" .                               # constants: where in the file?
grep -rn -E '=\s*"[^"]*\+"' gradle/libs.versions.toml                               # dynamic versions
grep -rn --include=*Test.kt -A1 "@Test" . | grep "fun [a-z]"                         # test names not in backticks
grep -rn --include='*.kt' "androidx.compose.material" core/designsystem/ features/        # no Material in an app (design-system rule 2)
grep -rn --include='*.kt' -E "StepRoute|\w+Actions\b" features apps                        # route names, Callbacks not Actions
grep -rln --include='*.kt' -E "compose.runtime.(Immutable|Stable)|collections.immutable" $(find features -type d -name domain -not -path '*/build/*')
                                                                                            # pure domain models (data-and-domain rule 9)
grep -rn --include='*Content.kt' -E "derivedStateOf|state\.value" features/                  # a Content reads no state (components rule 4)
grep -rn --include='*.kt' -E "remember(\([^)]*\))? \{ \{" features/                        # no callback wrapped in remember (components rule 6)
grep -rn --include='*.kt' -E "on[A-Z]\w*: \([^)]*,[^)]*\) ->" features/ core/designsystem/  # a callback takes one parameter (components rule 5)
grep -rn --include='*.kt' -E "\b(repository|source|store)\s*:\s*[A-Z]\w+" features/ apps/          # a dependency named after its type (files-and-names rule 9)
grep -rln --include='*.kt' -E "class \w+(State|Callbacks)\(" features/ | grep "/model/"      # a component's state sits with its component (components rule 1)
grep -rn --include='*.kt' -E "(val|var) \w+: (Mutable)?(State)?Flow<" $(find features -type d -path '*/data/repository' -not -path '*/build/*')
                                                                                            # no flow held by a repository (data-and-domain rule 3)
grep -rn --include='*.kt' -B1 -E "^(internal )?(data )?class \w+" $(find features -type d -path '*/impl/src/commonMain' -not -path '*/build/*') | grep -E "@(Immutable|Stable)"
                                                                                            # impl: only where the stability report needs it (compose-performance rule 2)
grep -rn --include='*ProvidersModule.kt' "ViewModelKey" features                             # ViewModels only in ViewModelsModule (di-modules rule 4)
grep -n "projects.features" $(find features -path '*/api/build.gradle.kts' -not -path '*/build/*')   # an api never depends on another feature's api
grep -rn "windowSoftInputMode" apps/*/android/src/main/AndroidManifest.xml                   # adjustResize (insets rule 3)
grep -rn "onFocusBehavior" apps/*/shared/src/iosMain                                        # OnFocusBehavior.DoNothing (insets rule 4)
find features -maxdepth 4 -type d -name testing                                             # a feature with a fake has a testing module
```

and list every comment of the scope for a verdict — the ones that restate a name, say who uses a
declaration or describe another class are findings (comments, rules 2 and 7):

```sh
git diff main...HEAD -U0 -- '*.kt' '*.kts' | grep -E '^\+\s*(/\*\*|\*|//)'                 # every comment line a diff adds
grep -rn --include='*.kt' -A1 -E '^\s*/\*\*.*\*/\s*$' <path> | grep -E 'object |enum |data class |val |^\S+-\s+[A-Z_]+[,(]'
                                                                                            # one-line KDocs above members: the usual suspects
```

and count top-level declarations per file (more than one non-private one, outside a sealed
hierarchy or a type with its factory/`remember`/`Local`, is a finding). In a kit next to
conventions-kit, its `scripts/check-namespaces.py <kit>` and `scripts/sync-kits.py --check <kit>`
cover packages, build-logic drift and the catalog.

### Then read the code, rule by rule

For each file in scope: package and file shape, names, constants, comments (each one against the
test in comments rule 7); then by kind — a
screen against presentation-structure, a component against components and previews, data and
domain types against data-and-domain, routes and graphs against navigation, binding containers
against di-modules, tests against tests, UI in a kit against kit-styling. Measure complexity
when a function reads as long: more than 8 (Detekt `CognitiveComplexMethod`) is split.

## 4. Pass two — correctness

Order matters — spend the time on the top.

1. **Correctness**: wrong logic, off-by-one, null and empty handling, wrong defaults, copy-paste mistakes (a value
   taken from the wrong variant), dead branches, unreachable `when` arms.
2. **Compose state and performance**: state read too high, unstable parameters, allocations in composition that
   are not remembered (a `Brush`, a `TextStyle`), `remember` with missing keys, side effects in composition,
   `derivedStateOf` misuse, `.value` read in the wrong phase.
3. **Lifecycle and coroutines**: leaked scopes, collection that ignores the lifecycle, missing cancellation,
   the wrong dispatcher.
4. **Multiplatform**: platform APIs in `commonMain`, `expect`/`actual` mismatches, resources and fonts per target,
   Android and iOS behaving differently, a target missing from a module's build file.
5. **Accessibility**: touch targets, `Role`, `contentDescription` and semantics, disabled and loading states
   exposed to TalkBack and VoiceOver, contrast, font scaling (no fixed heights that clip text), right-to-left.
6. **API design**: a public surface too wide or leaking internals, defaults, variant completeness, the risk of a
   breaking change for existing users.
7. **Build and dependencies**: catalog use, new dependencies justified, module dependency direction, unused ones,
   signing and flavor files untouched.
8. **Security and data**: secrets or `.env` values committed, personal data in logs, insecure defaults.
9. **Tests**: new logic without a test.
10. **Unrelated changes**: files outside the change's purpose, generated files, leftovers.

A finding pass one already reports is not repeated here. No taste without a concrete consequence.

## 5. Verify before reporting

Confirm each candidate by reading the code path or a quick check (grep, a module build, Detekt when cheap).
Drop what cannot be substantiated, or mark it "unverified". Line numbers come from the reviewed revision
(`git show origin/<branch>:<path> | nl`), never from memory.

## 6. Report

Most severe first, in the language the user speaks; code, file names and anything meant for the MR stay
English. Rule findings, one line each, grouped by rule:

```
package-naming · media/ui/src/…/crop/ImageCropScreen.kt:1 · package repeats the layer · drop `.presentation`
comments · …/OnboardingEffect.kt:5 · KDoc turns the name into a sentence · delete
```

Correctness findings, one block each:

```
[high] path/File.kt:42 — what is wrong
  Scenario: the input or state → the wrong result
  Fix: the change, in a line or two
```

**high** = wrong behaviour, a crash, an accessibility blocker, security; **medium** = a real but narrow or
latent bug, performance, API design that will hurt later; **low** = a nit with a concrete reason. End with a
verdict (approve / approve with comments / changes requested), what the fix of a rule finding would break for
its users (a renamed public type is a breaking change: the grep that finds them), what was not reviewed and
what could not be verified. When asked to fix, fix, re-run pass one's checks and the build, and report what
changed.

## 7. Posting to the MR

Never on the agent's own initiative. When the request is to review MRs for the user, the findings go on the
MR as inline discussions in English, through the project's tracker skill; a finding on a line outside the
diff becomes a general discussion with `path:line` in its text. Nothing is approved or resolved. The
project's own house format for these comments — a signature, tags, a summary note — is a row of its
`.agents/workspace.md`; read the MR's existing discussions first and do not repeat a point already raised.
