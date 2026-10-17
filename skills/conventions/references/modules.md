# Modules

**Decided:** 2026-10-17, by the owner · **Applies to:** every app built on the kits

## Rule

1. **In a product with several apps, features are grouped by who uses them:** `features/shared/<name>` for
   what both apps use, `features/client/<name>` and `features/store/<name>` for one app's own. The group is a
   path segment, so it is part of the namespace (`<app>.features.shared.auth.impl`,
   [package-naming](package-naming.md)). A feature one app uses is never under `shared`. **A product with one
   app has no groups:** every feature is `features/<name>` (`<app>.features.auth.impl`); a group is added
   only when a second app arrives, and then every feature moves into one.
2. **A feature is `api` / `impl` / `wiring`, plus `testing` when it has a fake** ([tests](tests.md)
   rule 5). A feature with nothing to publish has no `api` — a dashboard is `impl` + `wiring`.
3. **Dependency direction.** An `impl` may depend on any number of `api` modules — its own, other features',
   core's. An `api` never depends on another feature's `api`. An `impl` never depends on another feature's
   `impl`. An app depends on `wiring` (and on an `api` only for what its own code opens), never on `impl`.
   `testing` depends on its feature's `impl` and `wiring`, never the reverse; an app takes it only for the
   flavors that carry fakes.
4. **An app holds no screen.** `apps/<app>/shared` has the Metro graph, the root composable and the
   ViewModel that owns the root: the back stack and what the data layer feeds every screen (a theme or a
   language the user chose), read through the shared preferences repository. The root composable nests one
   **provider** per thing it gives every screen — for example `LanguageProvider`, `ThemeProvider`,
   `OverlayProvider`, `NavigationProvider`. These are examples, not a required set: an app has the providers it
   needs and adds one when it has something to provide. Each reads a single field of the root state, so one
   change recomposes one provider. A provider provides; none gates the content on a loading flag — a flow
   that never emitted would leave the app blank. The app's tabs are its own `dashboard` feature
   (`features/client/dashboard`, `features/store/dashboard`; `features/dashboard` in a one-app product),
   registered like any other feature's graph.
5. **A rule that spans features belongs to the feature that owns the subject.** Where a signed-out user
   goes is auth's: a nav-kit guard over the session, contributed by auth's `wiring`
   ([navigation](navigation.md) rule 6). Splash and the dashboards register their own destinations. No app
   copies a feature's logic, and no Logic navigates after sign-out — the guard rewrites the stack when the
   session ends.
6. **A repository another feature needs** is a shared repository
   ([data-and-domain](data-and-domain.md) rule 8).

## Why

- Where a feature lives says who may use it, and the namespace says the same. With one app every feature is
  that app's, so a group would say nothing and lengthen every package.
- `api` → `api` chains turn a contract into a dependency graph; an `impl` seeing any `api` costs nothing
  and keeps features independent of each other's internals.
- Two apps that each copy the session logic and the tab shell change twice for every rule.

## Checked by

Review. `code-review` greps the module build files for `api` → `api` and `impl` → `impl` dependencies
and the apps' source sets for screens.
