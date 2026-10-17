# Components

**Decided:** 2026-10-07

This file is for a feature's components. A design-system component (`Ds…`, in `core/designsystem/`) follows
[design-system](design-system.md): `State<T>` only for values that change often, plain for the rest.

## Rule

1. **A component is its state, its callbacks and its composable, in one file named after the composable.**
   `LoginUsernameInput.kt` holds `LoginUsernameInputState`, `LoginUsernameInputCallbacks` and
   `LoginUsernameInput`. It takes `State<LoginUsernameInputState>`; the screen maps its own state with
   `State<LoginState>.toLoginUsernameInputState()` (`select`) in `view/<screen>/mapper/`. A component's state
   or callbacks class is never in `model/` or `contract/`: those hold what the screen and its Logic agree on and
   the models that travel (a list item's data, an argument). A **list row** is a component too: its state is
   in the row's file, the list gives it `key(id) { Row(state = rememberUpdatedState(row), …) }`.
2. **A screen's component carries the screen's name** (`LoginUsernameInput`); a component the
   module's screens share is `internal`, lives in `presentation/components/` and has no prefix.
   No `<Screen>Components` context marker: Kotlin allows context parameters on functions only, not
   on classes, so it could not scope the state class, and `internal` already keeps it in the module.
3. **Parameters:** required ones first, then `modifier: Modifier = Modifier` as the first optional
   one, then the optional rest. Inside each group: state, config (set once, rarely changes),
   callbacks, composable slots — a slot last, so it stays a trailing lambda.
4. **Frequently changing inputs are `State<T>`**, read as late as possible; a static value is
   wrapped with `rememberUpdatedState(x)`. A part of a screen that reads a changing value — a
   footer's `enabled`, a sheet's `isVisible`, a list's rows — is its own component with its own `State<…>`,
   so only it recomposes ([compose-performance](compose-performance.md) rules 5 and 6). **`<Screen>Content`
   reads no state:** it arranges components and hands each one `state.to<Component>State()` and
   `onIntent.to<Component>Callbacks()`; a `val x by remember(state) { derivedStateOf { state.value.x } }` in a
   Content is the same mistake as unwrapping `.value`. A component made of regions that depend on state (a body
   that shows a failure, an empty state or the list) reads its own state and takes the nested screens as a
   trailing slot.
5. **Callbacks are the component's own event, as a verb**: `onSubmit`, `onBack`, `onChange` — never
   the parent's use case, never `onNav…`. `on<Thing>Click` only when the component has several
   clickable things and the thing is the meaning (`onAvatarClick`).
6. **Two or more callbacks are one `<Component>Callbacks`** — an `@Immutable data class` in the
   component's file (`CodeInputCallbacks(onChange, onSubmit)`), passed as `callbacks`. The screen builds
   it in a mapper from `onIntent` and its own `Callbacks`, remembered (`onIntent.toCodeInputCallbacks()`).
   One callback stays a parameter. Never `…Actions`: an action is the logic's word
   ([presentation-structure](presentation-structure.md) rule 2).
7. **Composables in an `impl` are `internal`**, module-shared ones included; only a render adapter
   is public.
8. **Across features, through a render contract**: `XRenderer` + `LocalXRenderer` + facade in `api`,
   `XRendererImpl` in `impl`, its `ProvidedValue` from `wiring`. Never import another feature's
   composable. The facade is `(params: XParams, modifier: Modifier = Modifier[, content])`, every
   optional input on `XParams`.
9. **Reuse before adding**: a component enters the design system only when it is product-generic.

## Why

- A component previewable from a literal state, with no screen around it.
- The parameter order is Compose's (required, then `modifier` first among the optional) refined by
  role; `NamedArguments` is enforced, so the order is for reading.

## Checked by

Detekt `MatchingDeclarationName` excludes `components/` (the file is named after the composable,
not the state class). The rest: review.
