---
description: Add supplier-side opportunity, discovery, commercial economics and delivery monitoring to an existing JAI engagement.
---

# Commercial

Use the `commercial-delivery` skill and `commercial-coordinator` procedure. This is an opt-in extension, preserving existing technical `/layered` and `/sabsa` behaviour.

1. Establish the human commercial owner and explicit profile scope change. Reuse canonical identities, source passages and existing engagement memberships.
2. Qualify the opportunity; iterate discovery with the six-question domain matrix. Unknown client/expert estimates remain explicit.
3. Assign the dedicated bid/proposal, estimation/cost engineering, pricing/deal finance, supplier deal-management and independent commercial-assurance roles to their respective scopes; never substitute an adjacent role. Route specialist consultation through the orchestrator. Load compact root metadata, selected domain shard, then selected role reference. Do not load the full role catalog into every worker context.
4. Build versioned effort, staffing, cost, price, terms and uncertainty models. Separate baseline, forecast, actual, accrual and cash; validate service coverage alongside workload.
5. Run independent assurance and separate client/internal projections. Keep required client contractual disclosures. Human authority signs scope, commercial risk and contractual commitments.
6. Monitor stages and operations, learning from actuals. Re-estimation creates a forecast; it does not rewrite a signed baseline.

Metadata discovery example (source checkout):

```bash
python3 .ai/runtime/tools/commercial_router.py 'firewall implementation effort' --contract ctr-1 --domain network-and-telecommunications
```

Installed equivalent uses `~/.ai/it-role-house/tools/commercial_router.py`. Routing does not dispatch or authorize a provider. Strict dispatch requires tested controls for the exact provider version/configuration; the shipped capability records are explicitly `not_run` for both Codex and Claude.
