# Kit styling

**Decided:** 2026-10-07 · **First applied:** overlay-kit `cc96716`

## Rule

1. **A kit that draws UI owns behaviour, never the look.** Placement, gestures, back, focus and
   lifecycles are the kit's; colours, shapes, spacing, text styles and durations are the app's.
2. **Every look is a field of a style value** (`DialogStyle`, `ImageCropperStyle`, …) with neutral
   defaults, read from a theme local (`OverlayTheme.styles`). Nothing visual is hard-coded in `impl` —
   a value only `impl` knows is a look no app can change.
3. **The app maps its design system once**, in one file of its own design-system module
   (`core/designsystem/…/overlay/AppOverlayStyles.kt`), and installs it at the root inside its theme:
   `AppTheme { OverlayTheme(styles = appOverlayStyles()) { … } }`. A one-off look is a `style =` at the
   call site.
4. **Kit code is never edited to restyle.** The defaults are fallbacks for previews, tests and the first
   build — not a design.
5. **A kit ships no design system in `code`.** Its example lives in `sample/designsystem` (tokens + the
   mapping file), which nothing copies; the kit's README, skill and `kit.yml` `requires` point at it.
6. **Map looks, keep behaviour.** Thresholds, auto-dismiss delays and insets keep the kit's defaults
   unless the app means to change how the component works.

## Why

A kit is merged into every app on update. A look the kit decided — or a design system shipped as copied
code — would be merged into each app's own design too, and either drift from it or fight it on every
update. One app-owned mapping file keeps the app's look entirely the app's, while the kit stays free to
change behaviour underneath.

## Example

overlay-kit: `sample/designsystem/…/SampleTheme.kt` (tokens) and
`…/overlay/SampleOverlayStyles.kt` (`@Composable fun sampleOverlayStyles(): OverlayStyles`); the sample
switches between the kit's neutral defaults and that mapping.

## Checked by

The kit's `requires` (shown at install), the kit's skill (an agent writes the mapping when it is
missing and never restyles kit code), review — a hard-coded colour, size or duration in `impl` is a
finding.
