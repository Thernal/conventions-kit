# conventions-kit

The rules every Thernal kit and every app built on the kits follows — package names, file shape,
names, presentation structure, components, previews, data and domain, navigation, DI modules,
strings, Compose performance, comments, tests, documentation, kit styling, dependencies — each with
its reason, an example and how it is checked. They reach agents as two skills; the few that a tool can
check are Detekt rules, kept here and synced into every kit. A third skill, `design-system`, is the
procedure for building an app's design system by those rules — screen by screen for one developer, in
one pass for a team.

## Documentation

| Read | For |
|---|---|
| [`docs/README.md`](docs/README.md) | the rules, one file each, and how a rule is added or changed |
| [`skills/conventions`](skills/conventions/SKILL.md) | the rules for an agent writing code in a project on the kits |
| [`skills/conventions-review`](skills/conventions-review/SKILL.md) | reviewing a diff, a module or a kit against them |
| [`skills/design-system`](skills/design-system/SKILL.md) | building or growing an app's `designsystem/` — the two modes and the shared steps |

## What is here

| Path | Holds |
|---|---|
| `skills/conventions/references/` | the rules — the one source; `docs/README.md` indexes them |
| `skills/conventions-review/` | the review procedure |
| `skills/design-system/` | the design-system procedure and its two modes (`references/grow.md`, `references/upfront.md`) |
| `build-logic/detekt-rules/` | the custom Detekt rules and their tests — the master copy |
| `build-logic/convention/` | the trimmed convention plugins every kit builds with — the master copy |
| `scripts/sync-kits.py` | renders `build-logic/` into every sibling kit, renamed; `--check` reports drift |
| `scripts/check-namespaces.py` | every module's packages under its namespace, in any kit or app |
| `config/detekt/detekt.yml` | the Detekt configuration the kits share |

## Installing in an app

```sh
skillctl.sh kit install conventions-kit
```

copies the three skills into the app's skills directory and records them in `kits.lock`; `kit update`
brings later rule changes. Nothing else is copied: the app's Detekt rules come from build-kit. Add three
lines to the app's `AGENTS.md` (`kit.yml` → `requires`):

```markdown
- Kotlin and Compose code here follows the `conventions` skill (conventions-kit); load it before writing code.
- A review against those rules is the `conventions-review` skill.
- A rule is changed in conventions-kit (skill-manager `report`), never in this repository's copy.
```

Without skill-manager: copy `skills/conventions`, `skills/conventions-review` and `skills/design-system`
into the app's skills directory. The `design-system` skill writes one row, `Design system mode`, into the
app's `.agents/workspace.md` on first use.

## Build logic: one master, synced copies

Every kit builds with the same trimmed convention plugins and the same Detekt rules. They are written
here and nowhere else:

```sh
./gradlew check                      # build the plugins, run the rules' tests
scripts/sync-kits.py                 # render build-logic/ into every kit next to this one, renamed
scripts/sync-kits.py --check         # report drift, missing catalog entries, dynamic versions; change nothing
```

The sync renames `io.thernal.conventionskit` to each kit's `package` and `conventionskit` to its `alias`
(`kit.yml`), and writes `build-logic/SYNCED` — a SHA-256 per file. Each kit's `check` runs
`verifyBuildLogic`, which fails, naming the file, when the build logic was edited in the kit instead of
here. build-kit has a build logic of its own and takes only `detekt-rules`.

## Building

Needs JDK 17 (Gradle provisions it). `./gradlew check` builds `build-logic` and runs its tests; there are
no other modules.
