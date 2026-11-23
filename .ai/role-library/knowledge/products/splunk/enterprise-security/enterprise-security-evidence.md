# Splunk Enterprise Security source integration evidence

Use this reference for log-source onboarding, CIM coverage review or changes
to data model scope and performance assumptions in an ES deployment.

Pin the ES version, platform and mode, region where applicable, CIM and
source add-on versions, applicable support and exact data route. Record
required fields, tags and source-to-model mapping for the ES use case.
Observe representative events reaching the authorized index and data model,
record gaps and distinguish raw ingestion from normalized coverage. Use
bounded, redacted observations and explicit expectations for each test.

Review index scope and acceleration only when the target ES content or a
material performance requirement depends on them. Verify the procedure for
the actual product versions and administration model. The ES 8.8 data model guide identifies version-specific deployment considerations.

[ES 8.8 compatibility and regional availability](https://help.splunk.com/en/splunk-enterprise-security-8/release-notes-and-resources/8.8/splunk-enterprise-security-release-notes/compatibility-and-regional-availability)
[Configure ES 8.8 data models](https://help.splunk.com/en/splunk-enterprise-security-8/install/8.8/installation/configure-data-models-for-splunk-enterprise-security)
[CIM overview](https://help.splunk.com/en/data-management/common-information-model/8.8/introduction/overview-of-the-splunk-common-information-model)
