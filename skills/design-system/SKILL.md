---
name: design-system
description: Builds and grows the design system (`designsystem/foundation` and `designsystem/components`) of a Compose Multiplatform app on the Thernal kits. Reads the design (a design-kit prototype, Figma, or the developer's description), decides for every element whether it is an existing component, a new atom or molecule, or a feature's own component, adds only the tokens and components a screen needs, and checks the result against the design-system rules. Two modes, recorded in .agents/workspace.md — `grow` (extend the design system screen by screen, for one developer) and `upfront` (build the product-neutral set in one pass, for a team). Use whenever a screen, a Ds component, a token or the theme is about to be written in such a project — "extend the design system", "add a Ds component", "build the foundation", "DS qur", "DS-i genişləndir", "bu ekran üçün komponent lazımdır". Not for a feature's own components (conventions), overlays (overlay-kit) or HTML prototypes (design-kit).
---

# Design system

The procedure for building the design system of an app on the kits. What the code looks like is the
`conventions` skill's [design-system](../conventions/references/design-system.md) rule — read it, and
its Example, before writing a component. This skill decides *what* to write, *when*, and in *which*
module.

A design system is never copied from another project. ArenaGo's, Act2Act's and DropNote's are read for
their shape, never taken whole: a foundation built to look complete holds tokens no screen uses, and
the design system exists to hold what the screens use.

## 1. Mode — read or resolve

Read `.agents/workspace.md`. The row this skill owns:

| Row | Values | Meaning |
|---|---|---|
| Design system mode | `grow` or `upfront` | `grow`: the design system starts as small as the first screen and is extended by every screen, in the change that needs it — one developer owns the app. `upfront`: the design's product-neutral set is built in one pass before the screens, so developers working in parallel meet the same atoms — a team. |

If the row is absent, look before asking: `git shortlog -sn --all | head` (how many people commit),
the remote (a team's GitLab or a personal one), and what already exists in `designsystem/`. Then ask
once, with the recommendation — one author → `grow`, several → `upfront` — and write the row. The mode
can change later; edit the row, nothing else moves.

Then read the file for the mode and follow it: [grow](references/grow.md) or
[upfront](references/upfront.md). Both use the shared steps below.

## 2. Find the design

In this order, and say which one you used when you report:

1. **A design-kit prototype** in the repository or beside it (`design/`): `screens.js` lists the
   screens, `tokens.css` holds the tokens, and `components/<group>/<name>/index.html` is each
   component's spec sheet with every variant and state. The `core/` group knows nothing about the
   product; a group named after the product, `shared/`, `customer/` or `business/` does.
2. **Figma**, when the design lives there and the Figma tools are connected (figma-kit builds the file
   from a design-kit prototype).
3. **Nothing written down**: the developer's screenshots or description. Say that there is no design
   source; do not invent values.

## 3. Shared steps

**3.1 Inventory.** What exists is the code, not a document: `Ds*` composables under
`designsystem/components`, and the tokens in `designsystem/foundation`.

```sh
grep -rhoE "^(internal )?fun Ds[A-Za-z]+" designsystem/components --include='*.kt' | sed 's/.*fun //' | sort -u
find designsystem/foundation/src -name '*.kt' | sort
```

**3.2 Classify every element of the screen or spec sheet**, one decision each:

| The element | Decision |
|---|---|
| exists in the inventory with the variant it needs | use it |
| exists, needs a variant, size or tone it lacks | extend that component — never a sibling beside it |
| a single primitive, no product meaning (a button, a chip, a switch) | new **atom** in `designsystem/components` |
| atoms composed, no product meaning (a labelled field, a list row, a banner) | new **molecule** in `designsystem/components` |
| carries product vocabulary (an offer card, a booking row) | the **feature's** component; other features get it through the feature's `api` render contract ([components](../conventions/references/components.md) rule 8) — never the design system |
| a dialog, bottom sheet, dropdown, tooltip, snackbar, showcase | **overlay-kit**: the app maps its tokens in its overlay styles file; nothing is built here |

**3.3 Tokens.** For each value the new component reads, find the design's token and add only that one.

- The Kotlin name follows the design's token name, in camel case (`--background-02` → `background02`;
  `--color-surface-raised` → `surfaceRaised`). A project that already has a vocabulary keeps it; two
  vocabularies never mix.
- Light and dark together. The values are the design's resolved values, not recomputed by hand —
  when the design is a design-kit prototype, resolve `tokens.css` in a browser and compare (DropNote's
  `scripts/golden-tokens/` does this; it is that project's code, not part of this kit).
- The KDoc of a token or a component names the screen or component that needed it. No token is added to
  complete a ramp or a scale.

**3.4 Write the component** by the rule: parameter order, `State<T>` only for a value that changes
often, plain for the rest, `modifier` on the root, no Material (copy the behaviour with a header when
it is needed), tokens only, a `String` or a slot for text, icons by the library's typed accessor, a
`@DsPreview` for every variant and state. One component, compile and preview, then the next.

**3.5 Check** before reporting: the project's build and Detekt (the Verification row of
`.agents/workspace.md`), `grep -rn "androidx.compose.material" designsystem/ features/` finds nothing,
and the `conventions-review` skill over the diff.

**3.6 Report** in a few lines, by category, each with the screen or spec sheet that needed it:
components added or extended, tokens added, icons added, feature components left in their feature,
overlays left to overlay-kit, and what the design did not say.

## 4. Never

- Copy a design system, or a foundation, from another project.
- Add a component, a token or an icon "because the set looks incomplete".
- Draw an atom a screen needs inside the screen "for now".
- Promote a feature's component into the design system.
- Put a literal colour, size, alpha or duration in a component, or import Material.
- Edit kit code (overlay-kit, media-kit) to restyle it; the app maps its tokens ([kit-styling](../conventions/references/kit-styling.md)).
