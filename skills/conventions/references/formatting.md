# Formatting

## Rule

`.editorconfig`: UTF-8, LF, 4 spaces, 120 columns, parameters chopped down, trailing commas on
declarations and calls, no wildcard imports. Block bodies with `return` (`ExpressionBodyNotAllowed`),
one constructor parameter per line (`MultilineConstructorRequired`), named arguments for calls with
several arguments (`NamedArguments`), no unchecked index access (`UnsafeCollectionIndexAccess`).

## Checked by

ktlint and the custom Detekt rules — conventions-kit's `build-logic/detekt-rules`, synced into every kit
and shipped to apps by build-kit.
