// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only operator review state; Czech prompts are explicitly requested by the operator. */
export type ReviewStatus = 'unknown' | 'pass' | 'fail';
/** One concrete task, rather than an overlapping list of commands for different windows. */
export interface ReviewTask { readonly id: string; readonly title: string; readonly instruction: string; readonly expected: string }
/** Actual confirmed observation; never inferred from visiting a step. */
export interface ReviewAnswer { readonly id: string; readonly status: ReviewStatus; readonly notes: string }
/** Four practical checks; sound-based assistive technology is outside the operator-approved scope. */
export const REVIEW_TASKS: readonly ReviewTask[] = Object.freeze([
  { id: 'panes', title: 'Rozložení okna a rozsah grafu', instruction: 'Stiskněte „Přejít do prohlížeče“. V okně Fabric Explorer zkontrolujte graf uprostřed a podpůrné panely po stranách. V záhlaví grafu porovnejte celkové počty s počty právě zobrazeného okolí. Pro návrat k tomuto formuláři stiskněte F8.', expected: 'Graf není odsunutý pod dlouhý seznam informací. Je jasné, že jde o omezené okolí vybraného uzlu, nikoliv o všechny importované záznamy. U posuvných panelů je vidět možnost posunu.' },
  { id: 'zoom-labels', title: 'Přiblížení a názvy uzlů', instruction: 'V okně Fabric Explorer použijte kolečko myši nebo tlačítko „Zoom in“. Přibližte skupinu materiálových uzlů tak, abyste rozeznal jednotlivé uzly a jejich popisky. Vyberte jeden uzel a prohlédněte jeho detail. Tlačítkem „Fit graph“ lze vrátit celý graf do záběru. Potom se vraťte klávesou F8.', expected: 'Přiblížení dovolí uzly oddělit. Nejsou zobrazené jako jediná dlouhá svislá řada. Primární názvy materiálů jsou krátké a rozlišitelné; úplný identifikátor zůstává dostupný v detailu.' },
  { id: 'scroll-focus', title: 'Posuvné panely a klávesnice', instruction: 'V okně Fabric Explorer posuňte obsah navigace, seznamu prvků a detailu. Potom několikrát použijte Tab a Shift+Tab a sledujte zvýraznění zaměřeného ovládacího prvku. Vraťte se klávesou F8.', expected: 'Panely lze posouvat samostatně a jejich obsah není nedostupný za okrajem. Při nedostatku šířky lze pracovní plochu posunout vodorovně. Zaměření klávesnice je viditelné a nezůstane skryté mimo záběr.' },
  { id: 'relation', title: 'Čitelný detail vztahu', instruction: 'V okně Fabric Explorer přepněte seznam „List“ na „Relations“ a vyberte vztah. V detailu přečtěte jeho název a oba koncové uzly, směr „From → To“ a podklad vztahu. Pokud potřebujete přesný identifikátor, rozbalte jeho detail. Vraťte se klávesou F8 a uložte výsledek.', expected: 'Vztah a jeho směr lze pochopit bez luštění dlouhého hashe. Popisek vybraného vztahu se dá přečíst a podstatné informace ani ovládací prvky se nepřekrývají.' },
]);
/** Confirmed review state is separate from unsubmitted form drafts and interruption evidence. */
export class OperatorReview {
  private position = 0;
  private readonly answers: ReviewAnswer[] = REVIEW_TASKS.map(task => ({ id: task.id, status: 'unknown', notes: '' }));
  /** Current zero-based page; moving alone never changes an answer. */
  get index(): number { return this.position; }
  /** Current concrete task. */
  get task(): ReviewTask { return REVIEW_TASKS[this.position]!; }
  /**
   * Confirm a direct human observation, requiring evidence for Pass and Fail.
   * @param status Explicit closed status value from the form.
   * @param notes Human explanation, including limitations for unknown observations.
   * @throws {Error} For an invented status or a claimed observation without a note.
   */
  answer(status: string, notes: string): void {
    if (!['unknown', 'pass', 'fail'].includes(status) || status !== 'unknown' && !notes.trim()) throw new Error('Invalid or unsupported observation');
    this.answers[this.position] = { id: this.task.id, status: status as ReviewStatus, notes: notes.trim() };
  }
  /**
   * Move to an existing step without clearing confirmed observations.
   * @param index Integer index within the four-step denominator.
   * @throws {RangeError} For an absent step.
   */
  move(index: number): void { if (!Number.isInteger(index) || index < 0 || index >= REVIEW_TASKS.length) throw new RangeError('Invalid review step'); this.position = index; }
  /** Return detached observations; external form state cannot rewrite recorded results. */
  snapshot(): ReviewAnswer[] { return this.answers.map(answer => ({ ...answer })); }
  /**
   * Classify explicit answers and optionally the actual renderer execution without rewriting human observations.
   * @param consoleErrors Unexpected renderer errors; omit only when requesting the human-observation outcome.
   * @returns Failed for an observed failure or runtime error, passed only for complete clean evidence.
   */
  outcome(consoleErrors: readonly string[] = []): 'passed' | 'failed' | 'incomplete' { return consoleErrors.length || this.answers.some(answer => answer.status === 'fail') ? 'failed' : this.answers.every(answer => answer.status === 'pass') ? 'passed' : 'incomplete'; }
}
