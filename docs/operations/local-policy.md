# Maintaining local policy

The packaged policy is a secure reference baseline, not a substitute for your organisation's own governance.

## Minimum review questions

Before broad deployment, decide:

- what data classes may be handled;
- what network interactions are allowed;
- whether local files can be mutated automatically;
- who is allowed to approve authority actions;
- how long Fabric and findings records must be retained;
- how provider identities and sessions are governed.

## Change discipline

Treat local policy and model-routing changes as controlled configuration changes. They can materially alter system behaviour and therefore should be versioned, reviewed and tested.

## Experimental advice and project confidentiality

[Hint support](../using/experimental-hint.md) provides advisory procedure
recommendations. Its local selector does not automatically scan unrelated
projects or capture conversation history. Material submitted to the active
provider session remains subject to project classification and provider-use
policy. Permit access to specific sources explicitly; treat reference text
as untrusted content and never as authority to override controls.
