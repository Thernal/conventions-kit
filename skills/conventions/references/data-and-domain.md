# Data and domain

**Decided:** 2026-10-07

## Rule

1. **Network models** are `<X>RequestDto` / `<X>ResponseDto` in `data/model/`: `@Serializable`, every
   field `@SerialName`, nullable with a default, so a partial payload does not fail.
2. **Domain models have plain names** in `domain/model/`: `Post`, not `PostEntity` (`Entity` collides
   with Room's).
3. **Data sources by where the data lives**: `<X>RemoteDataSource` (HTTP), `<X>LocalDataSource`
   (disk, database, preferences), `<X>RuntimeDataSource` (state shared while the app runs — the
   session, a cart). No `…Manager`, no `StateFlow` held by a repository. A remote data source is an
   interface with `<X>RemoteDataSourceImpl` (the test seam, rule 7); its fake is
   `Fake<X>RemoteDataSource` ([tests](tests.md) rule 5).
4. **Mappers are pure extension functions** `to<Target>()` in `data/mapper/`, one file per source
   type (`LoginRequestMapper.kt`).
5. **A repository is thin**: call the source, unwrap, map.
6. **A use case only when it combines several repositories**; one that forwards a single repository
   call is deleted.
7. **Inject interfaces, not classes** — and an interface only at an ownership or a test seam, never
   to mirror one stateless class.

8. **A repository another feature needs is shared through its `api`.** `api` has
   `<Feature>SharedRepository`; `impl/domain` has `<Feature>Repository : <Feature>SharedRepository` (its own
   methods, if any); `impl/data/repository` has `<Feature>RepositoryImpl : <Feature>Repository`. DI binds
   the shared interface from the same instance ([di-modules](di-modules.md) rule 5). Another feature
   reads the shared interface only.
9. **Domain models are pure Kotlin.** No `@Immutable` or `@Stable`, no Compose, no
   `kotlinx.collections.immutable`, no default values, no display logic (initials, formatted dates and
   ratings, concatenated names), no design-system or platform type (a domain `AppTheme`, never the
   design system's `ThemeMode`). The presentation layer maps them to its own models, in the Logic,
   with mappers in `view/<screen>/mapper/`; a component never takes a domain type.
10. **`data/` has the same four folders in every feature:** `model/` (`…Dto`), `mapper/`, `source/`,
    `repository/`. A feature with no network has the folders it needs, not a flat `data/`. Fake data is
    never an object in `data/` read by a Logic or by previews: it is a fake of the data source, behind the
    real repository ([tests](tests.md) rule 5).

## Checked by

The `conventions` skill and `conventions-review`.
