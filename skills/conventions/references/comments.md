# Comments

## Rule

1. **No comment is the default.** A comment stays when it holds a number or a unit, a constraint, a
   trap (what breaks if someone simplifies the code), a rule code (`BR-22`) or a "because" — something the
   code cannot say. With none of them it is deleted. Not every file needs a comment, and most do not.
2. **Self-explanatory code gets no comment.** If a developer who knows the language and the libraries
   understands the code from its names and types, and its effect shows where it is written, it is not
   commented. Deleted on sight:
   - a comment that restates the code, the platform or the callee's own documentation;
   - a KDoc that repeats its declaration's name or turns it into a sentence (`/** Corner shapes. */` on
     `DsRounding`, `/** The introduction is done. */` on `Finished`);
   - a KDoc on an enum entry, a `data object`, an intent, an effect or a state field whose name says it;
   - a KDoc that describes what another class does (an effect that "is remembered", a button that "opens
     the list");
   - a `//` line that narrates the statement under it;
   - a pointer to a design file's selectors (`.fld__box--code`).
3. **A comment never says where its subject is used.** Callers change and the comment does not; the
   IDE finds them. A token, a component or a function documents what it is, not who needed it.
4. **Short.** One or two lines; a KDoc of more than a few lines is the exception that a real trap
   earns. The history of a decision — what was tried and rejected — goes to the commit message or the
   docs, not the code.
5. **A capability without a common usage pattern** gets a short usage comment on its `api` surface
   only.
6. **A stale comment is fixed or deleted with the code it describes.**
7. **The test.** Before a comment goes in, finish the sentence "Without this, a reader would wrongly …".
   If it cannot be finished, there is no comment. A KDoc on every member of a sealed type, an enum or a
   state class fails the test by construction.

## Why

A comment is read as a warning: when most of them say nothing, the one that matters is skipped. Code
that needs no comment is cheaper to keep true than code and a comment. An agent that documents every
declaration trains the reader to skip all of them, so the default is none and a comment has to earn its
place.

## Example

```kotlin
// No — the name says it, and the second line names a caller
/** Border widths. The text field's outline uses [field]. */
class DsStroke(val hairline: Dp, val field: Dp)

// No — the name turned into a sentence, and "remembered" is another class's work
sealed interface OnboardingEffect {
    /** The introduction is done and remembered. */
    data object Finished : OnboardingEffect
}

// Yes — the code cannot say why
/** The spacing also follows the last digit; the same indent before the first keeps them centred. */

// Yes — a constraint and where it comes from
/** The MVP is Azerbaijani only (BR-22), so the code is fixed until the language list is settled. */
private const val CURRENT_LANGUAGE_CODE = "AZ"
```

## Checked by

Review. `conventions-review` lists every comment of the diff (its step 3) and gives each a verdict by
rules 2 and 7 — keep, or delete — so the rule is not left to a reader's eye.
