/** Compile-time consumer of emitted declarations; unused expected errors fail the type contract check. */
import { PROTOCOL, encodeFrame, elementKey } from '@jai/fabric-explorer-contracts';
import type { ElementIdentity, Operation, Request } from '@jai/fabric-explorer-contracts';

const identity: ElementIdentity = { kind: 'finding', projectId: 'synthetic-project', ledgerId: 'synthetic-review', findingId: 'F-0001' };
elementKey(identity);
const request: Request = {
  protocol: PROTOCOL, kind: 'request', requestId: 'synthetic-request',
  binding: { sessionId: 'synthetic-session', capability: null, generation: null },
  operation: 'roots.pick', payload: { families: ['fabric', 'findings'] },
};
encodeFrame(request);

// @ts-expect-error Consumer identities cannot be rewritten through the public type.
identity.projectId = 'another-project';
// @ts-expect-error Correlation identifiers are immutable after construction.
request.requestId = 'another-request';
// @ts-expect-error Root selection families are an immutable collection.
request.payload.families.push('audit');
// @ts-expect-error No source-writing operation exists in the public operation union.
const mutation: Operation = 'source.write';
void mutation;
