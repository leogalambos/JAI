/** Disposable corpus worker; full corpus remains owned here across bounded projection requests. */
import { createCorpusService } from './corpus-service';
import type { CorpusRequest } from './corpus-service';
const handle = createCorpusService();
self.onmessage = (event: MessageEvent<CorpusRequest>) => {
  try { self.postMessage(handle(event.data)); }
  catch (error) { self.postMessage({ requestId: event.data.requestId, error: String(error) }); }
};
