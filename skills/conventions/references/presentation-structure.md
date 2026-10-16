# Presentation structure

**Decided:** 2026-10-07

## Rule

A feature's `presentation` package (in `impl`; `api` holds only what it publishes):

```
presentation/
  navigation/              routes, <Feature>GraphProvider, navigation sheets   → [navigation](navigation.md)
  model/                   feature-level UI models, navigation argument classes
  mapper/                  mappers several screens use
  components/              internal components shared by the module's screens (no screen prefix)
  preview/                 PreviewParameterProviders shared in the module, if any
  view/<screen>/
    <Screen>View.kt        gets the ViewModel, builds the Callbacks, wires navigation
    <Screen>Content.kt     <Screen>Content(state, onIntent, callbacks) — pure, previewable
    <Screen>ViewModel.kt
    contract/              <Screen>State, <Screen>Intent, <Screen>Action (with an ActionLogic),
                           <Screen>Effect (only if needed), <Screen>Callbacks
    model/                 screen-level UI models
    mapper/                <Screen>StateMappers.kt, <Screen>CallbacksMappers.kt;
                           domain → UI model for this screen
    components/<Name>.kt   a component: its state, its callbacks, its composable → [components](components.md)
    components/<name>/     a large one: <Name>.kt + components/
    preview/               this screen's PreviewParameterProviders, if any
```

1. **A screen is a package** `view/<screen>/`, lowercase, no separators (`createaccount`).
2. **The contract is a package**, one file per type. `<Screen>Action` is the `internal` action type of
   an `ActionLogic`, kept with the State, Intent and Effect that `ActionLogic<S, I, A, E>` names.
   `<Screen>Callbacks` is one `@Immutable data class` of the screen's callbacks — navigation, nothing
   that changes state. **Action is the logic's word and Callbacks the UI's**; neither is ever called
   `Actions`. `<Screen>Effect` exists only when `NavEffect` and `MessageEffect` are not enough, and
   says why.
3. **UI models are not contract.** Display models and navigation argument classes go to `model/` —
   the screen's, or the feature's when several screens use them.
4. **`<Screen>Content` never sees the ViewModel**: `(state, onIntent, callbacks)`; the parameter is
   `onIntent`.
5. **One ViewModel per screen** holds everything on it. A component gets its own ViewModel only when
   it is self-contained and reused — a post card with its own like, share and bookmark — and is then a
   `<Name>View` with a `<Name>ViewModel`, created with `componentViewModel` (or
   `assistedComponentViewModel` when it takes the item). That ViewModel is scoped to the component
   (`rememberViewModelStoreOwner`): created when it enters composition, cleared when it leaves, kept
   across a rotation. An item scrolled out of a lazy list gets a fresh one when it comes back; state
   that must survive scrolling belongs to the screen's ViewModel, or to a keyed owner
   (`rememberViewModelStoreOwner(key, provider)`) held by the list.
6. **`…View`, never `…Screen`**: a component with a ViewModel is a `…View` too, and is not a screen.
7. **Sheets and dialogs.** One with its own state or its own navigation (a multi-step report flow)
   is a navigation destination, a `…View` under `navigation/` + `view/`. One driven by the screen's
   state that acts on the screen directly (an image picker sheet) is a component of that screen.
   App-level overlays (overlay-kit) are called through their api.
8. **No preview data shared between screens.** `PreviewParameterProvider`s, when written, live in
   `preview/` of the module or of the screen.
9. **Only an intent handler changes state**; a sheet's visibility is state set by an intent, never a
   local `remember { mutableStateOf(…) }`. No network or database call from a composable.

## Why

- Each folder answers one question — where is this screen's contract, its models, its parts — so
  nothing is placed by taste.
- Contract and models apart: a contract is what the screen and its ViewModel agree on; a model is
  data that also travels (an argument, a list item) and outlives one screen's contract.
- Callbacks in one class keep `Content`'s signature the same on every screen and its previews short.
- An action is what the logic does about an intent, so it sits with the types its `ActionLogic` names;
  a callback is what the UI asks of its parent. One word each, so `LoginAction` and `LoginActions`
  never stand side by side.

## Checked by

Review; Detekt `LayerPackage*` keeps all of it inside `presentation`.
