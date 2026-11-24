<!-- SPDX-License-Identifier: BSD-4-Clause -->
<!-- Copyright (c) 2026 Leo Galambos and the Egothor team -->

# Google Cloud governed cloud delivery pipelines

Repository-to-deployment CI/CD using an explicitly supported AWS, Azure DevOps Services or Google Cloud target.

Use Secure Source Manager or a supported Cloud Build repository connection. Cloud Source Repositories requires existing eligibility. Build in Cloud Build, store immutable images in Artifact Registry and promote the same Cloud Deploy release to its Cloud Run target. Bind release and rollout IDs, execution identity and previous successful release for rollback.

[Deploy your application](https://docs.cloud.google.com/deploy/docs/deploying-application)

