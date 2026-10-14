# Previews

**Decided:** 2026-10-07

## Rule

1. **Every component file ends with its previews**, annotated `@DsPreview`.
2. **Previews are `private`.**
3. **Names:** one preview is `Preview`; more are named for the state they show — `PreviewSuccess`,
   `PreviewError`, `PreviewLoading`.
4. **No theme wrapping in the body.** `@DsPreview` carries `@PreviewWrapper(ThemeWrapper::class)`;
   `ThemeWrapper : PreviewWrapperProvider` wraps every preview in the theme (ArenaGo's design).
   `PreviewWrapper` is in Compose Multiplatform 1.12's `commonMain`.
5. **Preview-only values** (`"text".ui()`) and constants sit after the component, before the
   previews — see [files-and-names](files-and-names.md) rule 7.
6. **States come from a `PreviewParameterProvider`.** A component or screen shown in more than one
   state has one `Preview(@PreviewParameter(…) state: …)` fed by a provider, not a preview function
   and a `private val Sample…` per state. Providers live in `preview/` of the screen or the module
   ([presentation-structure](presentation-structure.md)); none is shared between screens.
7. **A `State<T>` parameter gets `rememberUpdatedState(state)`** in a preview.

## Example

```kotlin
@Composable
internal fun LoginUsernameInput(
    state: State<LoginUsernameInputState>,
    actions: LoginUsernameInputActions,
    modifier: Modifier = Modifier,
) { … }

@DsPreview
@Composable
private fun Preview(@PreviewParameter(LoginUsernameInputStatePreviewProvider::class) state: LoginUsernameInputState) {
    LoginUsernameInput(state = rememberUpdatedState(state), actions = PreviewActions)
}

// view/login/preview/LoginUsernameInputStatePreviewProvider.kt
internal class LoginUsernameInputStatePreviewProvider : CollectionPreviewParameterProvider<LoginUsernameInputState>(
    listOf(LoginUsernameInputState(value = ""), LoginUsernameInputState(value = "ada")),
)
```

## Checked by

Detekt `PreviewMustBePrivate`; names: the `conventions` skill and `conventions-review`.
