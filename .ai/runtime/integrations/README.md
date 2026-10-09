# Enterprise integration layer — 26.10.0

Agents depend on provider-neutral enterprise adapters, not vendor APIs.
The first-class categories are ITSM/CMDB, backlog/project management,
GRC, EA repository, CI/CD, identity, observability and financial/TBM.

The standard interface is `discover`, `read`, `query`, `create-draft`,
`validate`, `propose-change`, `execute-approved-change`, `verify`,
`rollback`. Default authority is read-only/dry-run. Mutation requires an
explicit approval whose scope and digest match the proposed change,
followed by verification and a tamper-evident Execution Record audit
event.

Vendor implementations (for example a particular ITSM or backlog
product) sit below this contract and must not leak vendor API semantics
into role/agent prompts.

The generated `adapter-registry.json` records the E25 priority order and
points to the canonical per-adapter contracts. It is an index, not a
second source of truth; `integration_adapters.py` fails qualification if
the registry drifts from those contracts.
