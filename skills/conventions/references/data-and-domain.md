# Data and domain

**Decided:** 2026-10-07

## Rule

1. **Network models** are `<X>RequestDto` / `<X>ResponseDto` in `data/model/`: `@Serializable`, every
   field `@SerialName`, nullable with a default, so a partial payload does not fail.
2. **Domain models have plain names** in `domain/model/`: `Post`, not `PostEntity` (`Entity` collides
   with Room's).
3. **Data sources by where the data lives**: `<X>RemoteDataSource` (HTTP), `<X>LocalDataSource`
   (disk, database, preferences), `<X>RuntimeDataSource` (state shared while the app runs — the
   session, a cart). No `…Manager`, no `StateFlow` held by a repository.
4. **Mappers are pure extension functions** `to<Target>()` in `data/mapper/`, one file per source
   type (`LoginRequestMapper.kt`).
5. **A repository is thin**: call the source, unwrap, map.
6. **A use case only when it combines several repositories**; one that forwards a single repository
   call is deleted.
7. **Inject interfaces, not classes** — and an interface only at an ownership or a test seam, never
   to mirror one stateless class.

## Checked by

The `conventions` skill and `conventions-review`.
