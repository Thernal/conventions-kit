# Tests

**Decided:** 2026-10-07

## Rule

1. **Test names are backtick sentences**: `` fun `keeps the placement when it fits`() ``. Plain
   words only — Kotlin/Native rejects `,` `.` `:` `;` `/` `<` `>` `[` `]` in a function name, and the
   tests compile for iOS too.
2. **Stubs come from Mokkery** — Kotlin Multiplatform on every target (MockK has no Kotlin/Native,
   and the tests run on the iOS simulator too). The module applies `alias(libs.plugins.mokkery)`.
   Stub an interface at the boundary the unit talks to (a Logic's repository, `SessionManager`):

   ```kotlin
   private val repository = mock<SupportRepository> {
       everySuspend { send(any()) } returns Result.success(Unit)
   }
   // a flow or a non-suspending call: every { conversations() } returns flowOf(Result.success(list))
   verifySuspend { repository.send(request) }
   verifySuspend(VerifyMode.not) { repository.send(any()) }
   ```

   Imports: `dev.mokkery.mock`, `every`, `everySuspend`, `dev.mokkery.answering.returns`,
   `dev.mokkery.matcher.any`, `dev.mokkery.verify.VerifyMode`, `verifySuspend`. Inside the `mock { … }`
   block a name resolves to the mock's member first, so a test property with the same name
   (`state`) is shadowed — give such a field another name (`sessionState`). A failing stub is
   `returns Result.failure(Failure(message = "offline"))`; a second behaviour is a second `mock`, not a flag.
3. **A hand-written `Fake<Contract>` only where it has behaviour** (an in-memory repository), in the
   module's `testing` part, so every module that needs it reuses it.
4. **Every ViewModel has a test, and so does every critical piece of logic below it** — use cases,
   mappers, repositories with logic. `make test-ios` compiles and runs them on the iOS simulator too: it
   is part of done, because a name or an API that only the common tests accept fails there.
5. **A feature's fake sits behind its real data layer.** The whole of `data/` runs for real (DTO, mapper,
   repository); only the `…RemoteDataSource` is replaced, by `Fake<X>RemoteDataSource` in
   `features/<group>/<name>/testing`. The fake returns DTOs, keeps the state a screen would see change
   (what was read, what was sent) and is `@SingleIn` when it must. A container in the `testing` module,
   `@ContributesTo(AppScope::class, replaces = [<X>SourceProvidersModule::class])`, binds it
   ([di-modules](di-modules.md) rule 5), and `apps/*/shared` takes the module with
   `flavorImplementation("dev", dependencyNotation = …)`: staging and production never carry a fake
   (the dex of their builds has no `Fake…` class). A fake of a repository is the exception, for a backend
   whose contract is not settled; production then binds an `Unavailable<X>Repository` whose every call fails.
6. **Data sources and repositories are tested through `mockApiClient`**, never a real server: the test
   asserts the path, the verb and the body, and the mapped result. JSON in a test is a string — `String.format`
   does not exist in common code; build variants with a function or `replace`.

## Checked by

The `conventions` skill and `conventions-review`.
