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
   trailing slot. **A component's boundary is its trigger:** values that change on the same input (a page index,
   one field) are one component; a part that never changes (a button with a fixed label and callback) is never
   inside a component that reads state — it is a sibling in the parent, which reads nothing. Compose's skipping
   is not counted on: the scope that reads a state re-runs up to every call inside it.
5. **Callbacks are the component's own event, as a verb**: `onSubmit`, `onBack`, `onChange` — never
   the parent's use case, never `onNav…`. `on<Thing>Click` only when the component has several
   clickable things and the thing is the meaning (`onAvatarClick`). **A callback takes at most one
   parameter:** two or more values travel as one data class in the component's file
   (`onSubmit: (LoginCredentials) -> Unit`, never `onSubmit: (String, String) -> Unit`).
6. **Two or more callbacks are one `<Component>Callbacks`** — an `@Immutable data class` in the
   component's file (`CodeInputCallbacks(onChange, onSubmit)`), passed as `callbacks`. The screen builds
   it in a `@Composable` mapper from `onIntent` and its own `Callbacks` (`onIntent.toCodeInputCallbacks()`).
   One callback stays a parameter, written in place: `onClick = { onIntent(StartIntent) }`. **No callback is
   wrapped in `remember`:** strong skipping memoizes a lambda created in composition, keyed on what it
   captures, and `onIntent` does not change — a mapper that is not `@Composable` loses this and builds new
   lambdas on every call. Never `…Actions`: an action is the logic's word
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
- A boundary drawn by trigger makes a change re-run exactly what it changes. A card that reads its state at
  the top and holds the button re-runs up to the button's call on every page; whether Compose then skips the
  button depends on every argument comparing equal, which a reader of the code cannot see.
- `remember { { … } }` around a lambda repeats what the compiler already does under strong skipping (the
  default since Kotlin 2.0.20) and adds a key a reader has to check.

## Example

An introduction slideshow (compiled: Kotlin 2.4.10, Compose Multiplatform 1.12.1; imports omitted). The page
indicator, the title and the text all change with the page, so they are one component; the button never
changes, so it is a sibling in the Content, which reads nothing.

```kotlin
// view/onboarding/OnboardingContent.kt
@Composable
internal fun OnboardingContent(
    state: State<OnboardingState>,
    onIntent: (OnboardingIntent) -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier) {
        OnboardingSlide(state = state.toOnboardingSlideState())
        DsButton(onClick = { onIntent(OnboardingIntent.StartPressed) }) {
            DsText(text = stringResource(Res.string.auth_onboarding_start))
        }
    }
}

// view/onboarding/mapper/OnboardingStateMappers.kt
@Composable
internal fun State<OnboardingState>.toOnboardingSlideState(): State<OnboardingSlideState> {
    return select { screen ->
        val page = OnboardingPages[screen.currentPage]
        OnboardingSlideState(
            page = screen.currentPage,
            pageCount = screen.pageCount,
            title = page.title,
            description = page.description,
        )
    }
}

// view/onboarding/components/OnboardingSlide.kt
@Immutable
internal data class OnboardingSlideState(
    val page: Int,
    val pageCount: Int,
    val title: UiString,
    val description: UiString,
)

@Composable
internal fun OnboardingSlide(
    state: State<OnboardingSlideState>,
    modifier: Modifier = Modifier,
) {
    val slide = state.value

    Column(modifier = modifier) {
        DsPageIndicator(
            pageCount = slide.pageCount,
            currentPage = slide.page,
        )
        DsText(text = slide.title.resolve())
        DsText(text = slide.description.resolve())
    }
}
```

`OnboardingSlide` reads `.value` at its top because everything it draws depends on it. The shape this replaces:

```kotlin
// No — the button is inside the scope that reads the page, and the callback is remembered by hand
@Composable
internal fun OnboardingCard(state: State<OnboardingCardState>, onStart: () -> Unit) {
    val card = state.value
    Column {
        DsPageIndicator(pageCount = card.pageCount, currentPage = card.page)
        DsText(text = card.title.resolve())
        DsButton(onClick = onStart) { DsText(text = stringResource(Res.string.auth_onboarding_start)) }
    }
}
// …and in the Content: onStart = remember(onIntent) { { onIntent(OnboardingIntent.StartPressed) } }
```

## Checked by

Detekt `MatchingDeclarationName` excludes `components/` (the file is named after the composable,
not the state class). The rest: review.
