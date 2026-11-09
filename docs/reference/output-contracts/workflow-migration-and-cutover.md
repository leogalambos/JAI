<!-- JAI:OUTPUT-CONTRACTS:START -->
# Migration and cutover: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-migration-and-cutover-1"></a>

## migration data model and ownership boundaries

**Handoff content contract:** `handoff/migration-and-cutover:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_migration_data_boundary`**: For migration data model and ownership boundaries, supply the actual versioned migration data boundary record, including source_target_domains, accountable_owners, target_definitions, classification, mappings. Independently assess the evidence against this exact criterion: Every migrated domain has an accountable data owner and target definition. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_target_domains`, `accountable_owners`, `target_definitions`, `classification`, `mappings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `data-architect`; **receiver:** `data-migration-and-cutover-lead`.

**Receiving condition:** Every migrated domain has an accountable data owner and target definition

**Next:** Step 2.

**Role output contracts:** `data-architect:1`, `data-architect:3`.

- **`handoff_migration_data_boundary`**: For migration data model and ownership boundaries, supply the actual versioned migration data boundary record, including source_target_domains, accountable_owners, target_definitions, classification, mappings. Independently assess the evidence against this exact criterion: Every migrated domain has an accountable data owner and target definition. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_target_domains`, `accountable_owners`, `target_definitions`, `classification`, `mappings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `data-architect`; **receiver:** `data-migration-and-cutover-lead`.

**Receiving condition:** Every migrated domain has an accountable data owner and target definition

**Next:** Step 2.

**Role output contracts:** `data-architect:1`, `data-architect:3`.

- **`handoff_migration_data_boundary`**: For migration data model and ownership boundaries, supply the actual versioned migration data boundary record, including source_target_domains, accountable_owners, target_definitions, classification, mappings. Independently assess the evidence against this exact criterion: Every migrated domain has an accountable data owner and target definition. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_target_domains`, `accountable_owners`, `target_definitions`, `classification`, `mappings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-2"></a>

## migration plan, cutover runbook and rollback plan

**Handoff content contract:** `handoff/migration-and-cutover:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_migration_cutover_plan`**: For migration plan, cutover runbook and rollback plan, supply the actual versioned migration cutover plan record, including object_inventory, mappings, wave_sequence, acceptance_criteria, rollback_restore_semantics. Independently assess the evidence against this exact criterion: Every object has mapping, acceptance and rollback/restore semantics. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `object_inventory`, `mappings`, `wave_sequence`, `acceptance_criteria`, `rollback_restore_semantics`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `data-migration-and-cutover-lead`; **receiver:** `data-engineer`.

**Receiving condition:** Every object has mapping, acceptance and rollback/restore semantics

**Next:** Step 3.

**Role output contracts:** `data-migration-and-cutover-lead:1`, `data-migration-and-cutover-lead:2`, `data-migration-and-cutover-lead:4`.

- **`handoff_migration_cutover_plan`**: For migration plan, cutover runbook and rollback plan, supply the actual versioned migration cutover plan record, including object_inventory, mappings, wave_sequence, acceptance_criteria, rollback_restore_semantics. Independently assess the evidence against this exact criterion: Every object has mapping, acceptance and rollback/restore semantics. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `object_inventory`, `mappings`, `wave_sequence`, `acceptance_criteria`, `rollback_restore_semantics`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `data-migration-and-cutover-lead`; **receiver:** `data-engineer`.

**Receiving condition:** Every object has mapping, acceptance and rollback/restore semantics

**Next:** Step 3.

**Role output contracts:** `data-migration-and-cutover-lead:1`, `data-migration-and-cutover-lead:2`, `data-migration-and-cutover-lead:4`.

- **`handoff_migration_cutover_plan`**: For migration plan, cutover runbook and rollback plan, supply the actual versioned migration cutover plan record, including object_inventory, mappings, wave_sequence, acceptance_criteria, rollback_restore_semantics. Independently assess the evidence against this exact criterion: Every object has mapping, acceptance and rollback/restore semantics. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `object_inventory`, `mappings`, `wave_sequence`, `acceptance_criteria`, `rollback_restore_semantics`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-3"></a>

## pre-production rehearsal evidence and exceptions

**Handoff content contract:** `handoff/migration-and-cutover:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_migration_rehearsal`**: For pre-production rehearsal evidence and exceptions, supply the actual versioned migration rehearsal record, including permitted_data_scope, rehearsal_revision, throughput, error_handling, repeatability, exceptions. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `permitted_data_scope`, `rehearsal_revision`, `throughput`, `error_handling`, `repeatability`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `data-engineer`; **receiver:** `test-manager`.

**Receiving condition:** Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects

**Next:** Step 4.

**Role output contracts:** `data-engineer:1`, `data-engineer:3`.

- **`handoff_migration_rehearsal`**: For pre-production rehearsal evidence and exceptions, supply the actual versioned migration rehearsal record, including permitted_data_scope, rehearsal_revision, throughput, error_handling, repeatability, exceptions. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `permitted_data_scope`, `rehearsal_revision`, `throughput`, `error_handling`, `repeatability`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `data-engineer`; **receiver:** `test-manager`.

**Receiving condition:** Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects

**Next:** Step 4.

**Role output contracts:** `data-engineer:1`, `data-engineer:3`.

- **`handoff_migration_rehearsal`**: For pre-production rehearsal evidence and exceptions, supply the actual versioned migration rehearsal record, including permitted_data_scope, rehearsal_revision, throughput, error_handling, repeatability, exceptions. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `permitted_data_scope`, `rehearsal_revision`, `throughput`, `error_handling`, `repeatability`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-4"></a>

## test and residual-risk report

**Handoff content contract:** `handoff/migration-and-cutover:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_rehearsal_test_conclusion`**: For test and residual-risk report, supply the actual versioned rehearsal test conclusion record, including predeclared_exit_criteria, actual_results, residual_risks, scoped_exception_authority, blocking_findings. Independently assess the evidence against this exact criterion: Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `predeclared_exit_criteria`, `actual_results`, `residual_risks`, `scoped_exception_authority`, `blocking_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `test-manager`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking

**Next:** Step 5.

**Role output contracts:** `test-manager:2`, `test-manager:3`.

- **`handoff_rehearsal_test_conclusion`**: For test and residual-risk report, supply the actual versioned rehearsal test conclusion record, including predeclared_exit_criteria, actual_results, residual_risks, scoped_exception_authority, blocking_findings. Independently assess the evidence against this exact criterion: Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `predeclared_exit_criteria`, `actual_results`, `residual_risks`, `scoped_exception_authority`, `blocking_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `test-manager`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking

**Next:** Step 5.

**Role output contracts:** `test-manager:2`, `test-manager:3`.

- **`handoff_rehearsal_test_conclusion`**: For test and residual-risk report, supply the actual versioned rehearsal test conclusion record, including predeclared_exit_criteria, actual_results, residual_risks, scoped_exception_authority, blocking_findings. Independently assess the evidence against this exact criterion: Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `predeclared_exit_criteria`, `actual_results`, `residual_risks`, `scoped_exception_authority`, `blocking_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-5"></a>

## operational cutover constraints and acceptance evidence

**Handoff content contract:** `handoff/migration-and-cutover:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_cutover_operational_constraints`**: For operational cutover constraints and acceptance evidence, supply the actual versioned cutover operational constraints record, including readiness_criteria, operational_limits, receiving_evidence, critical_gaps, owners. Independently assess the evidence against this exact criterion: No critical operational readiness gap is unowned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `operational_limits`, `receiving_evidence`, `critical_gaps`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `release-engineer`.

**Receiving condition:** No critical operational readiness gap is unowned

**Next:** Step 6.

**Role output contracts:** `service-transition-and-operational-readiness-manager:3`.

- **`handoff_cutover_operational_constraints`**: For operational cutover constraints and acceptance evidence, supply the actual versioned cutover operational constraints record, including readiness_criteria, operational_limits, receiving_evidence, critical_gaps, owners. Independently assess the evidence against this exact criterion: No critical operational readiness gap is unowned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `operational_limits`, `receiving_evidence`, `critical_gaps`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `release-engineer`.

**Receiving condition:** No critical operational readiness gap is unowned

**Next:** Step 6.

**Role output contracts:** `service-transition-and-operational-readiness-manager:3`.

- **`handoff_cutover_operational_constraints`**: For operational cutover constraints and acceptance evidence, supply the actual versioned cutover operational constraints record, including readiness_criteria, operational_limits, receiving_evidence, critical_gaps, owners. Independently assess the evidence against this exact criterion: No critical operational readiness gap is unowned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `operational_limits`, `receiving_evidence`, `critical_gaps`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-6"></a>

## candidate release manifest and rehearsal deployment/rollback evidence

**Handoff content contract:** `handoff/migration-and-cutover:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_cutover_release_candidate`**: For candidate release manifest and rehearsal deployment/rollback evidence, supply the actual versioned cutover release candidate record, including artifact_versions, rehearsal_results, deployment_steps, rollback_steps, production_boundary. Independently assess the evidence against this exact criterion: Exact artefact versions and rollback steps are known; no production effects before the human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_versions`, `rehearsal_results`, `deployment_steps`, `rollback_steps`, `production_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `rehearsal`.

**Producer:** `release-engineer`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Exact artefact versions and rollback steps are known; no production effects before the human change decision

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `release-engineer:2`, `release-engineer:4`.

- **`handoff_cutover_release_candidate`**: For candidate release manifest and rehearsal deployment/rollback evidence, supply the actual versioned cutover release candidate record, including artifact_versions, rehearsal_results, deployment_steps, rollback_steps, production_boundary. Independently assess the evidence against this exact criterion: Exact artefact versions and rollback steps are known; no production effects before the human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_versions`, `rehearsal_results`, `deployment_steps`, `rollback_steps`, `production_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cutover`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Exact artefact versions and rollback steps are known; no production effects before the human change decision

**Next:** Step 7.

**Role output contracts:** `release-engineer:2`, `release-engineer:4`.

- **`handoff_cutover_release_candidate`**: For candidate release manifest and rehearsal deployment/rollback evidence, supply the actual versioned cutover release candidate record, including artifact_versions, rehearsal_results, deployment_steps, rollback_steps, production_boundary. Independently assess the evidence against this exact criterion: Exact artefact versions and rollback steps are known; no production effects before the human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_versions`, `rehearsal_results`, `deployment_steps`, `rollback_steps`, `production_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-7"></a>

## production change authorisation

**Handoff content contract:** `handoff/migration-and-cutover:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_cutover_authorisation`**: For production change authorisation, supply the actual versioned cutover authorisation record, including rehearsal_refs, reconciliation_design, readiness_refs, exact_effect_scope, authority, window, rollback_boundaries. Independently assess the evidence against this exact criterion: Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `rehearsal_refs`, `reconciliation_design`, `readiness_refs`, `exact_effect_scope`, `authority`, `window`, `rollback_boundaries`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cutover`.

**Producer:** `change-manager`; **receiver:** `data-engineer`.

**Receiving condition:** Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope

**Next:** Step 8.

**Role output contracts:** `change-manager:1`.

- **`handoff_cutover_authorisation`**: For production change authorisation, supply the actual versioned cutover authorisation record, including rehearsal_refs, reconciliation_design, readiness_refs, exact_effect_scope, authority, window, rollback_boundaries. Independently assess the evidence against this exact criterion: Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `rehearsal_refs`, `reconciliation_design`, `readiness_refs`, `exact_effect_scope`, `authority`, `window`, `rollback_boundaries`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-8"></a>

## actual cutover execution, reconciliation and stop/go evidence

**Handoff content contract:** `handoff/migration-and-cutover:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_actual_cutover`**: For actual cutover execution, reconciliation and stop/go evidence, supply the actual versioned actual cutover record, including prior_authorisation_ref, actual_versions, actual_actions, reconciliation, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `actual_versions`, `actual_actions`, `reconciliation`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cutover`.

**Producer:** `data-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope

**Next:** Step 9.

**Role output contracts:** `data-engineer:1`, `data-engineer:3`.

- **`handoff_actual_cutover`**: For actual cutover execution, reconciliation and stop/go evidence, supply the actual versioned actual cutover record, including prior_authorisation_ref, actual_versions, actual_actions, reconciliation, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `actual_versions`, `actual_actions`, `reconciliation`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-9"></a>

## executed independent validation cases, observed results, reconciliation evidence and located defects

**Handoff content contract:** `handoff/migration-and-cutover:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_independent_cutover_validation`**: For executed independent validation cases, observed results, reconciliation evidence and located defects, supply the actual versioned independent cutover validation record, including prior_authorisation_ref, validator_independence, actual_cases, observed_results, reconciliation, defects, untested_scope. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `validator_independence`, `actual_cases`, `observed_results`, `reconciliation`, `defects`, `untested_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cutover`.

**Producer:** `test-analyst`; **receiver:** `test-manager`.

**Receiving condition:** Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check

**Next:** Step 10.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_independent_cutover_validation`**: For executed independent validation cases, observed results, reconciliation evidence and located defects, supply the actual versioned independent cutover validation record, including prior_authorisation_ref, validator_independence, actual_cases, observed_results, reconciliation, defects, untested_scope. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `validator_independence`, `actual_cases`, `observed_results`, `reconciliation`, `defects`, `untested_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-10"></a>

## independent production validation and residual-risk report

**Handoff content contract:** `handoff/migration-and-cutover:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_production_validation_conclusion`**: For independent production validation and residual-risk report, supply the actual versioned production validation conclusion record, including validation_evidence, predeclared_criteria, residual_defects, risk_disposition, blocking_status. Independently assess the evidence against this exact criterion: Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validation_evidence`, `predeclared_criteria`, `residual_defects`, `risk_disposition`, `blocking_status`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cutover`.

**Producer:** `test-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance

**Next:** Step 11.

**Role output contracts:** `test-manager:2`, `test-manager:3`.

- **`handoff_production_validation_conclusion`**: For independent production validation and residual-risk report, supply the actual versioned production validation conclusion record, including validation_evidence, predeclared_criteria, residual_defects, risk_disposition, blocking_status. Independently assess the evidence against this exact criterion: Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validation_evidence`, `predeclared_criteria`, `residual_defects`, `risk_disposition`, `blocking_status`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-migration-and-cutover-11"></a>

## service acceptance and residual issues

**Handoff content contract:** `handoff/migration-and-cutover:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_migrated_service_acceptance`**: For service acceptance and residual issues, supply the actual versioned migrated service acceptance record, including service_validation, data_reconciliation, ownership_acceptance, residual_issues, legacy_retirement_conditions. Independently assess the evidence against this exact criterion: Service, data and ownership acceptance are explicit before legacy retirement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_validation`, `data_reconciliation`, `ownership_acceptance`, `residual_issues`, `legacy_retirement_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cutover`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Service, data and ownership acceptance are explicit before legacy retirement

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`, `it-service-owner:4`.

- **`handoff_migrated_service_acceptance`**: For service acceptance and residual issues, supply the actual versioned migrated service acceptance record, including service_validation, data_reconciliation, ownership_acceptance, residual_issues, legacy_retirement_conditions. Independently assess the evidence against this exact criterion: Service, data and ownership acceptance are explicit before legacy retirement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_validation`, `data_reconciliation`, `ownership_acceptance`, `residual_issues`, `legacy_retirement_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
