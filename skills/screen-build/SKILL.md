---
name: screen-build
description: How a screen's UI is written in an app on the Thernal kits, in one of two modes — build it from the design (a design-kit prototype, Figma through figma-bridge, or screenshots), or, when the working tree has a Content the developer changed, tidy it (components, state reads, tokens, strings, TODO(agent) comments). Both start from the screen's dynamics table — each element's source (static, navigation argument, state field and its trigger, remote data) from the design and the spec or API contract — and draw the component boundaries from it. Use it for "build this screen", "write the onboarding screen from the design", "tidy this Content", "extract the components", "ekranı yaz", "ekranı dizayndan qur", "Content-i səliqəyə sal", "komponentlərə ayır". Not for a Ds component alone (design-system) or a ViewModel's logic alone (arch-kit).
---

# Writing a screen

The rules the code follows are the `conventions` skill's (components rules 4 and 6, compose-performance rules 5
and 6) and `arch-kit`'s; this skill is the order of work.

| Mode | The developer | The agent |
|---|---|---|
| **From the design** | names the screen | reads the design, builds the whole UI |
| **Tidy** | assembles the UI in `<Screen>Content` — layout, literals, `TODO(agent)` comments | keeps the layout and the look, restructures it by the rules |

**Which mode, when the developer does not say:** the working tree decides, never a question.

```sh
git status --short -- features | grep -E 'Content\.kt$'     # a Content the developer changed or added
```

- A `<Screen>Content.kt` modified or new in the working tree is the developer's assembled UI → **Tidy** that
  screen (`git diff -- <file>` shows what they built). Several of them → tidy the one the request names; with
  no name, the one whose diff adds the layout, and say which was picked.
- None → **From the design**, for the screen the request names.

## 1. The dynamics table — always first

Before any code, one row per element of the screen:

| Element | Source | Trigger | Component |
|---|---|---|---|
| page indicator | state `currentPage`, `pageCount` | page change | `OnboardingSlide` |
| title, description | `OnboardingPages[currentPage]` | page change | `OnboardingSlide` |
| "Start" button | static | — | in Content |

- **Source** is one of: static, a navigation argument, a state field, remote data (`ContentState`).
- Where it comes from: the design (every frame of the screen — its loading, empty, error and disabled
  variants are what change), the spec or FRD and the API contract (wherever the project keeps them): which
  fields exist, which are optional, what loads, what the user edits. A row the sources do not settle is a
  question for the developer, not a guess.
- **Component boundaries come from the Trigger column:** rows with the same trigger are one component; a
  static row is never inside a component that reads state; `<Screen>Content` reads nothing. The state's shape
  comes from the Source column (arch-kit picks the level).

Show the table in the reply (or the task's `plan.md` for a large screen) before writing the code.

## 2a. From the design

1. Find the design as the `design-system` skill orders it — a design-kit prototype in or beside the repository,
   Figma (through `figma-bridge`: frames by page and canvas label, exported), or the developer's screenshots —
   and say which was used. Write the value table: every colour, gradient, blur, size, gap, padding and type →
   its token, or "no token", or "not read"; values come from the source's data (the prototype's tokens, the
   export's `structure.json`), never from a picture.
2. `design-system`: classify each element — an existing `Ds…`, a new atom or molecule, or the feature's own
   component. Missing tokens and components are added there first, never as literals in the screen.
3. Write the screen by the table: `<Screen>Content` arranges components; each component reads its own state
   from a `@Composable` mapper (`state.to<Component>State()`); callbacks are written in place, never in
   `remember`.

## 2b. Tidy

The developer's Content is the specification of the look. The tidy changes structure, never the look —
a visual change needs the developer's yes.

1. Write the dynamics table from the Content as it is, and from the sources above.
2. Carry out each `TODO(agent)` comment and delete it; one that cannot be done stays, and the report says why.
3. Extract the components the table names, each with its state and mapper; move every `.value` /
   `state.value` read out of the Content into the component that draws it.
4. Replace literals — colours, `dp`, `sp`, alphas, `TextStyle(…)` — with tokens; a value with no token goes to
   the design system first (`design-system`) or is reported. Texts become string resources.
5. Remove `remember` around callbacks; delete commented-out old code the tidy replaced.

## 3. Verify and report

- Compile the module for Android and iOS (`compileAndroidMain`, `compileKotlinIosSimulatorArm64`), Detekt on
  the changed files, `code-review` (rules pass) for the touched screen.
- Report: the table, the components with their triggers, tokens or components added, `TODO(agent)` comments
  done or left, questions the sources did not settle.
