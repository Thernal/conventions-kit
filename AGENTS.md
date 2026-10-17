# conventions-kit — rules for agents

conventions-kit holds the rules every Thernal kit and every app on the kits follows, and the build logic
every kit builds with. Apps take its two skills with `skillctl.sh kit install conventions-kit` (the
skill-manager skill, `Thernal/knowledge`); kits take its build logic through `scripts/sync-kits.py`.
A change here reaches every kit and every app, so it is made deliberately.

## Delivering a change

- **Nothing reaches `main` without a green `./gradlew check`** (the convention plugins compile, the
  Detekt rules' tests pass) **and `scripts/sync-kits.py --check`** — no kit drifted, no catalog lacks an
  alias the build logic reads. Check Gradle's own exit code, never through a pipe.
- A change to `build-logic/` is synced into every kit in the same piece of work, and each kit is built
  (`verifyBuildLogic`, compile, Detekt) and committed with it. A rule change that some kit breaks is
  fixed in that kit, or the rule names the exception — never left for later.
- Git conventions, attribution (off here) and branches: `.agents/workspace.md`.

## Writing here

- **Build logic is edited here only.** In a kit it is generated; `verifyBuildLogic` fails on a hand edit.
- **Rename-safe.** The sync renames `io.thernal.conventionskit` to a kit's `package` and `conventionskit`
  to its `alias`. Write them whole; keep everything kit-specific out of the build logic (an example path
  in a KDoc included) — a kit that needs something different adds it in its own module build files.
- **A catalog alias the build logic reads** must exist in every kit's catalog; `--check` lists the
  missing ones (`does not compile without it` blocks, `read when a module applies…` warns).
- **The rules** are `skills/conventions/references/*.md`, one file per topic; `docs/README.md` indexes
  them and says how a rule is written. A new rule gets a row there and in `skills/conventions/SKILL.md`.
- **No new Detekt rule** for a convention that review can carry; Detekt keeps what it checks without
  false positives.

## Documentation

| File | Holds | Update when |
|---|---|---|
| `README.md` | what the kit is, its layout, install, the sync | anything a user of the kit sees changes |
| `docs/README.md` | the index of the rules and how one is written | a rule is added, renamed or its check changes |
| `skills/conventions` | the rules for an agent; `references/` are the rules | a rule changes |
| `skills/code-review` | how a review is done: the rules pass and the correctness pass | the procedure, the mechanical checks or the correctness list change |
| `skills/screen-build` | the order of work for a screen's UI: the dynamics table, from the design or tidy | the components, state-read or design-source rules change |
| `skills/design-system` | how an app's design system is built or grown, in its two modes | the design-system rule changes, or a step of either mode does |
| `kit.yml` | what an app takes and must provide | a skill or a requirement changes |

The skills' frontmatter has to load in Claude Code and in Codex alike: a `description` of at most 1024
characters (600–900 in practice), valid YAML, only `name` and `description`.

Docs are read in place by apps (`knowledgectl.sh kit conventions-kit read <path>`), never copied. When
`kit.yml` or `README.md` changes, the knowledge card `kits/conventions-kit.md` in `Thernal/knowledge`
needs its `card_sha` bumped (`scripts/check-corpus.py --kits` says so).
