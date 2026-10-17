# The rules

The rules every kit and every app built on the kits follows — written for the agents that write and
review the code, and for the people who read it — one file per topic, each with its reason, an example
and how it is checked. The files live in [`skills/conventions/references/`](../skills/conventions/references/)
so that the `conventions` skill ships them as they are; this page is their index.

| Rule | Checked by |
|---|---|
| [Package naming — namespace, layer once, nothing repeated](../skills/conventions/references/package-naming.md) | build-kit's namespace, Detekt `LayerPackageRequired`, `scripts/check-namespaces.py` |
| [Files and names — one declaration per file, `Impl`, constants, the component / preview border, dependency names](../skills/conventions/references/files-and-names.md) | Detekt `MatchingDeclarationName`, review |
| [Modules — `features/{shared,client,store}`, dependency direction, apps hold no screen, the owning feature's rule](../skills/conventions/references/modules.md) | review, `code-review` greps |
| [Presentation structure — screens, contract, models, mappers, sheets, component ViewModels](../skills/conventions/references/presentation-structure.md) | review |
| [Components — state + composable, boundaries by trigger, names, parameter order, one-parameter callbacks, render contracts](../skills/conventions/references/components.md) | review |
| [Design system — two modules, no Material, atoms and molecules, `State<T>` only for frequent values, tokens only](../skills/conventions/references/design-system.md) | review, `grep` for Material imports |
| [Previews — private, `Preview` / `Preview<State>`, `PreviewWrapper`](../skills/conventions/references/previews.md) | Detekt `PreviewMustBePrivate`, review |
| [Data and domain — `Dto`, plain domain names, the `DataSource` family, thin repositories](../skills/conventions/references/data-and-domain.md) | review |
| [Navigation — `presentation/navigation/`, `GraphProvider`, route keys](../skills/conventions/references/navigation.md) | nav-kit, review |
| [DI modules — `ViewModelsModule`, `ProvidersModule`, `BindingsModule`](../skills/conventions/references/di-modules.md) | review |
| [Insets and the keyboard — each inset once, `imePadding` then `navigationBarsPadding`, `adjustResize`, iOS `DoNothing`](../skills/conventions/references/insets.md) | review, `code-review` greps |
| [Strings — `UiString`, keys, where they live](../skills/conventions/references/strings.md) | review |
| [Compose performance — immutable collections, stability, phases](../skills/conventions/references/compose-performance.md) | stability report, review |
| [Comments — none by default; a number, a constraint, a trap, a rule code or a "because" earns one; short](../skills/conventions/references/comments.md) | review, the comment listing of `code-review` |
| [Tests — backtick names, Mokkery, fakes with behaviour, what is tested](../skills/conventions/references/tests.md) | review |
| [Documentation — a README per `api` module](../skills/conventions/references/documentation.md) | the kit's done-list, review |
| [Formatting — editorconfig and the custom Detekt rules](../skills/conventions/references/formatting.md) | ktlint, Detekt |
| [Dependencies — exact catalog versions, no `+`](../skills/conventions/references/dependencies.md) | `scripts/sync-kits.py --check`, review |
| [Kit styling — looks from the app's design system, one mapping file, examples only in `sample/`](../skills/conventions/references/kit-styling.md) | `requires`, skill, review |

`review` means: carried to agents by the `conventions` skill and checked by `code-review`. These
rules get no new Detekt rule: they are instructions. Detekt keeps what it checks today — formatting,
layers, private previews and the four style rules in `build-logic/detekt-rules`.

## Adding or changing a rule

- One rule per file in `skills/conventions/references/`, named after what it governs
  (`package-naming.md`), and a row here and in the skill's task table.
- Sections: **Rule** (numbered, each stated so it can be checked) and **Checked by** always; **Why**,
  **Example**, **Scenarios considered** (the alternatives and why they lost) and **Where it is applied**
  when the rule was a choice between options.
- A rule a kit breaks is not written until the kit is fixed or the rule names the exception —
  `code-review` over every kit says which.
- A rule that a tool can check without false positives may become a Detekt rule in
  `build-logic/detekt-rules`, synced into every kit by `scripts/sync-kits.py`.
