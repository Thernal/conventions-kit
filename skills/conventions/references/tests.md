# Tests

**Decided:** 2026-10-07

## Rule

1. **Test names are backtick sentences**: `` fun `keeps the placement when it fits`() ``. Plain
   words only — Kotlin/Native rejects `,` `.` `:` `;` `/` `<` `>` `[` `]` in a function name, and the
   tests compile for iOS too.
2. **Stubs come from Mokkery** — Kotlin Multiplatform on every target (MockK has no Kotlin/Native,
   and the tests run on the iOS simulator too).
3. **A hand-written `Fake<Contract>` only where it has behaviour** (an in-memory repository), in the
   module's `testing` part, so every module that needs it reuses it.
4. **Every ViewModel has a test, and so does every critical piece of logic below it** — use cases,
   mappers, repositories with logic.

## Checked by

The `conventions` skill and `conventions-review`.
