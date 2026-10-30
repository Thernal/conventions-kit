# Kotlin features

**Decided:** 2026-10-30 — Kotlin 2.4 moved two conventions into the compiler, each at a cost its release
notes do not state

## Rule

1. **A function called for its value is marked must-use.** A file whose functions return `Result`, a
   sealed outcome or a `Flow` declares `@file:MustUseReturnValues` (a class or an interface may carry
   `@MustUseReturnValues` instead; an override inherits it). Every build compiles with
   `-Xreturn-value-checker=check`, so a call that drops the value is a compiler warning.
2. **A value is dropped on purpose at the call site**, written `val _ = save()`, never by leaving the
   function unmarked. A function whose result most callers ignore is `@IgnorableReturnValue`. A chain
   ending in `.onSuccess { }` or `.onFailure { }` is a use: the standard library marks both ignorable.
3. **A backing field replaces the `mutableX` / `x` pair only where the property is read inside its own
   module** — a screen's ViewModel, an `internal` class. A public declaration in an `api` module, an
   `override` of an `api` interface and a store other features collect keep the pair and
   `asStateFlow()`.

## Why

A dropped `Result` is an error nobody sees: `safeCall { repository.save(draft) }` as a statement
compiles, reports the failure to the crash reporter and tells the screen nothing. Before 2.4 only a
reviewer could notice. The checker is off unless the build turns it on (`disable` is its default in
2.4), and in `check` mode it covers the standard library and what the code marks — hence both halves of
rule 1.

The backing field is one property instead of two:

```kotlin
// before
private val mutableState = MutableStateFlow(DraftState())
val state: StateFlow<DraftState> = mutableState.asStateFlow()

// after
val state: StateFlow<DraftState>
    field = MutableStateFlow(DraftState())
```

but the property now returns the field itself. Every collector holds the `MutableStateFlow`, and
`(viewModel.state as MutableStateFlow).value = …` writes to it. `asStateFlow()` returned a read-only
wrapper no cast gets through, and a backing field cannot return one, since it forbids a custom getter.
Inside one module the cast is a theoretical risk; across a module boundary the read-only object is the
contract.

## Scenarios considered

- **`-Xreturn-value-checker=full`** — every function in the project becomes must-use. Rejected for now:
  a builder or a `MutableMap.put` dropped as a statement would warn everywhere, and the warnings that
  matter would drown.
- **Detekt `IgnoredReturnValue` with `kotlin.Result` in `returnValueTypes`** — it fails the build, which
  a warning does not. Rejected: `result.onSuccess { }.onFailure { }` returns the `Result` again, and
  Detekt reads the type, not the standard library's marks, so the most common way of handling one
  would be a finding.
- **Swift export's `sealedType()`** — Kotlin 2.4.20 maps a sealed hierarchy to a Swift enum, so a state
  added in Kotlin breaks the iOS `switch` instead of falling into `default`. Not adopted: Swift export
  is Alpha in 2.4 and Beta in 2.5. Decided again when it is Stable, or when an app's iOS code switches
  over a Kotlin sealed state.

## Where it is applied

arch-kit's `safeCall`, `runSafeCall` and `safeCallFlow` and its three use-case shapes; the
`-Xreturn-value-checker=check` flag in the convention plugins every kit builds with and in build-kit's.

## Checked by

The compiler, for rule 1's dropped values; review for an unmarked function, a `@Suppress` used
in place of `val _ =`, and rule 3 — `code-review` greps for a backing field in an `api` module.
