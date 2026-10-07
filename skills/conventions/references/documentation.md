# Documentation

**Decided:** 2026-10-07

## Rule

1. **In a kit, every `api` module has a `README.md`**: how to use it, task by task. A multi-capability
   kit has one per capability, not one shared file.
2. **In an app, every `core` `api` module has one.** A feature's `api` needs one only when it exposes
   more than routes and render contracts — those are documented on the types.
3. **Why a part has its shape** goes in the module's design README (`<module>/README.md`) in a kit.

## Checked by

The kit's done-list; review.
