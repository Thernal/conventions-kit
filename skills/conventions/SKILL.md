---
name: conventions
description: The house rules for Kotlin and Compose Multiplatform code in projects built on the Thernal kits (build-kit, arch-kit, nav-kit and the rest) — package names, one declaration per file, Impl and Module names, presentation structure (view, contract, components, mappers), component state and parameters, previews, data and domain names, navigation graphs and routes, DI modules, strings, Compose performance, comments, tests, api READMEs, kit styling, dependency versions. Use it whenever Kotlin or Compose code is written, moved, renamed or reviewed in such a project — a new feature, screen, component, ViewModel, repository, module or kit change — even when the rules are not mentioned. Not for projects that do not use the kits.
---

# conventions

The rules every kit and every app on the kits follows. Each rule file under `references/` has the
rule, why, an example and how it is checked. Read the ones the task touches before writing code;
most tasks need two or three.

## Always

These hold for every change; the rest is in the references.

- **Package** = the module's namespace (`app.namespace` + module path below `app.modules.root`) + the
  layer (`data` / `domain` / `presentation`) only in an `api`/`impl` module not named after its layer
  + topic packages by role. Nothing repeated. → [package-naming](references/package-naming.md)
- **One top-level declaration per file**, named after it; one non-preview composable per file.
  Exceptions: a sealed hierarchy, a type unusable apart from its parent, a type with its
  `remember…`/`Local…`/factory. → [files-and-names](references/files-and-names.md)
- **Names:** the one implementation is `<Interface>Impl`, never `Default…`; DI containers are
  `…ViewModelsModule` / `…ProvidersModule` / `…BindingsModule`; screens are `…View`, never `…Screen`.
- **File-private constants** at the bottom of the file — in a composable file, the component's
  before the component, the preview's between component and preview.
- **No magic values; comments say why, not what.** → [comments](references/comments.md)
- **Exact catalog versions** — no `+`. → [dependencies](references/dependencies.md)

## Which rule for which task

| Task | Read |
|---|---|
| a new module, package or file; moving code | [package-naming](references/package-naming.md), [files-and-names](references/files-and-names.md) |
| a screen: View, Content, ViewModel, contract, models, mappers | [presentation-structure](references/presentation-structure.md) |
| a component (state + composable), its parameters and callbacks; a render contract across features | [components](references/components.md) |
| a design-system component, token or modifier (`core/designsystem/`, `Ds…`) | [design-system](references/design-system.md) |
| previews | [previews](references/previews.md) |
| DTOs, domain models, data sources, repositories, use cases | [data-and-domain](references/data-and-domain.md) |
| routes, a feature's graph, sheets and dialogs as destinations | [navigation](references/navigation.md) |
| Metro binding containers | [di-modules](references/di-modules.md) |
| user-facing text | [strings](references/strings.md) |
| collections, stability, animated values, derived state | [compose-performance](references/compose-performance.md) |
| tests, fakes, stubs | [tests](references/tests.md) |
| an `api` module's README; a kit's docs | [documentation](references/documentation.md) |
| a kit that draws UI; an app styling one | [kit-styling](references/kit-styling.md) |
| formatting, the custom Detekt rules | [formatting](references/formatting.md) |
| the version catalog | [dependencies](references/dependencies.md) |

## What checks what

- **Detekt** (build-kit in apps, every kit's own build): formatting, `LayerPackageRequired`,
  `LayerPackageBoundary`, `PreviewMustBePrivate`, `ExpressionBodyNotAllowed`,
  `MultilineConstructorRequired`, `UnsafeCollectionIndexAccess`. A finding fails the build.
- **Everything else is review**: the `conventions-review` skill checks a diff rule by rule. No other
  rule becomes a Detekt rule — they are instructions, and this skill is where they live.

## Changing a rule

The rules are conventions-kit's. A project that disagrees reports it (skill-manager `report`), and
the rule changes there, with its reason — never in a project's copy of this skill.
