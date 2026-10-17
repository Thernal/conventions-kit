# Files and names

**Decided:** 2026-10-07

## Rule

1. **One top-level declaration per file**, the file named after it. Types that cannot be used apart
   from their parent may share its file — nested response DTOs, a component's state and callbacks
   classes — and a sealed hierarchy stays together. A screen's UI mappers are grouped by what they
   produce: `<Screen>StateMappers.kt` holds every `State<ScreenState>.to<Component>State()`,
   `<Screen>CallbacksMappers.kt` every `to<Component>Callbacks()`.
2. **One non-preview composable per file**; its previews stay in the same file, after it.
3. **The line limit splits files too.** A composable that outgrows its file becomes a folder:
   `<name>/<Name>.kt` and `<name>/components/` for its parts.
4. **An implementation is `<Interface>Impl`** when it is the one implementation. A name that says how
   it works is kept when that is the point, or when there are several (`SharedFlowEventBus`,
   `MetroViewModelResolver`, `InMemoryCache`). Never a `Default…` prefix.
5. **Names say what is not already said.** No suffix the type repeats (`asStringMap` returning a
   `Map<…, String>`), no abbreviations, English everywhere — code, comments, docs.
6. **No magic values.** A number or string with meaning is a named constant, a resource or a typed
   value; look for an existing holder before adding one.
7. **Constants have a place.**
   - File-private constants: top-level `private const val` at the bottom of the file.
   - Constants several files share: a companion of one chosen file.
   - In a composable file, the component's constants come **before** the component; a preview's come
     **after** the component and before the preview. Component and preview never interleave.
8. **Composables are PascalCase nouns**; design-system components carry the `Ds` prefix.
9. **A dependency is named after its type, in full:** `authRepository: AuthRepository`,
   `keyValueStore: KeyValueStore`, `authSharedRepository: AuthSharedRepository` — never `repository`,
   `source`, `store` or a shortening (`posts: PostRepository`). A class may take several of them, and the name
   says which; a test's mock or fake of one is named the same way.

## Why

- One declaration per file makes a type findable by name and a diff readable; the exceptions are the
  types that would be noise as separate files and can never be used alone.
- `Impl` sorts next to its interface and needs no choice; `Default` and `Impl` side by side in the kits
  made every new class a coin toss.
- The component / preview border keeps what ships apart from what only the IDE renders.

## Example

```kotlin
// PostsResponseDto.kt — the item type cannot be used without the list
@Serializable
data class PostsResponseDto(val posts: List<PostResponseDto> = emptyList())

@Serializable
data class PostResponseDto(val id: String? = null)
```

## Checked by

- Detekt `MatchingDeclarationName` (excluded under `components/`, where the file is named after the
  composable, see [components](components.md)), `MagicNumber` (partly), ktlint formatting.
- The rest: the `conventions` skill and `code-review` — no Detekt rule.
