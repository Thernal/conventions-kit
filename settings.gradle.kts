// conventions-kit has no modules of its own: the root build exists to build and test `build-logic`,
// the master copy every kit's build logic is synced from (`scripts/sync-kits.py`).
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "conventions-kit"
includeBuild("build-logic")
