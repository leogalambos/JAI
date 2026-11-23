# Microsoft Entra ID federation evidence

Use this reference when assessing a tenant's hybrid sign-in design, executing a
federation change or reviewing a recovery or cutover decision.

Record which identity populations use password hash synchronization,
pass-through authentication or federation. Trace each sign-in path to the
applicable verification service, directory, network and operational owners.
Check tenant configuration and evidence of the actual path. If a fallback is
planned, establish its configuration, authorization, activation and test
evidence separately.

For a federation trust, retain the applicable issuer and audience boundaries,
signing credential and rollover ownership, and metadata or trust observations
per the inherited IAM contract. Investigate discrepancies between configuration
and observed sign-in before claiming coverage.

[Microsoft guidance on hybrid authentication methods](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn)
