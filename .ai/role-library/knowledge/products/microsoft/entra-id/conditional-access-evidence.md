# Microsoft Entra Conditional Access evidence

Use this reference when work concerns rollout, exceptions, licensing
applicability or emergency recovery.

Record the policy scope, each applicable condition and control, enabled mode,
other potentially applicable policies, and approved exclusions. For a test
population, record the expected decision and observed result with timestamp
and applicable policy version. Distinguish report-only observations from
enforced results. Mark coverage limits for unevaluated populations or signals.

Verify current coverage in the target tenant and distinguish shared platform
features from licensed capabilities. The Microsoft deployment guide identifies
P1 or P2 as the base licence prerequisite and P2 for Microsoft Entra ID
Protection risk conditions. Confirm it when a decision depends on licensing,
cloud or preview status.

Verify the intended emergency access path from authorized observations. Check
independence from normal federation and privileged role activation, the
reasoning behind scoped exclusions, detection of emergency use and test
cadence. Retain evidence without exposing account credentials or unnecessary
sign-in data.

[Conditional Access deployment](https://learn.microsoft.com/en-us/entra/identity/conditional-access/plan-conditional-access)
[Emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
