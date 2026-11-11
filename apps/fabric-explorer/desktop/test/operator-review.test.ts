// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Human-evidence safety: navigation, interruption and unconfirmed drafts cannot manufacture a pass. */
import { describe, expect, it } from 'vitest';
import { OperatorReview, REVIEW_TASKS } from './operator-review.js';
describe('explicit operator observations', () => {
  it('retains unknown results when every page has merely been visited', () => {
    const review = new OperatorReview(); for (let index = 0; index < REVIEW_TASKS.length; index++) review.move(index);
    expect(review.outcome()).toBe('incomplete'); expect(review.snapshot().every(answer => answer.status === 'unknown')).toBe(true);
  });
  it('requires actual notes for both claimed success and failure without altering the old answer', () => {
    const review = new OperatorReview();
    for (const status of ['pass', 'fail', 'invented']) expect(() => review.answer(status, '  ')).toThrow();
    expect(review.snapshot()[0]?.status).toBe('unknown');
  });
  it('preserves an earlier answer through next and back', () => {
    const review = new OperatorReview(); review.answer('fail', 'The selected label is obscured.'); review.move(1); review.move(0);
    expect(review.snapshot()[0]).toMatchObject({ status: 'fail', notes: 'The selected label is obscured.' }); expect(review.outcome()).toBe('failed');
  });
  it('allows an unknown observation with no invented speech or environment requirement', () => {
    const review = new OperatorReview(); review.answer('unknown', ''); expect(review.outcome()).toBe('incomplete');
  });
  it('cannot be rewritten by a mutable exported snapshot', () => {
    const review = new OperatorReview(); (review.snapshot()[0] as { status: string }).status = 'pass'; expect(review.snapshot()[0]?.status).toBe('unknown');
  });
  it('requires every explicit observed pass before returning passed', () => {
    const review = new OperatorReview();
    REVIEW_TASKS.forEach((_task, index) => { review.move(index); review.answer('pass', 'Directly observed the required result.'); });
    expect(review.outcome()).toBe('passed');
  });
  it('retains human passes but rejects an execution with an unexpected renderer error', () => {
    const review = new OperatorReview();
    REVIEW_TASKS.forEach((_task, index) => { review.move(index); review.answer('pass', 'Directly observed the required result.'); });
    const executionOutcome: (errors?: readonly string[]) => string = review.outcome.bind(review);
    expect(executionOutcome(['Sigma: Container has no width.'])).toBe('failed');
    expect(review.snapshot().every(answer => answer.status === 'pass')).toBe(true);
    expect(review.outcome()).toBe('passed');
  });
  it('rejects nonexistent steps without discarding observations', () => {
    const review = new OperatorReview(); for (const index of [-1, 0.5, REVIEW_TASKS.length]) expect(() => review.move(index)).toThrow(); expect(review.index).toBe(0);
  });
});
