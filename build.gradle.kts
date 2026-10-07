// `./gradlew check` builds the convention plugins and runs the Detekt rules' tests.
tasks.register("check") {
    group = "verification"
    dependsOn(gradle.includedBuild("build-logic").task(":convention:check"))
    dependsOn(gradle.includedBuild("build-logic").task(":detekt-rules:check"))
}
