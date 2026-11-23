# Open Policy Agent policy operations evidence

Use this reference when an authorization decision depends on evaluator
integration, policy rollout, version compatibility or decision telemetry.

Identify the policy enforcement caller, evaluator representation and decision
path. Pin the result type, approved behavior for an undefined result or
unavailable evaluator, fixture version, and test observations. Test Rego rules
and caller enforcement as separate interfaces before claiming that the
approved access behavior works.

For a bundle-based deployment, record the admitted bundle identity and
observed active revision. Check applicable bundle verification and rollback
assumptions against the runtime and distributor in scope. For decision logs,
verify masking and retention for the information classes present in inputs
and results. A logged decision may support a policy-evaluation claim. Evidence
from the caller supports claims about actual enforcement.

[OPA integration](https://www.openpolicyagent.org/docs/integration)
[Policy testing](https://www.openpolicyagent.org/docs/policy-testing)
[Bundles](https://www.openpolicyagent.org/docs/management-bundles)
[Decision logs](https://www.openpolicyagent.org/docs/management-decision-logs)
[Upstream releases](https://github.com/open-policy-agent/opa/releases)
