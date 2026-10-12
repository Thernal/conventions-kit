# Mode: grow

One developer owns the app. The design system is as large as the screens written so far; every screen
extends it first and is written on top of it. The extension and the screen are one piece of work, kept
separable in the diff (the design system under `core/designsystem/`, the screen under `features/`).

## Per screen

1. **Read the screen's design** — the prototype file or the Figma frame — and list every element with
   the variants and states the design shows (disabled, loading, error, selected, each size).
2. **Inventory and classify** (steps 3.1 and 3.2 of the skill). Write the decision for each element
   before writing any code; when one is not obvious — an atom, or a feature's own component? — say
   which you chose and why, in one line.
3. **Extend the design system first**, one component at a time (3.3 → 3.5): its tokens, the
   component with every variant and state the design shows for it, its previews. The first screen of a
   project also needs the theme mechanism and `@DsPreview`/`ThemeWrapper` — create them when the first
   component needs them, no earlier, and with only the tokens that first screen reads.
4. **Then write the screen** and its feature components ([presentation-structure](../../conventions/references/presentation-structure.md),
   [components](../../conventions/references/components.md)) on top of what exists. The screen never
   draws its own version of a missing atom.
5. **Report** (3.6).

## Judgement calls

- **A new variant of an existing component changes how other screens look.** Stop and say so: it is
  either a parameter, a new variant (the old look stays the default), or a sign that the two screens
  disagree — which the developer settles, not the agent.
- **A value the design has no token for.** A question about a missing token, not a literal to paste;
  ask, or add the token with the screen as its reason when the design clearly implies it.
- **The design shows an element twice, slightly different.** Treat it as one component with a variant
  until the design says they are two.
- **Nothing in the design source** (step 2 of the skill, option 3): build the smallest component that
  serves the screen, name the assumptions in the report, and expect them to be corrected.
