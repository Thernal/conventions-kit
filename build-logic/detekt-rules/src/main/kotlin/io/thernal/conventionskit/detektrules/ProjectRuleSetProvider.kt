package io.thernal.conventionskit.detektrules

import dev.detekt.api.RuleSet
import dev.detekt.api.RuleSetId
import dev.detekt.api.RuleSetProvider
import io.thernal.conventionskit.detektrules.collections.UnsafeCollectionIndexAccess
import io.thernal.conventionskit.detektrules.packageboundary.LayerPackageBoundary
import io.thernal.conventionskit.detektrules.packageboundary.LayerPackageRequired
import io.thernal.conventionskit.detektrules.preview.PreviewMustBePrivate
import io.thernal.conventionskit.detektrules.style.ExpressionBodyNotAllowed
import io.thernal.conventionskit.detektrules.style.MultilineConstructorRequired

class ProjectRuleSetProvider : RuleSetProvider {
    override val ruleSetId = RuleSetId("project")

    override fun instance() = RuleSet(
        ruleSetId,
        listOf(
            ::PreviewMustBePrivate,
            ::UnsafeCollectionIndexAccess,
            ::LayerPackageBoundary,
            ::LayerPackageRequired,
            ::ExpressionBodyNotAllowed,
            ::MultilineConstructorRequired,
        ),
    )
}
