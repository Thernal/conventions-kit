# Compose performance

## Rule

1. **Collections exposed to Compose are `kotlinx.collections.immutable` types.**
2. **Every presentation model an `api` publishes is `@Immutable` or `@Stable`.**
3. **Animated values are read in the draw or layout phase** (`graphicsLayer {}`, `offset {}`), never
   in the composable's body.
4. **No `Modifier.composed`**; write `@Composable` modifier functions.
5. **Derived values**: a `derivedStateOf` field on the state, or `select` at the call site; never
   unwrap `.value` high up and pass raw values down.

## Checked by

build-kit's Compose stability report (rules 1–2); review.
