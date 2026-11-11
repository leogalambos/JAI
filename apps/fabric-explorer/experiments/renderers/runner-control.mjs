/** Disposable finite-plan control. Functional deadline tests inject the scheduler. */
export const stages = [
  ['Load graph', 'Automatic load test. The dense graph is deliberately not intended for human inspection.'],
  ['Check identities', 'Automatic checks of selected vertex and relation metadata. No action is required.'],
  ['Measure pan and zoom', 'Automatic 20-second load sample. Leave the graph alone until manual review begins.'],
  ['Check expansion', 'Automatic bounded expansion and grouping. No action is required.'],
  ['Check cancellation', 'Automatic cancellation check. No action is required.'],
  ['Review readable example', 'The graph now has only two vertices and four relations. Complete the checks in this window, then Save or Skip.'],
  ['Check context loss', 'Automatic context-loss observation. Recovery is not inferred as passing.'],
  ['Save case', 'Saving observations before the next numbered case.'],
];

/**
 * Create the finite candidate/scale plan without admitting duplicate scales.
 * @param {number[]} scales Distinct supported display scales.
 * @param {string} selection Explicit sigma/cytoscape focus or both candidates.
 * @returns {object[]} Ordered candidate/scale cases.
 * @throws {Error} If the scale list is empty or contains duplicates.
 */
export function createPlan(scales, selection = 'both') {
  if (!scales.length || new Set(scales).size !== scales.length) throw new Error('A nonempty set of distinct display scales is required');
  if (!['sigma', 'cytoscape', 'both'].includes(selection)) throw new Error('Renderer selection must be sigma, cytoscape or both');
  const renderers = selection === 'both' ? ['sigma', 'cytoscape'] : [selection];
  return renderers.flatMap(renderer => scales.map(scale => ({ renderer, scale })));
}

/**
 * Create idempotent cancellation and bounded asynchronous operations.
 * @param {object} options Callbacks and an injectable timer scheduler.
 * @param {Function} options.onStop Called exactly once on a whole-run stop.
 * @param {Function} options.setTimer Schedules an automatic-work watchdog.
 * @param {Function} options.clearTimer Cancels a watchdog.
 * @returns {object} Shared cancellation state and operation wrapper.
 */
export function createRunControl(options = {}) {
  const { onStop = () => {}, setTimer = setTimeout, clearTimer = clearTimeout } = options;
  const aborter = new AbortController();
  let reason = null;
  let failed = false;
  const pendingResources = new Set();
  const cleanupErrors = [];
  const stop = (value = 'operator-stop', failure = false) => {
    if (aborter.signal.aborted) return false;
    reason = value; failed = failure;
    aborter.abort(); onStop(value); return true;
  };
  const stoppedError = () => Object.assign(new Error(reason ?? 'Run stopped'), { name: 'AbortError' });
  const check = () => { if (aborter.signal.aborted) throw stoppedError(); };
  const operation = (label, action, timeoutMs = null, disposeLateValue) => {
    check();
    return new Promise((resolve, reject) => {
      let timer;
      const cleanup = () => { aborter.signal.removeEventListener('abort', cancelled); if (timer !== undefined) clearTimer(timer); };
      const cancelled = () => { cleanup(); reject(stoppedError()); };
      aborter.signal.addEventListener('abort', cancelled, { once: true });
      if (timeoutMs !== null) timer = setTimer(() => {
        cleanup();
        const error = Object.assign(new Error(`${label} exceeded its ${timeoutMs} ms watchdog; run stopped without retry`), { name: 'ProbeTimeoutError' });
        reject(error); stop(`timeout: ${label}`, true);
      }, timeoutMs);
      const completion = Promise.resolve().then(() => { check(); return action(); }).then(async value => {
        cleanup();
        if (aborter.signal.aborted) {
          if (disposeLateValue) {
            try { await disposeLateValue(value); }
            catch (error) { cleanupErrors.push(`${label}: ${error}`); }
          }
          reject(stoppedError());
        } else resolve(value);
      }, error => {
        cleanup();
        if (error?.name === 'AbortError') stop('operation-cancelled');
        reject(error);
      });
      if (disposeLateValue) {
        pendingResources.add(completion);
        void completion.finally(() => pendingResources.delete(completion));
      }
    });
  };
  return { stop, check, operation, settleResources: () => Promise.all([...pendingResources]), cleanupErrors,
    get stopped() { return aborter.signal.aborted; }, get reason() { return reason; }, get failed() { return failed; } };
}

/**
 * Admit no later case after cancelled or failed infrastructure.
 * @param {object[]} plan Ordered finite cases.
 * @param {object} control Shared run cancellation controller.
 * @param {Function} execute Executes one case and records any failure.
 * @returns {Promise<void>} Resolves after the admitted cases end.
 */
export async function executePlan(plan, control, execute) {
  for (let index = 0; index < plan.length; index++) {
    if (control.stopped) break;
    await execute(plan[index], index + 1, plan.length);
  }
}
