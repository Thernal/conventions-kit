# Navigation

**Decided:** 2026-10-07

## Rule

1. **Everything about navigation lives in `presentation/navigation/`** — routes, the graph,
   navigation sheets — the same in `api` and `impl`. `api` publishes the routes others may open.
2. **The graph is `<Feature>GraphProvider`** (it implements nav-kit's `NavigationGraphProvider`).
3. **Routes** are a `sealed interface <Feature>Route : NavKey` with `@Immutable` cases.
4. **Routes do not override `toString`.** Navigation3 keys an entry's content by `toString()` by
   default, so two `data object Main` in different features would share a key and the transition
   would not run; nav-kit sets each entry's `contentKey` from the route's full name (and a
   `data class` route's arguments) instead.
5. **A sheet or dialog with its own state or its own navigation is a destination** (a `…View`);
   one driven by the screen's state is a component of the screen ([presentation-structure](presentation-structure.md) rule 7).

## Checked by

nav-kit (rule 4); review.
