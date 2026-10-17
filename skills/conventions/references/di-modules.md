# DI modules

**Decided:** 2026-10-07

## Rule

1. **`wiring` is only the name of the Gradle module.** The Metro binding containers in it are
   `Module`s, named for what they bind:
   - `<X>ViewModelsModule` — ViewModels into the ViewModel map;
   - `<X>ProvidersModule` — `@Provides` functions;
   - `<X>BindingsModule` — `@Binds` from an interface to its implementation.
2. A module binds one kind of thing; a small capability may have only one of them.
3. **A feature's ViewModels are bound in its `wiring`** with `@Provides @IntoMap @ViewModelKey(X::class)`
   (an assisted one: `@ManualViewModelAssistedFactoryKey`), and the class in `impl` carries no Metro
   annotation. The app depends on `wiring` only, so `impl` is not on the app graph's classpath and
   Metro never sees a `@ContributesIntoMap` there: the build passes and the map lacks the ViewModel.

4. **A ViewModel is never bound in a `ProvidersModule`.** A feature with ViewModels has a
   `<X>ViewModelsModule`, however small, and keeps graph providers and renderers in `<X>ProvidersModule`.
5. **Data bindings are split so a fake can replace the source:** `<X>RepositoryProvidersModule` provides the
   repository from the source, `<X>SourceProvidersModule` provides the `…RemoteDataSource`. A fake in the
   feature's `testing` module is a container `@ContributesTo(AppScope::class, replaces =
   [<X>SourceProvidersModule::class])`; the app pulls it in for the dev flavor only ([tests](tests.md)
   rule 5). A shared repository is bound from the same instance: `@Provides fun shared(repository:
   <X>Repository): <X>SharedRepository { return repository }`.

## Why

Where a ViewModel, a factory or an implementation is bound is found from the file name, and a large
feature does not grow one file of every kind of binding.

## Checked by

Review. Kits renamed in the per-kit pass (`EventWiring`, `PresentationWiring`, …).
