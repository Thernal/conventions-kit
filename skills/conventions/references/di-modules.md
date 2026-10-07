# DI modules

**Decided:** 2026-10-07

## Rule

1. **`wiring` is only the name of the Gradle module.** The Metro binding containers in it are
   `Module`s, named for what they bind:
   - `<X>ViewModelsModule` — ViewModels into the ViewModel map;
   - `<X>ProvidersModule` — `@Provides` functions;
   - `<X>BindingsModule` — `@Binds` from an interface to its implementation.
2. A module binds one kind of thing; a small capability may have only one of them.

## Why

Where a ViewModel, a factory or an implementation is bound is found from the file name, and a large
feature does not grow one file of every kind of binding.

## Checked by

Review. Kits renamed in the per-kit pass (`EventWiring`, `PresentationWiring`, …).
