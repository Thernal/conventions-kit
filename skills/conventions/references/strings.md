# Strings

**Decided:** 2026-10-07

## Rule

1. **User-visible text travels as `UiString`**, never a raw `String`; a ViewModel never resolves it.
2. **Keys are `snake_case`, prefixed** by feature (`report_submit_success`) or by kind for shared
   ones (`common_cancel`, `error_network`).
3. **Shared strings live in one module**; a feature's own strings in its own module's `strings.xml`
   (`composeResources/values/` in a multiplatform module).

## Checked by

Review.
