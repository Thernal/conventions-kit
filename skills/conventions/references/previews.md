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
6. **No preview data shared between screens**; `PreviewParameterProvider`s live in `preview/` of the
   module or the screen ([presentation-structure](presentation-structure.md)).

## Example

```kotlin
@Composable
internal fun LoginUsernameInput(
    state: State<LoginUsernameInputState>,
    onChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) { … }

private val SampleState = LoginUsernameInputState(value = "ada")

@DsPreview
@Composable
private fun Preview() {
    LoginUsernameInput(state = stateOf(SampleState), onChange = {})
}
```

## Checked by

Detekt `PreviewMustBePrivate`; names: the `conventions` skill and `conventions-review`.
