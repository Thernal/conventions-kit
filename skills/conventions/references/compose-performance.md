# Compose performance

## Rule

1. **Collections exposed to Compose are `kotlinx.collections.immutable` types.**
2. **Every presentation model an `api` publishes is `@Immutable` or `@Stable`.** Domain models carry neither
   ([data-and-domain](data-and-domain.md) rule 9): the screen's models are what Compose sees.
3. **Animated values are read in the draw or layout phase** (`graphicsLayer {}`, `offset {}`), never
   in the composable's body.
4. **No `Modifier.composed`**; write `@Composable` modifier functions.
5. **Derived values**: a `derivedStateOf` field on the state, or `select` at the call site; never
   unwrap `.value` high up and pass raw values down.
6. **A `State` is read in the smallest composable that needs it.** `Content` reads none: a value that
   only the footer uses goes to a footer component through a mapper
   (`state.toSubmitFooterState()`), or the whole screen recomposes when it changes.

## Checked by

build-kit's Compose stability report (rules 1–2); review.
