<!-- SPDX-License-Identifier: BSD-4-Clause -->
<!-- Copyright (c) 2026 Leo Galambos and the Egothor team -->

# AWS governed cloud delivery pipelines

Repository-to-deployment CI/CD using an explicitly supported AWS target.

Use CodeCommit where eligible or a supported external repository connection through CodeConnections. CodePipeline orchestrates CodeBuild and the ECS standard deploy action for this path. Store container images in Amazon ECR and use CodeArtifact for applicable packages. Bind image digest to deployment input and record the previous completed task definition and circuit breaker outcome. Check CodeDeploy separately for service and deployment controller combinations using blue-green.

[Amazon ECS standard deployment action](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-ECS.html)
