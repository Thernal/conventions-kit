# A repository's Result is must-use

Skill: conventions
Fixture: an app on build-kit and arch-kit with a `features/profile` feature that has a
`ProfileRemoteDataSource` and no repository yet

## Prompt
Add a ProfileRepository to the profile feature with a save(profile) that calls the remote data source.

## Passes when
- `grep -rn MustUseReturnValues features/profile` finds the repository's interface or its file
- `save` returns `Result<Unit>`, and no caller written in the same change drops it bare
  (a `val _ =` or an `.onSuccess` / `.onFailure` chain is a use)
- the implementation is `ProfileRepositoryImpl` in `impl/data/repository/`

## Runs
| Date | Model | Without the skill | With it |
|---|---|---|---|
