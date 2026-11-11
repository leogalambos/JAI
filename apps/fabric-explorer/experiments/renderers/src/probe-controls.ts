/** Disposable guided test controls; progress/feedback are separate from benchmark verdicts. */
import { observationCriteria, parseOperatorObservation } from '../operator-observation.mjs';
import type { OperatorObservation } from '../operator-observation.mjs';

/** One runner-issued position within a finite case/stage plan. */
export type ProbeProgress = {
  caseIndex: number; caseCount: number; stageIndex: number; stageCount: number;
  renderer: string; scale: number; title: string; instructions: string;
  mode: 'automatic' | 'manual' | 'stopping' | 'complete' | 'failed';
  remainingMs?: number;
};
type ProgressText = { case: string; stage: string; overall: string; title: string; instructions: string; mode: string };
type Handlers = { save(): void; skip(): void; stop(reason: string): void };
type View = {
  renderProgress(value: ProgressText): void; renderCountdown(value: string): void;
  showReview(visible: boolean): void; readReview(): { answers: Record<string, string>; note: string };
  resetReview(): void; disableReview(disabled: boolean): void;
  showStopping(reason: string): void; showReviewError(message: string): void;
  bind(handlers: Handlers): void;
};
type Environment = {
  now(): number; timestamp(): string;
  setInterval(callback: () => void, milliseconds: number): unknown;
  clearInterval(handle: unknown): void; requestStop(reason: string): void | Promise<unknown>;
};
/** Local progress/feedback operations; Stop rejects pending feedback and notifies the runner once. */
export type ProbeControls = { setProgress(progress: ProbeProgress): void; review(): Promise<OperatorObservation>; stop(reason: string): void };

/**
 * Render finite, validated counters; source counts never act as case progress.
 * @param progress Current one-based case/stage and declared totals.
 * @returns Human-readable counters and phase instructions.
 * @throws {Error} If counters are invalid or exceed their totals.
 */
export function progressText(progress: ProbeProgress): ProgressText {
  for (const value of [progress.caseIndex, progress.caseCount, progress.stageIndex, progress.stageCount]) {
    if (!Number.isInteger(value) || value < 1) throw new Error('Positive finite case/stage counters required');
  }
  if (progress.caseIndex > progress.caseCount || progress.stageIndex > progress.stageCount) throw new Error('Case/stage exceeds declared total');
  return {
    case: `Case ${progress.caseIndex} of ${progress.caseCount} · ${progress.renderer} · ${Math.round(progress.scale * 100)}%`,
    stage: `Step ${progress.stageIndex} of ${progress.stageCount}: ${progress.title}`,
    overall: `Overall step ${(progress.caseIndex - 1) * progress.stageCount + progress.stageIndex} of ${progress.caseCount * progress.stageCount}`,
    title: progress.title, instructions: progress.instructions, mode: progress.mode,
  };
}

/**
 * Control a visible progress view with injected time; tests need no native browser.
 * @param view Local presentation and feedback event adapter.
 * @param environment Injected clock, scheduler, timestamp and fixed Stop callback.
 * @returns A controller that preserves unknown feedback and stops idempotently.
 * @throws {Error} If the view's event binding fails.
 */
export function createProbeControls(view: View, environment: Environment): ProbeControls {
  let timer: unknown;
  let stopped = false;
  let pending: { resolve(value: OperatorObservation): void; reject(error: Error): void } | undefined;
  const abort = () => Object.assign(new Error('Test stopped by the operator'), { name: 'AbortError' });
  const clearCountdown = () => {
    if (timer !== undefined) environment.clearInterval(timer);
    timer = undefined;
  };
  const finishReview = (skip: boolean) => {
    if (!pending || stopped) return;
    try {
      const values = view.readReview();
      const result = parseOperatorObservation(skip ? '' : JSON.stringify({ ...values.answers, note: values.note }), environment.timestamp());
      if (skip) result.method = 'operator-skipped';
      const response = pending; pending = undefined;
      view.showReview(false);
      response.resolve(result);
    } catch (error) { view.showReviewError(String(error)); }
  };
  const controls: ProbeControls = {
    setProgress(progress) {
      if (stopped) return;
      const text = progressText(progress);
      clearCountdown();
      view.renderProgress(text);
      view.showReview(false);
      view.renderCountdown('');
      if (progress.remainingMs !== undefined) {
        if (!Number.isFinite(progress.remainingMs) || progress.remainingMs < 0) throw new Error('Finite countdown required');
        const started = environment.now();
        const update = () => {
          const seconds = Math.ceil(Math.max(0, progress.remainingMs! - (environment.now() - started)) / 1000);
          view.renderCountdown(seconds ? `${seconds} s remaining` : '0 s — finishing measurement');
          if (!seconds) clearCountdown();
        };
        update();
        if (progress.remainingMs > 0) timer = environment.setInterval(update, 1000);
      }
    },
    review() {
      if (stopped) return Promise.reject(abort());
      if (pending) return Promise.reject(new Error('A manual review is already pending'));
      clearCountdown();
      view.renderCountdown('Your action is required — no automatic time limit');
      view.resetReview(); view.disableReview(false); view.showReview(true);
      return new Promise((resolve, reject) => { pending = { resolve, reject }; });
    },
    stop(reason) {
      if (stopped) return;
      stopped = true; clearCountdown();
      view.disableReview(true); view.showStopping(reason);
      const response = pending; pending = undefined;
      response?.reject(abort());
      void Promise.resolve(environment.requestStop(reason)).catch(() => {
        view.showStopping('The local test is stopped. You may close this window.');
      });
    },
  };
  view.bind({ save: () => finishReview(false), skip: () => finishReview(true), stop: reason => controls.stop(reason) });
  return controls;
}

const labels: Record<string, { title: string; task: string }> = {
  vertexPointerPicking: { title: 'Vertex selection', task: 'Click each of the two vertices. Does Selected element show v0 and v1?' },
  vertexLabelReadability: { title: 'Vertex labels', task: 'Can you read the selected vertex label completely?' },
  edgeLabelReadability: { title: 'Relation labels', task: 'Click a relation. Can you read its full label in Selected element?' },
  edgeCanvasLabelReadability: { title: 'Labels directly on graph relations', task: 'Click e0, e1, e2 and e3. Can you read each selected label directly on its edge in the graph, rather than only in Selected element?' },
  parallelEdgePicking: { title: 'Two parallel relations', task: 'Click both curves separately. Check that one selects e0 and the other e1.' },
  selfLoopPicking: { title: 'Self-loop selection', task: 'Click the loop returning to the same vertex. Check that it selects e2.' },
  arrowDirection: { title: 'Arrow direction', task: 'Check arrows from v0 to v1, the reverse e3, and the self-loop.' },
};

/**
 * Attach controls to local DOM; Stop exposes only one fixed runner binding.
 * @param document Local test page containing the required control elements.
 * @param target Browser window for time, keyboard events and the fixed runner binding.
 * @returns Controls ready for runner-issued progress and manual review.
 * @throws {Error} If required elements or criterion descriptions are missing.
 */
export function installProbeControls(document: Document, target: Window, reviewScope = 'all'): ProbeControls {
  const element = <T extends HTMLElement>(id: string) => {
    const value = document.getElementById(id);
    if (!value) throw new Error(`Missing guided probe control: ${id}`);
    return value as T;
  };
  const review = element<HTMLFormElement>('probe-review');
  const questions = element<HTMLElement>('probe-questions');
  const selectors = new Map<string, HTMLSelectElement>();
  for (const criterion of observationCriteria) {
    if (reviewScope === 'labels' && !['edgeLabelReadability', 'edgeCanvasLabelReadability'].includes(criterion)) continue;
    const description = labels[criterion];
    if (!description) throw new Error(`Missing manual criterion description: ${criterion}`);
    const field = document.createElement('fieldset');
    const legend = document.createElement('legend'); legend.textContent = description.title;
    const task = document.createElement('p'); task.textContent = description.task;
    const answer = document.createElement('select'); answer.name = criterion; answer.setAttribute('aria-label', description.title);
    for (const [value, label] of [['unknown', 'Not checked'], ['pass', 'Pass'], ['fail', 'Fail']]) {
      const option = document.createElement('option'); option.value = value; option.textContent = label; answer.append(option);
    }
    selectors.set(criterion, answer); field.append(legend, task, answer); questions.append(field);
  }
  const note = element<HTMLTextAreaElement>('probe-note');
  const save = element<HTMLButtonElement>('probe-save');
  const skip = element<HTMLButtonElement>('probe-skip');
  const stop = element<HTMLButtonElement>('probe-stop');
  const view: View = {
    renderProgress(value) {
      element('probe-case').textContent = value.case;
      element('probe-stage').textContent = value.stage;
      element('probe-overall').textContent = value.overall;
      element('probe-instructions').textContent = value.instructions;
      element('probe-progress').dataset.mode = value.mode;
      document.title = `${value.case} — ${value.title}`;
    },
    renderCountdown(value) { element('probe-countdown').textContent = value; },
    showReview(visible) { review.hidden = !visible; if (visible) element('probe-review-title').focus(); },
    readReview() { return { answers: Object.fromEntries([...selectors].map(([key, select]) => [key, select.value])), note: note.value }; },
    resetReview() { for (const select of selectors.values()) select.value = 'unknown'; note.value = ''; element('probe-review-error').textContent = ''; },
    disableReview(disabled) { for (const select of selectors.values()) select.disabled = disabled; note.disabled = disabled; save.disabled = disabled; skip.disabled = disabled; },
    showStopping(reason) {
      stop.disabled = true; element('probe-progress').dataset.mode = 'stopping';
      element('probe-stage').textContent = 'Stopping the complete test';
      element('probe-countdown').textContent = '';
      element('probe-instructions').textContent = `${reason}. No further cases will start. Saving the partial report and closing browser resources.`;
    },
    showReviewError(message) { element('probe-review-error').textContent = message; },
    bind(handlers) {
      review.addEventListener('submit', event => { event.preventDefault(); handlers.save(); });
      skip.addEventListener('click', () => handlers.skip());
      stop.addEventListener('click', () => handlers.stop('Stop button pressed'));
      target.addEventListener('keydown', event => { if (event.key === 'Escape') { event.preventDefault(); handlers.stop('Escape pressed'); } });
    },
  };
  return createProbeControls(view, {
    now: () => target.performance.now(), timestamp: () => new Date().toISOString(),
    setInterval: (callback, milliseconds) => target.setInterval(callback, milliseconds),
    clearInterval: handle => target.clearInterval(handle as number),
    requestStop: reason => {
      const runner = target as Window & { requestProbeStop?: (reason: string) => Promise<unknown> };
      return runner.requestProbeStop ? runner.requestProbeStop(reason) : Promise.reject(new Error('Runner binding unavailable'));
    },
  });
}
