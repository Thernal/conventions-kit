# Design system

**Decided:** 2026-10-12

This file is what the code looks like. *When* a component or a token is added — screen by screen, or in one
pass — and how the design is read is the `design-system` skill.

## Rule

1. **Two modules, one direction.** `core/designsystem/foundation` holds the tokens and the theme (colours,
   type, spacing, rounding, motion, the theme provider); it draws nothing. `core/designsystem/components`
   holds every `Ds…` component and the modifiers they share (`pressable`, borders).
   `components` depends on `foundation`; neither depends on a feature or on another `core` module (arch-kit,
   navigation, …). The design system is a leaf. It sits in `core/designsystem/`, with the app-wide modules, and
   the kit code that styles itself through it installs beside it as `core/designsystem/<kit>` (overlay-kit:
   `core/designsystem/overlay`); packages follow the module path, `<app>.core.designsystem.foundation`.
2. **No Material.** The design system and the features import nothing from `androidx.compose.material*`.
   A behaviour Material has and the design needs (pull to refresh, a top bar's scroll state) is copied
   into `components` and rewritten on tokens, under a header naming the source file, its version, its
   licence (Apache 2.0) and what was changed.
3. **Atoms and molecules only.** An atom is one primitive (`DsButton`, `DsText`, `DsIcon`, `DsChip`,
   `DsSwitch`); a molecule composes atoms without product meaning (`DsTextField` with label, helper and
   error; `DsListRow`; `DsBanner`). A component with product vocabulary is the feature's, and other
   features get it through the owning feature's `api` render contract
   ([components](components.md) rule 8) — it is never moved up into the design system. A component
   enters the design system when a screen needs an atom or a molecule that does not exist yet: not
   before, and never to complete a set.
4. **Names.** `Ds` + a noun; a package per component (`components/button/`); its variant, size and tone
   are types of their own in that package (`DsButtonVariant`, `DsButtonSize`); one non-preview
   composable per file ([files-and-names](files-and-names.md)).
5. **Parameters.** Required first, then `modifier: Modifier = Modifier` — every component takes it and
   applies it to its root — then config, callbacks, and the content slot last
   ([components](components.md) rule 3). A value that changes often and makes its readers recompose is
   a `State<T>` — a text field's text, a progress, a drag offset, an animated alpha — read as late as
   possible (`.value` at the use, in a layout or draw lambda when the value is only drawn). Everything
   else is plain: a text field's label, `enabled`, `variant`, `size`. A plain value for a frequently
   changing parameter is a finding, and so is a `State<T>` for one that rarely changes. A constant for
   a `State<T>` parameter is `rememberUpdatedState(x)`.
6. **Looks come from tokens.** No literal colour, `dp`, `sp`, alpha or duration in a component: read
   `DsTheme.*`. A value a screen needs and foundation lacks is added to foundation in the same change;
   the commit says which screen needed it, the KDoc never does ([comments](comments.md) rule 3). A
   value is never added to complete a scale.
7. **Text is a `String` or a slot.** A component never takes a `UiString`; a feature that has one
   resolves it at the call site.
8. **Icons are values, from a library.** A component takes an `ImageVector` (or a `Painter`), never an
   icon name. The app takes its icons from a library and reaches them through its typed accessors
   (`MaterialSymbols.Rounded.Home`), never through a name lookup or a registry of the whole set: the
   shrinker drops the icons nothing references, and a lookup references all of them.
9. **Accessibility.** An interactive component sets its `role` and state semantics; an icon-only one
   takes a `contentDescription`; decorative motion respects reduced motion. The touch target is the
   component's own decision: one whose hit area is under 44dp (a chip) says why in its KDoc. There is
   no global minimum.
10. **Previews and stability.** Every variant and state has a `@DsPreview`
    ([previews](previews.md)); published models carry `@Immutable` or `@Stable`; collections are
    `kotlinx.collections.immutable`.

## Why

- A button's corner radius is one edit only if no feature draws its own button. The boundary is a
  build fact, not a habit: no Material import is available to reach past it, and the design system
  depends on nothing that could pull a feature in.
- Passing a `State<T>` moves the read into the component, so a value that changes on every keystroke or
  frame recomposes the component and not its parent. A value that rarely changes gains nothing from it
  and costs every caller a wrapper, so it stays plain and the API stays simple.
- A foundation built to look complete holds tokens no screen uses; one grown from the parameters the
  screens use holds none.
- Icons measured on iOS (release arm64 static framework, Kotlin/Native 2.4.10, Compose 1.12.0, three
  Material Symbols libraries on the classpath): no icon referenced 83.3 MB, one icon 84.1 MB, 134 icons
  85.0 MB — about 7 KB each after the first — and the whole Rounded set referenced by name 122.8 MB.
  Unreferenced icons are dropped; a name registry keeps all of them (+39.4 MB). Android's R8 is
  expected to do the same and was not measured, nor was the final app link.

## Example

The first three blocks were compiled (Kotlin 2.4.10, Compose Multiplatform 1.12.0, imports and the
theme omitted; the last two are call-site and comment shapes only). `DsTheme`, `pressable`, `DsText`
and `DsPreview` are the design system's own.

**An atom — `DsButton`** (rules 1–6). The variant and the size are values the theme resolves, built as
composable getters on the companion, one file each (`button/variants/DsButtonVariantPrimary.kt`);
`DsButtonSize` has the same shape. `onClick` is required, so it comes before `modifier`; the slot is
last. Everything is plain, nothing is a `State`: none of it changes often.

```kotlin
// button/DsButtonVariant.kt
@Immutable
data class DsButtonVariant(
    val background: Color,
    val content: Color,
    val border: Color,
) {
    companion object
}

// button/variants/DsButtonVariantPrimary.kt
val DsButtonVariant.Companion.primary: DsButtonVariant
    @Composable get() {
        return DsButtonVariant(
            background = DsTheme.colors.accent,
            content = DsTheme.colors.accentOn,
            border = DsTheme.colors.accent,
        )
    }

// button/DsButton.kt
@Composable
fun DsButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    variant: DsButtonVariant = DsButtonVariant.primary,
    size: DsButtonSize = DsButtonSize.large,
    enabled: Boolean = true,
    content: @Composable RowScope.() -> Unit,
) {
    val shape = DsTheme.rounding.radiusMd

    Row(
        modifier = modifier
            .alpha(if (enabled) 1f else DsTheme.metrics.disabledAlpha)
            .pressable(
                onPress = onClick,
                enabled = enabled,
                role = Role.Button,
            )
            .defaultMinSize(minHeight = size.height)
            .background(
                color = variant.background,
                shape = shape,
            )
            .border(
                width = DsTheme.stroke.hairline,
                color = variant.border,
                shape = shape,
            )
            .padding(size.padding),
        horizontalArrangement = Arrangement.spacedBy(
            space = DsTheme.dimens.dp8,
            alignment = Alignment.CenterHorizontally,
        ),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        CompositionLocalProvider(
            LocalContentColor provides variant.content,
            LocalTextStyle provides size.textStyle,
        ) {
            content()
        }
    }
}

@DsPreview
@Composable
private fun Preview() {
    Column(verticalArrangement = Arrangement.spacedBy(DsTheme.dimens.dp8)) {
        DsButton(onClick = {}) {
            DsText(text = "Primary")
        }
        DsButton(
            onClick = {},
            enabled = false,
        ) {
            DsText(text = "Disabled")
        }
    }
}
```

**A molecule with a frequent value — `DsTextField`** (rule 5). The text is the one parameter that
changes on every keystroke, so it is a `State<T>` read where it is drawn; the label, `enabled` and the
error change rarely and are plain. State first, then config, then the callback, as in
[components](components.md) rule 3.

```kotlin
@Composable
fun DsTextField(
    text: State<String>,
    label: String,
    onChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    error: String? = null,
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(DsTheme.dimens.dp4),
    ) {
        DsText(
            text = label,
            color = DsTheme.colors.content02,
        )
        BasicTextField(
            value = text.value,
            onValueChange = onChange,
            enabled = enabled,
            textStyle = DsTheme.typography.body.copy(color = DsTheme.colors.content01),
            cursorBrush = SolidColor(DsTheme.colors.accent),
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    color = DsTheme.colors.surfaceSunken,
                    shape = DsTheme.rounding.radiusMd,
                )
                .border(
                    width = DsTheme.stroke.hairline,
                    color = DsTheme.colors.borderSubtle,
                    shape = DsTheme.rounding.radiusMd,
                )
                .padding(DsTheme.dimens.dp12),
        )
        if (error != null) {
            DsText(
                text = error,
                color = DsTheme.colors.error,
            )
        }
    }
}
```

**The feature side — where the split pays** ([components](components.md)). The feature component never
reads its own state's `.value` for the text: it passes the derived `State<String>` on, so a keystroke
recomposes `DsTextField` and not `LoginUsernameInput`. The plain `error` is read through its own
`select`, so the feature component recomposes only when the error changes. Reading
`state.value.error` directly would subscribe it to every keystroke.

```kotlin
@Composable
internal fun LoginUsernameInput(
    state: State<LoginUsernameInputState>,
    onChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val error = state.select { it.error }

    DsTextField(
        text = state.select { it.value },
        label = stringResource(Res.string.login_username),
        onChange = onChange,
        modifier = modifier,
        error = error.value,
    )
}
```

**Icons** (rule 8). The typed accessor names one icon, so the shrinker keeps one; a lookup by name
names all of them.

```kotlin
DsIcon(icon = MaterialSymbols.Rounded.Home)            // right: one icon reachable
DsIcon(icon = RoundedIconRegistry.byName(iconName))    // wrong: every Rounded icon reachable (+39 MB on iOS)
```

**Material copied** (rule 2). The header says where it came from and what changed.

```kotlin
/*
 * Adapted from androidx.compose.material3.pulltorefresh.PullToRefreshState (material3 1.4.0).
 * Copyright 2023 The Android Open Source Project, Apache License 2.0.
 * Changes: colours, sizes and durations read from DsTheme; the Material indicator replaced by DsLoader.
 */
```

## Scenarios considered

- **`State<T>` for every changing parameter (Act2Act's `DsButton(enabled: State<Boolean>)`).** Lost:
  `enabled` and `selected` change rarely, so the read buys nothing, and every static call site pays a
  `stateOf(x)` that ties the design system to a presentation module for that helper.
- **A feature-level wrapper that reads `.value` and passes a plain value.** Lost: for a frequent
  change the wrapper recomposes on each one and passes it on, so the saving is only as large as the
  wrapper is small, and a draw-phase read is out of its reach.
- **`() -> T` instead of `State<T>` for the frequent ones.** Equivalent in cost (both defer the read);
  `State<T>` won because the feature layer already speaks it ([components](components.md) rule 4).
- **Promoting a feature's component into the design system when a second feature uses it.** Lost:
  product meaning would enter the design system. The feature publishes it through its `api`.
- **Material sealed behind `implementation` and wrapped (the knowledge note's zero-Material policy).**
  Lost: the owner takes no Material dependency at all; what is needed is copied.
- **A global minimum touch target (`DsTarget`).** Lost: a chip is small by design.

## Where it is applied

No kit has a design-system module yet; the rule is for apps. Against the three Compose design systems
read on 2026-10-12: ArenaGo and Act2Act import `androidx.compose.material*` (13 and 11 files; Act2Act
also `material-icons-extended`); Act2Act takes `State<T>` for `enabled`, `isSelected`, `isVisible`
and depends on `common.presentation` for `stateOf`, and carries `RoundedIconRegistry` (a name lookup
over the whole Rounded set, 8 000 generated lines, called nowhere — rule 8 forbids it); DropNote
imports no Material and takes its icons as per-icon drawables, which rule 8 does not ask for.

## Checked by

Review (`conventions-review`). Mechanical: `grep -rn "androidx.compose.material" core/designsystem/ features/`
finds a rule 2 breach; a Material artifact in a design-system module's build file is the same finding.
