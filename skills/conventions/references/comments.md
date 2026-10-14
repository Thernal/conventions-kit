# Comments

## Rule

1. **Comment why, not what** — a constraint, a trade-off, business logic that is not obvious.
2. **Self-explanatory code gets no comment.** If a developer who knows the language and the
   libraries understands the code from its names and types, and its effect shows where it is
   written, it is not commented. Deleted on sight: a comment that restates the code, the platform or
   the callee's own documentation; a KDoc that repeats its declaration's name (`/** Corner shapes. */`
   on `DsRounding`); a pointer to a design file's selectors (`.fld__box--code`).
3. **A comment never says where its subject is used.** Callers change and the comment does not; the
   IDE finds them. A token, a component or a function documents what it is, not who needed it.
4. **Short.** One or two lines; a KDoc of more than a few lines is the exception that a real trap
   earns. The history of a decision — what was tried and rejected — goes to the commit message or the
   docs, not the code.
5. **A capability without a common usage pattern** gets a short usage comment on its `api` surface
   only.
6. **A stale comment is fixed or deleted with the code it describes.**

## Why

A comment is read as a warning: when most of them say nothing, the one that matters is skipped. Code
that needs no comment is cheaper to keep true than code and a comment.

## Example

```kotlin
// No — the name says it, and the second line names a caller
/** Border widths. The text field's outline uses [field]. */
class DsStroke(val hairline: Dp, val field: Dp)

// Yes — the code cannot say why
/** The spacing also follows the last digit; the same indent before the first keeps them centred. */
```

## Checked by

Review.
