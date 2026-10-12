# Mode: upfront

A team works on the app. The product-neutral part of the design is built in one pass before the
screens, so that developers writing different screens meet the same atoms and molecules instead of
inventing their own. Only what the design names is built: the foundation grows from the components,
not the other way round.

## The pass

1. **Scope — confirm it before building.** List the design's product-neutral components (a design-kit
   prototype's `core/` spec sheets; the matching Figma components) as names, with how many variants and
   states each shows. Leave out what belongs elsewhere: product-named groups (feature components),
   and the overlays (overlay-kit). Show the list and the build order to the developer and ask two
   things: is anything missing or not wanted, and should a gallery screen listing every component be
   built (it is the team's living documentation; it is only built when asked for).
2. **Build in dependency order**: the theme mechanism and `@DsPreview` first, then atoms (text, icon,
   button, chip, switch, avatar, divider), then the molecules made of them (labelled field, list row,
   banner, tabs). Each component by steps 3.3 → 3.5 of the skill, complete in one go: every variant and
   state of its spec sheet, a preview for each, tokens added as it reads them and no others.
3. **Test what has logic.** A state holder, a pure function or a layout calculation gets a test
   ([tests](../../conventions/references/tests.md)); a component that only draws gets its previews.
4. **The gallery**, when asked for: one screen listing every component with its variants, in light and
   dark, as the design-system module's own sample or a debug-only feature.
5. **Report** (3.6), including what the design lists that was left out and why.

## After the pass

The design system is the team's shared contract. A screen that needs something it lacks has found a gap
in the design or in this pass — say so rather than drawing the missing piece in the screen. The
addition is then a change of its own, named after the component, with the screen that needed it in its
KDoc, so the other developers see a design-system change and not a detail of someone's screen.
Running the skill again in `upfront` mode with an existing design system is that same step, for one
component at a time.
