# IT landscape (from the client's architecture overview)

## Platform
Payments API on AWS: API Gateway, Lambda, DynamoDB, KMS for card token encryption. Logs in CloudWatch.

## Identity
Staff sign in through Google Workspace. Partners authenticate with static API keys issued manually.

## Operations
No dedicated security operations team; alerts go to the platform engineers' shared channel.
