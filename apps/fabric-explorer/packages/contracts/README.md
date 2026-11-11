# Read-only model and consumer contracts

This package implements the [public contract specification](../../docs/contracts.md)
for the future broker, canonical-reader adapter, graph workers and UI. It
contains no Electron, renderer, filesystem reader, note store or canonical
permission evaluator. Build-time AJV compilation produces static ESM validators;
runtime import requires no `eval`, `Function` or Node built-in module.

Use the pinned toolchain from the application dependency baseline:

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm test
npm run test:built
```

Generation runs before build/check/tests. The one authored schema is
`schema/contracts.schema.json`; `generated/` and `dist/` are reproducible build
outputs. The package root exports runtime functions and types, while
`@jai/fabric-explorer-contracts/schema` exports the published JSON schema.
Application packaging consumes compiled runtime assets, not this source tree.

```ts
import {
  encodeSemantic,
  elementKey,
} from '@jai/fabric-explorer-contracts';

const reference = {
  engagement: 'synthetic-engagement',
  scope: 'synthetic-origin',
  logical_id: 'synthetic-source',
  version_id: '1'.repeat(64),
};
const key = elementKey({ kind: 'version', projectId: 'synthetic-project', ref: reference });
const semanticInteger = encodeSemantic(90071992547409931234567890n);
```

The example identifies local addressing and transport only; its synthetic
reference is not an admitted source version. `elementKey`/`edgeKey` encode local
tagged tuples and never compute source-domain hashes. Finding integers must
already be `bigint` or explicit integer tags before a JS boundary. Findings
float64 tags preserve big-endian IEEE-754 bits, including `1.0`, signed zero and
nonfinite values; lifecycle numeric rules remain separate.

Model assertions validate local shape/identity/provenance and do not authenticate
the supplied claims. `assertBinding` and `assertResponseForRequest` compare with
trusted retained receiver state; they cannot create or authenticate a capability.
`assertCancellationTarget` compares the actual retained target context. Cursor
tokens still require a broker-owned lookup. Inputs are not mutated or globally
frozen; readonly types and detached transport values are owned by each receiver.

Use `decodeChunkFrame` / `advanceChunks` for large query results. The pure
transition checks sequence, context, finite progress, terminal status and
cumulative visible limits. It does not assemble or publish a graph. The owning
consumer validates the fully staged projection with `assertProjection` before
publishing; endpoint/duplicate checks across chunks cannot be skipped. A model
can exceed one frame while each transmitted frame remains at most 8 MiB.

Tests use real validators and synthetic DTO goldens. They cover stable identities,
opaque semantic values, integer/float separation, source revision consistency,
closed operation-specific schemas, cursor/cancellation/generation binding,
limits, partial streams and exact raw bytes. The built-consumer check imports
the actual package, emitted declarations and its browser bundle with runtime
string code generation disabled. Typed consumer checks include readonly and
unknown-operation rejection. These tests do not qualify canonical replay, operating-system access,
desktop packaging or graphical readability.

Rollback removes the new package and consumers' imports. No source format or
stored annotation migration exists. Schema/API changes require compatibility
review and rerunning affected consumers. Failures carry typed, value-redacted
`ContractError` codes suitable for diagnostics without logging source payloads.

Recorded source observations use `mode: recorded` and `replay: recorded`, with decoded content but unknown chain and trust. Validators reject recorded metadata that claims verified replay, verified chains or fresh applicability. Historical `canonical-dependency` relation values retain their recorded classification meaning and do not assert that the viewer reverified source authority.
