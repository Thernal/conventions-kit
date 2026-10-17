# Package naming

**Decided:** 2026-10-07, by the owner · **Applies to:** every kit and every app built on build-kit

## Rule

A source file's package is, in this order, with nothing added and nothing repeated:

1. **The package prefix** — `app.namespace` (`io.thernal.archkit`, `com.example.app`).
2. **The module path below the modules root** — area, group, capability, role: `features.shared.profile.impl`
   (the group is `shared`, `client` or `store`, and a one-app product has none — `features.profile.impl`:
   [modules](modules.md) rule 1).
   The modules root (`app.modules.root`) is never part of it.
3. **The layer** — `data`, `domain` or `presentation` — only in an `api` or `impl` module, and only
   when the module path does not name the layer already. A module named after its layer
   (`core/presentation/api`) holds its code directly under the module.
4. **Topic packages** — grouped by what the code is for (`plugin.state`, `form.validator`), not to
   add depth.

**Everywhere.** Every module of every kit and app follows it — `sample` apps, `testing` and `wiring`
modules included: a file's package starts with its module's namespace. Every kit's build logic derives
the namespace the same way as build-kit (`app.namespace` + the module path below `app.modules.root`),
taken from build-kit by the build-logic sync, never written by hand.

The first two parts are the module's namespace: Android namespace, generated `Environment` package,
iOS framework bundle id and the directories `./gradlew create` scaffolds all use the same string, so
sources sit exactly under the namespace their module declares.

## Why

| Part | Why it is there, or not |
|---|---|
| Modules root left out | It is a directory, not part of any module's identity. build-kit's fixture lives under `fixture/`, and `fixture` in every package (`io.thernal.buildkit.fixture.core.config`) said nothing. Apps keep their modules at the repository root (`app.modules.root=`), so for them nothing changes. |
| Area kept (`core`, `features`, `apps`) | Without it, `core/auth` and `features/auth` get the same namespace — AGP rejects two modules with one namespace — and an app that relies on the default application id silently becomes a different app in the store. |
| Role kept (`api`, `impl`, `wiring`) | The parts of one capability need distinct Android namespaces, and the layer Detekt rules find a module's root at its first `api` or `impl` segment. |
| Layer written once | `core/presentation/api` is the presentation layer by name; a `presentation` package inside it repeats the segment and carries no information (`io.thernal.archkit.core.presentation.api.presentation.plugin.state`). A module named after a capability (`features/profile/impl`) still splits into `data`, `domain`, `presentation`, because there the layer is what the package adds. |
| Topic packages by role | A package says what its files are for (`plugin` is the machinery, `plugin.state` one plugin). A package level is added when it separates roles, never to mirror a file. |

## Examples

| Module | Before | After |
|---|---|---|
| build-kit `fixture/core/config` (`app.modules.root=fixture`) | `io.thernal.buildkit.fixture.core.config` | `io.thernal.buildkit.core.config` |
| build-kit `fixture/features/greeting/impl` | `io.thernal.buildkit.fixture.features.greeting.impl.domain` | `io.thernal.buildkit.features.greeting.impl.domain` |
| arch-kit `core/presentation/api` | `io.thernal.archkit.core.presentation.api.presentation.plugin.state` | `io.thernal.archkit.core.presentation.api.plugin.state` |
| arch-kit `core/presentation/impl` | `io.thernal.archkit.core.presentation.impl.presentation.plugin.state` | `io.thernal.archkit.core.presentation.impl.plugin.state` |
| arch-kit `core/event/api` (named after a capability) | `io.thernal.archkit.core.event.api.domain` | unchanged |

## Checked by

- **Namespace** — build-kit's `namespaceFor` (`build-logic/convention`, `ProjectExtensions.kt`),
  tested in `NamingTest`: module path, dashes split, modules root removed.
- **Layer** — Detekt `LayerPackageRequired` (`build-logic/detekt-rules`, build-kit and arch-kit):
  in a capability module a file outside `data`/`domain`/`presentation` is reported; in a module
  named after its layer, a layer package is reported ("repeats a layer"). `LayerPackageBoundary` reads
  the layer the same way.
- **Every module under its namespace** — conventions-kit's `scripts/check-namespaces.py` (each
  module's packages against `kit.yml`'s `package` + the module path).
- **Topic packages** — the `conventions` skill and `code-review`.

## Scenarios considered

| Option | Result | Why it lost or won |
|---|---|---|
| A. Leave the modules root out | chosen | Only repositories with a modules root change; real apps have none. |
| B. A, and leave the area out too | rejected | Collisions between areas fail the build, and changed default application ids reinstall apps as new ones. Only acceptable as an opt-in with a collision check. |
| C. Leave the role out (`api`/`impl`) | rejected | Duplicate namespaces inside one capability; the layer Detekt rules lose the module root. |
| D. Layer package everywhere, even in `core/presentation/api` | rejected | The repeated segment was the deepest part of every arch-kit package. |

## Where it is applied

- build-kit `ffcbefe` (2026-10-07) — modules root out of namespaces, fixture moved.
- build-kit and arch-kit, branch work 2026-10-07 — `LayerPackageRequired` knows layer-named modules;
  arch-kit's presentation packages lose the repeated `presentation`.
- Every kit, 2026-10-07: the new `LayerPackage.kt` / `LayerPackageRequired.kt` copied from build-kit
  into all nine kits' `detekt-rules` (which also fixes nav-kit's and paging-kit's dead layer rules);
  nav-kit's and paging-kit's sample apps moved under their namespaces (`…sample.shared.*`,
  `…sample.app`). No kit has another off-namespace package.
