<!-- SPDX-License-Identifier: BSD-4-Clause -->
<!-- Copyright (c) 2026 Leo Galambos and the Egothor team -->

# Terraform governed plans and state

Terraform infrastructure engineering for an explicitly selected tool version, providers and backend.

## Constraints

Pin Terraform, provider constraints and lock file checksums. Version reusable modules with declared inputs, outputs and upgrade tests. Verify provider and backend support in the exact account, region and tool version.

[Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)

## State

Assign ownership of a versioned and access-controlled state backend. Confirm that the backend supports locking and establish an incident procedure for lock recovery. Minimize sensitive values and protect state and saved plan material as sensitive.

[Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)

## Promotion

Validate and review the saved plan before effect. Bind its digest to the source and provider lock file, state identity, target environment and reviewed change scope. Replan after drift or a changed input. Apply the exact saved plan only with applicable prior authority and collect reconciliation and recovery evidence.

[Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)
