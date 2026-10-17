# Insets and the keyboard

**Decided:** 2026-10-17, by the owner · **Applies to:** every app built on the kits

## Rule

1. **Every inset is applied once.** A screen pads each inset (status bar, navigation bar, keyboard) in
   one place; a parent and a child that both apply the same inset add up. The pieces that own an inset
   say so: `DsAppBar` the status bar, `DsTabBar` and `DsFooter` the navigation bar, a bottom sheet's
   surface the keyboard.
2. **The keyboard has one owner per screen.** If the screen has a bottom bar (a message composer, a
   footer with a button), the bar owns it: `imePadding()`, then `navigationBarsPadding()` — in that order, so
   the navigation bar adds nothing while the keyboard is up (`DsFooter` does both). The content above the
   bar is a `weight(1f)` child and shrinks by itself; it adds nothing. If there is no bottom bar, the
   scrolling viewport owns it, before `verticalScroll`:
   `Modifier.weight(1f).imePadding().verticalScroll(...).navigationBarsPadding().padding(...)`. A screen
   that gives the keyboard to the bar *and* to the viewport shrinks the visible area twice (a contact form
   with a send footer showed a strip of two fields and white space below).
3. **Android: the activity is `adjustResize`.** `android:windowSoftInputMode="adjustResize"` on every
   launcher activity. Without it the system pans the whole window up to keep the focused field in view
   *and* `imePadding()` lifts the bar again: the header is cut off and a gap the height of the keyboard
   stays between the bar and the keyboard.
4. **iOS: Compose does not lift the view itself.** The view controller is
   `ComposeUIViewController(configure = { onFocusBehavior = OnFocusBehavior.DoNothing })`. The default
   (`FocusableAboveKeyboard`) moves the content above the keyboard and `imePadding()` moves it again.
5. **A bottom sheet pads the keyboard in its own surface** (`BottomSheetStyle.isImePadded`) and the
   content of the sheet adds no `imePadding()`.

## Why

The double padding shows only with a field low on the screen (a chat composer), so it passes a review
that never opens the keyboard there. The two fixes are platform settings, not code in a screen, and are
easy to leave out of a new app.

## Checked by

Review: open the keyboard on a screen with a bottom field, on both platforms. `conventions-review`
greps the manifests for `adjustResize` and the iOS entry points for `onFocusBehavior`.
