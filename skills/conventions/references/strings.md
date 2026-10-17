# Strings

**Decided:** 2026-10-07

## Rule

1. **User-visible text travels as `UiString`**, never a raw `String`; a ViewModel never resolves it.
2. **Keys are `snake_case`, prefixed** by feature (`report_submit_success`) or by kind for shared
   ones (`common_cancel`, `error_network`).
3. **Shared strings live in one module**; a feature's own strings in its own module's `strings.xml`
   (`composeResources/values/` in a multiplatform module).

4. **A feature's text is in that feature's module.** The shared module holds only text more than one feature
   shows (`common_back`, `common_retry`). A tab label belongs to the dashboard, a store status to the profile
   feature.
5. **An effect carries a `UiString`**, never a `StringResource` or a resolved `String`
   ([presentation-structure](presentation-structure.md) rule 2); the View resolves it with
   `load(LocalStringLookup.current)` or `resolve()`.
6. **Dates, times and ratings are shown from a model, not stored as text.** A relative time is a model
   (`Minutes(count)`, `Yesterday`) and its words are resources; a domain model and a data source never hold a
   preformatted label.

## Checked by

Review.
