# Compose performance

## Rule

1. **Collections exposed to Compose are `kotlinx.collections.immutable` types.**
2. **`@Immutable` / `@Stable` only where the compiler cannot prove stability.** Every presentation model an
   `api` publishes carries one. In an `impl` only a class that holds something the compiler reads as unstable —
   an `Instant`, a `List`, an interface or sealed interface used as a field type — carries it; a state,
   callbacks, route or small model of primitives, strings, enums and `State`-free lambdas does not. Check with
   the stability report (`-PcomposeStabilityReport=true`): an annotation on a class it already reports stable is
   removed. Domain models carry neither ([data-and-domain](data-and-domain.md) rule 9).
3. **Animated values are read in the draw or layout phase** (`graphicsLayer {}`, `offset {}`), never
   in the composable's body.
4. **No `Modifier.composed`**; write `@Composable` modifier functions.
5. **Derived values**: a `derivedStateOf` field on the state, or `select` at the call site; never
   unwrap `.value` high up and pass raw values down, and never write
   `remember(state) { derivedStateOf { state.value.x } }` by hand — that is what `select` is.
6. **A `State` is read in the smallest composable that needs it.** `Content` reads none: a value that
   only the footer uses goes to a footer component through a mapper
   (`state.toSubmitFooterState()`), or the whole screen recomposes when it changes.

## Checked by

build-kit's Compose stability report (rules 1–2); review.
