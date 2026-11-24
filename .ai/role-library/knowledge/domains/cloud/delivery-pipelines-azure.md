<!-- SPDX-License-Identifier: BSD-4-Clause -->
<!-- Copyright (c) 2026 Leo Galambos and the Egothor team -->

# Microsoft Azure governed cloud delivery pipelines

Repository-to-deployment CI/CD using an explicitly supported Microsoft Azure target.

Use Azure Repos, Azure Pipelines and Azure Artifacts for applicable package feeds. Publish immutable pipeline evidence and promote the same image digest from Azure Container Registry to Container Apps. Configure environment approvals outside pipeline YAML. Scope the workload identity federation service connection and verify the previous revision and traffic allocation for reversal. Record whether Boards and Test Plans are applicable.

[Azure Pipelines approvals and checks](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals)
