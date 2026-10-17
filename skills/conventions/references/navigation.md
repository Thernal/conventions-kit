# Navigation

**Decided:** 2026-10-07

## Rule

1. **Everything about navigation lives in `presentation/navigation/`** — routes, the graph,
   navigation sheets — the same in `api` and `impl`. `api` publishes the routes others may open.
2. **The graph is `<Feature>GraphProvider`** (it implements nav-kit's `NavigationGraphProvider`).
3. **Routes.** A route an `api` publishes — one another feature may open — is a
   `sealed interface <Feature>SharedRoute : Route` (or a `data object`), `@Immutable`. A route used inside
   one `impl` is `<Feature>Route`, `internal`, and never leaves the module. The name says which of the two
   it is; there is no `…StepRoute`.
4. **Routes do not override `toString`.** Navigation3 keys an entry's content by `toString()` by
   default, so two `data object Main` in different features would share a key and the transition
   would not run; nav-kit sets each entry's `contentKey` from the route's full name (and a
   `data class` route's arguments) instead.
5. **A sheet or dialog with its own state or its own navigation is a destination** (a `…View`);
   one driven by the screen's state is a component of the screen ([presentation-structure](presentation-structure.md) rule 7).
6. **Access rules are guards, contributed by the feature that owns the subject.** Where a signed-out user
   goes is auth's `AuthGuard`, a `NavigationGuard` over the session contributed `@IntoSet` from auth's
   `wiring`; it holds the public routes (splash, sign-in) and sends every other route to sign-in, and it
   revalidates every host when the session changes. A Logic does not navigate after sign-out and an app's
   root does not repeat the rule.
7. **A screen that is only a start is a graph entry of its own feature.** Splash registers its
   `SplashSharedRoute` and moves on with `replaceAll(HomeSharedRoute)`; the root composable registers
   nothing but the providers.

8. **A dashboard owns a nested host.** Its tabs are `<Feature>Route`s on a `NavigationHost` of their own, the
   stack held by the dashboard's Logic (selecting a tab replaces it; `onBackStackChange` is a plain setter).
   Only the tab bar and the host read the stack, each through `select`. A tab's ViewModels live with the
   dashboard, not with the tab's entry: inside the host's entries a `TabEntryScope(outer)` gives the tab the
   host's mount point as its `ViewModelStoreOwner` (`LocalHostViewModelStoreOwner`) and the **outer**
   navigator, so a tab keeps its state while another is shown and opens details above the bar. The nested host
   has a `fallback` entry for a guard rewriting its stack on sign-out.

## Checked by

nav-kit (rule 4); review.
