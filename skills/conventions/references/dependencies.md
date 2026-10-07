# Dependencies

**Found:** 2026-10-07 — `androidx-activity = "1.+"` broke three kits the same way

## Rule

1. **Every catalog version is exact.** No `+`, no `latest.release`, no ranges.
2. **A version moves by a commit** that changes the catalog, with the build green on every target.

## Why

`"1.+"` resolved to `1.14.0-alpha03` the day a new alpha shipped; its dependency constraint against the
transitive `activity:1.7.0` then broke resolution of the sample and fixture apps ("No target component for
edge androidx.activity:activity:1.7.0") and failed the IDE sync — in build-kit, nav-kit and paging-kit at
once. A dynamic version also makes yesterday's green build unreproducible.

## Checked by

conventions-kit's `scripts/sync-kits.py --check` (every kit's catalog); review.
