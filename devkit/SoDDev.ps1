[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CommandArguments
)

# CBO-style Windows-safe front door for the M&B-native Workbench, Order
# Control Plane, and optional Module Studio. The Studio is a loopback-only
# viewer/editor over the same guarded APIs; none of these routes builds or
# exports module data on its own.
$devkitRoot = Split-Path -Parent $PSCommandPath
$workbench = Join-Path $devkitRoot 'workbench\workbench.py'
$orderControl = Join-Path $devkitRoot 'order_control\order_control.py'
$balanceLab = Join-Path $devkitRoot 'troop_item_balance\troop_item_balance.py'
$campaignStateDoctor = Join-Path $devkitRoot 'campaign_state_doctor\campaign_state_doctor.py'
$slotLifecycleLint = Join-Path $devkitRoot 'slot_lifecycle_lint\slot_lifecycle_lint.py'
$dialogueModelChecker = Join-Path $devkitRoot 'dialogue_model_checker\dialogue_model_checker.py'
$stringProvenance = Join-Path $devkitRoot 'string_provenance\string_provenance.py'
$campaignScenarioFuzzer = Join-Path $devkitRoot 'campaign_scenario_fuzzer\campaign_scenario_fuzzer.py'
$semanticChangeDiff = Join-Path $devkitRoot 'semantic_change_diff\semantic_change_diff.py'
$releaseGate = Join-Path $devkitRoot 'release_gate\release_gate.py'
$rglLogSentinel = Join-Path $devkitRoot 'rgl_log_sentinel\rgl_log_sentinel.py'
$moduleBlueprint = Join-Path $devkitRoot 'module_blueprint\module_blueprint.py'
$featureAuthoring = Join-Path $devkitRoot 'feature_authoring\feature_authoring.py'
$contentForge = Join-Path $devkitRoot 'content_forge\content_forge.py'
$studio = Join-Path $devkitRoot 'module_studio\module_studio.py'

if (-not (Test-Path -LiteralPath $workbench)) {
    Write-Error "SoD Workbench entry point was not found: $workbench"
    exit 2
}

if (-not $CommandArguments -or $CommandArguments.Count -eq 0) {
    $CommandArguments = @('summary')
}

if ($CommandArguments[0] -eq 'studio') {
    if (-not (Test-Path -LiteralPath $studio)) {
        Write-Error "SoD Module Studio entry point was not found: $studio"
        exit 2
    }
    $studioArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $studio @studioArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'order') {
    if (-not (Test-Path -LiteralPath $orderControl)) {
        Write-Error "Order Control entry point was not found: $orderControl"
        exit 2
    }
    $orderArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $orderControl @orderArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'balance') {
    if (-not (Test-Path -LiteralPath $balanceLab)) {
        Write-Error "SoD Troop + Item Balance Lab entry point was not found: $balanceLab"
        exit 2
    }
    $balanceArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $balanceLab @balanceArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'state') {
    if (-not (Test-Path -LiteralPath $campaignStateDoctor)) {
        Write-Error "Campaign State Doctor entry point was not found: $campaignStateDoctor"
        exit 2
    }
    $stateArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $campaignStateDoctor @stateArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'slots') {
    if (-not (Test-Path -LiteralPath $slotLifecycleLint)) {
        Write-Error "Slot Lifecycle Lint entry point was not found: $slotLifecycleLint"
        exit 2
    }
    $slotArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $slotLifecycleLint @slotArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'dialogue-model') {
    if (-not (Test-Path -LiteralPath $dialogueModelChecker)) {
        Write-Error "Dialogue Model Checker entry point was not found: $dialogueModelChecker"
        exit 2
    }
    $modelArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $dialogueModelChecker @modelArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'provenance') {
    if (-not (Test-Path -LiteralPath $stringProvenance)) {
        Write-Error "String Provenance entry point was not found: $stringProvenance"
        exit 2
    }
    $provenanceArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $stringProvenance @provenanceArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'fuzz') {
    if (-not (Test-Path -LiteralPath $campaignScenarioFuzzer)) {
        Write-Error "Campaign Scenario Fuzzer entry point was not found: $campaignScenarioFuzzer"
        exit 2
    }
    $fuzzArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $campaignScenarioFuzzer @fuzzArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'semantic') {
    if (-not (Test-Path -LiteralPath $semanticChangeDiff)) {
        Write-Error "Semantic Change Diff entry point was not found: $semanticChangeDiff"
        exit 2
    }
    $semanticArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $semanticChangeDiff @semanticArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'gate') {
    if (-not (Test-Path -LiteralPath $releaseGate)) {
        Write-Error "Strict Release Gate entry point was not found: $releaseGate"
        exit 2
    }
    $gateArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $releaseGate @gateArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'rgl') {
    if (-not (Test-Path -LiteralPath $rglLogSentinel)) {
        Write-Error "RGL Log Sentinel entry point was not found: $rglLogSentinel"
        exit 2
    }
    $rglArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $rglLogSentinel @rglArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'blueprint') {
    if (-not (Test-Path -LiteralPath $moduleBlueprint)) {
        Write-Error "Module Blueprint Compiler entry point was not found: $moduleBlueprint"
        exit 2
    }
    $blueprintArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $moduleBlueprint @blueprintArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'feature') {
    if (-not (Test-Path -LiteralPath $featureAuthoring)) {
        Write-Error "Feature Authoring Compiler entry point was not found: $featureAuthoring"
        exit 2
    }
    $featureArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $featureAuthoring @featureArguments
    exit $LASTEXITCODE
}

if ($CommandArguments[0] -eq 'content') {
    if (-not (Test-Path -LiteralPath $contentForge)) {
        Write-Error "Content Forge entry point was not found: $contentForge"
        exit 2
    }
    $contentArguments = @($CommandArguments | Select-Object -Skip 1)
    & py -3 -B $contentForge @contentArguments
    exit $LASTEXITCODE
}

& py -3 -B $workbench @CommandArguments
exit $LASTEXITCODE
