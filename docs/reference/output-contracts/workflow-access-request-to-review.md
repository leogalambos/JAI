<!-- JAI:OUTPUT-CONTRACTS:START -->
# Access request to periodic review: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-access-request-to-review-1"></a>

## request with entitlement and approval path

**Handoff content contract:** `handoff/access-request-to-review:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_access_request`**: For request with entitlement and approval path, supply the actual versioned access request record, including request_id, subject, entitlement, purpose, request_type, approval_path. Independently assess the evidence against this exact criterion: Entitlement and approval path defined for the request type. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `request_id`, `subject`, `entitlement`, `purpose`, `request_type`, `approval_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `service-desk-analyst`; **receiver:** `data-owner`.

**Receiving condition:** Entitlement and approval path defined for the request type

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_access_request`**: For request with entitlement and approval path, supply the actual versioned access request record, including request_id, subject, entitlement, purpose, request_type, approval_path. Independently assess the evidence against this exact criterion: Entitlement and approval path defined for the request type. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `request_id`, `subject`, `entitlement`, `purpose`, `request_type`, `approval_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `privileged`.

**Producer:** `service-desk-analyst`; **receiver:** `data-owner`.

**Receiving condition:** Entitlement and approval path defined for the request type

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_access_request`**: For request with entitlement and approval path, supply the actual versioned access request record, including request_id, subject, entitlement, purpose, request_type, approval_path. Independently assess the evidence against this exact criterion: Entitlement and approval path defined for the request type. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `request_id`, `subject`, `entitlement`, `purpose`, `request_type`, `approval_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `leaver-transfer`.

**Producer:** `service-desk-analyst`; **receiver:** `data-owner`.

**Receiving condition:** Entitlement and approval path defined for the request type

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_access_request`**: For request with entitlement and approval path, supply the actual versioned access request record, including request_id, subject, entitlement, purpose, request_type, approval_path. Independently assess the evidence against this exact criterion: Entitlement and approval path defined for the request type. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `request_id`, `subject`, `entitlement`, `purpose`, `request_type`, `approval_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-access-request-to-review-2"></a>

## access decision recorded with its purpose

**Handoff content contract:** `handoff/access-request-to-review:2`.

**Basis:** JAI-authored individual access-decision practice; professional qualification pending.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`individual_access_decision`**: Record the specific access subject, requested entitlement, justified purpose, actual grant/refusal decision, accountable authority, validity/review condition and applicable versioned policy; policy text alone is insufficient.
  Required fields: `subject`, `entitlement`, `purpose`, `decision`, `authority`, `validity`, `policy_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `data-owner`; **receiver:** `identity-and-access-management-engineer`.

**Receiving condition:** Purpose-free access grants refused

**Next:** Step 3.

**Role output contracts:** `data-owner:2`.

- **`individual_access_decision`**: Record the specific access subject, requested entitlement, justified purpose, actual grant/refusal decision, accountable authority, validity/review condition and applicable versioned policy; policy text alone is insufficient.
  Required fields: `subject`, `entitlement`, `purpose`, `decision`, `authority`, `validity`, `policy_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `privileged`.

**Producer:** `data-owner`; **receiver:** `identity-and-access-management-engineer`.

**Receiving condition:** Purpose-free access grants refused

**Next:** Step 3.

**Role output contracts:** `data-owner:2`.

- **`individual_access_decision`**: Record the specific access subject, requested entitlement, justified purpose, actual grant/refusal decision, accountable authority, validity/review condition and applicable versioned policy; policy text alone is insufficient.
  Required fields: `subject`, `entitlement`, `purpose`, `decision`, `authority`, `validity`, `policy_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `leaver-transfer`.

**Producer:** `data-owner`; **receiver:** `identity-and-access-management-engineer`.

**Receiving condition:** Purpose-free access grants refused

**Next:** Step 3.

**Role output contracts:** `data-owner:2`.

- **`individual_access_decision`**: Record the specific access subject, requested entitlement, justified purpose, actual grant/refusal decision, accountable authority, validity/review condition and applicable versioned policy; policy text alone is insufficient.
  Required fields: `subject`, `entitlement`, `purpose`, `decision`, `authority`, `validity`, `policy_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-access-request-to-review-3"></a>

## provisioned access, automated where integrated

**Handoff content contract:** `handoff/access-request-to-review:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_access_provisioning`**: For provisioned access, automated where integrated, supply the actual versioned access provisioning record, including decision_ref, subject, entitlement, actual_provisioning, evidence, revocation_event_evidence. Independently assess the evidence against this exact criterion: Leaver revocation evidenced automatically, not attested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `decision_ref`, `subject`, `entitlement`, `actual_provisioning`, `evidence`, `revocation_event_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `identity-and-access-management-engineer`; **receiver:** `identity-governance-specialist`.

**Receiving condition:** Leaver revocation evidenced automatically, not attested

**Next:** Step 5.

**Role output contracts:** `identity-and-access-management-engineer:2`, `identity-and-access-management-engineer:3`.

- **`handoff_access_provisioning`**: For provisioned access, automated where integrated, supply the actual versioned access provisioning record, including decision_ref, subject, entitlement, actual_provisioning, evidence, revocation_event_evidence. Independently assess the evidence against this exact criterion: Leaver revocation evidenced automatically, not attested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `decision_ref`, `subject`, `entitlement`, `actual_provisioning`, `evidence`, `revocation_event_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `privileged`.

**Producer:** `identity-and-access-management-engineer`; **receiver:** `privileged-access-management-administrator`.

**Receiving condition:** Leaver revocation evidenced automatically, not attested

**Next:** Step 4.

**Role output contracts:** `identity-and-access-management-engineer:2`, `identity-and-access-management-engineer:3`.

- **`handoff_access_provisioning`**: For provisioned access, automated where integrated, supply the actual versioned access provisioning record, including decision_ref, subject, entitlement, actual_provisioning, evidence, revocation_event_evidence. Independently assess the evidence against this exact criterion: Leaver revocation evidenced automatically, not attested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `decision_ref`, `subject`, `entitlement`, `actual_provisioning`, `evidence`, `revocation_event_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `leaver-transfer`.

**Producer:** `identity-and-access-management-engineer`; **receiver:** `identity-governance-specialist`.

**Receiving condition:** Leaver revocation evidenced automatically, not attested

**Next:** Step 5.

**Role output contracts:** `identity-and-access-management-engineer:2`, `identity-and-access-management-engineer:3`.

- **`handoff_access_provisioning`**: For provisioned access, automated where integrated, supply the actual versioned access provisioning record, including decision_ref, subject, entitlement, actual_provisioning, evidence, revocation_event_evidence. Independently assess the evidence against this exact criterion: Leaver revocation evidenced automatically, not attested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `decision_ref`, `subject`, `entitlement`, `actual_provisioning`, `evidence`, `revocation_event_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-access-request-to-review-4"></a>

## vaulted account with session monitoring

**Handoff content contract:** `handoff/access-request-to-review:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_privileged_account_controls`**: For vaulted account with session monitoring, supply the actual versioned privileged account controls record, including account_id, vault_ref, session_monitoring, break_glass_test, use_review. Independently assess the evidence against this exact criterion: Break-glass tested on a schedule; every use reviewed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `account_id`, `vault_ref`, `session_monitoring`, `break_glass_test`, `use_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `privileged`.

**Producer:** `privileged-access-management-administrator`; **receiver:** `identity-governance-specialist`.

**Receiving condition:** Break-glass tested on a schedule; every use reviewed

**Next:** Step 5.

**Role output contracts:** `privileged-access-management-administrator:1`, `privileged-access-management-administrator:2`.

- **`handoff_privileged_account_controls`**: For vaulted account with session monitoring, supply the actual versioned privileged account controls record, including account_id, vault_ref, session_monitoring, break_glass_test, use_review. Independently assess the evidence against this exact criterion: Break-glass tested on a schedule; every use reviewed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `account_id`, `vault_ref`, `session_monitoring`, `break_glass_test`, `use_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-access-request-to-review-5"></a>

## certification campaign results

**Handoff content contract:** `handoff/access-request-to-review:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_access_certification`**: For certification campaign results, supply the actual versioned access certification record, including campaign_scope, reviewer_knowledge, entitlement_decisions, evidence, exceptions, revocation_followup. Independently assess the evidence against this exact criterion: Reviewers have actual knowledge of the access. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `campaign_scope`, `reviewer_knowledge`, `entitlement_decisions`, `evidence`, `exceptions`, `revocation_followup`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `identity-governance-specialist`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Reviewers have actual knowledge of the access

**Next:** Step 6.

**Role output contracts:** `identity-governance-specialist:1`.

- **`handoff_access_certification`**: For certification campaign results, supply the actual versioned access certification record, including campaign_scope, reviewer_knowledge, entitlement_decisions, evidence, exceptions, revocation_followup. Independently assess the evidence against this exact criterion: Reviewers have actual knowledge of the access. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `campaign_scope`, `reviewer_knowledge`, `entitlement_decisions`, `evidence`, `exceptions`, `revocation_followup`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `privileged`.

**Producer:** `identity-governance-specialist`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Reviewers have actual knowledge of the access

**Next:** Step 6.

**Role output contracts:** `identity-governance-specialist:1`.

- **`handoff_access_certification`**: For certification campaign results, supply the actual versioned access certification record, including campaign_scope, reviewer_knowledge, entitlement_decisions, evidence, exceptions, revocation_followup. Independently assess the evidence against this exact criterion: Reviewers have actual knowledge of the access. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `campaign_scope`, `reviewer_knowledge`, `entitlement_decisions`, `evidence`, `exceptions`, `revocation_followup`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `leaver-transfer`.

**Producer:** `identity-governance-specialist`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Reviewers have actual knowledge of the access

**Next:** Step 6.

**Role output contracts:** `identity-governance-specialist:1`.

- **`handoff_access_certification`**: For certification campaign results, supply the actual versioned access certification record, including campaign_scope, reviewer_knowledge, entitlement_decisions, evidence, exceptions, revocation_followup. Independently assess the evidence against this exact criterion: Reviewers have actual knowledge of the access. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `campaign_scope`, `reviewer_knowledge`, `entitlement_decisions`, `evidence`, `exceptions`, `revocation_followup`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-access-request-to-review-6"></a>

## audit finding or assurance

**Handoff content contract:** `handoff/access-request-to-review:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_access_assurance`**: For audit finding or assurance, supply the actual versioned access assurance record, including assessed_period, criteria, sample, control_evidence, findings, auditor_independence. Independently assess the evidence against this exact criterion: Auditor never operated the control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `assessed_period`, `criteria`, `sample`, `control_evidence`, `findings`, `auditor_independence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Auditor never operated the control

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_access_assurance`**: For audit finding or assurance, supply the actual versioned access assurance record, including assessed_period, criteria, sample, control_evidence, findings, auditor_independence. Independently assess the evidence against this exact criterion: Auditor never operated the control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `assessed_period`, `criteria`, `sample`, `control_evidence`, `findings`, `auditor_independence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `privileged`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Auditor never operated the control

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_access_assurance`**: For audit finding or assurance, supply the actual versioned access assurance record, including assessed_period, criteria, sample, control_evidence, findings, auditor_independence. Independently assess the evidence against this exact criterion: Auditor never operated the control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `assessed_period`, `criteria`, `sample`, `control_evidence`, `findings`, `auditor_independence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `leaver-transfer`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Auditor never operated the control

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_access_assurance`**: For audit finding or assurance, supply the actual versioned access assurance record, including assessed_period, criteria, sample, control_evidence, findings, auditor_independence. Independently assess the evidence against this exact criterion: Auditor never operated the control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `assessed_period`, `criteria`, `sample`, `control_evidence`, `findings`, `auditor_independence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
