// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Four-step Czech visual/keyboard collector; the operator explicitly excluded sound-reader testing. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { isAbsolute, join } from 'node:path';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { BrowserWindow } from 'electron';
import { accessibilityFixture, accessibilityHost } from './accessibility-host.js';
import { NativeExit } from './native-exit.js';
import { OperatorReview, REVIEW_TASKS } from './operator-review.js';
import { app } from 'electron';
const termination = new NativeExit(code => app.exit(code));
const destination = process.argv.at(-1);
if (!destination || !isAbsolute(destination) || destination.endsWith('.cjs')) throw new Error('An absolute observation destination is required');
const output = join(destination, 'manual-visual'); mkdirSync(output, { mode: 0o700 });
let fixture: ReturnType<typeof accessibilityFixture>; const state = new OperatorReview();
const drafts = new Map<string, Record<string, string>>(); let production: BrowserWindow; let review: BrowserWindow;
const errors: string[] = []; let stopping = false;
const digest = (value: Buffer) => createHash('sha256').update(value).digest('hex');
const escapeHtml = (value: string) => value.replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]!);
const save = (name: string, extra: Record<string, unknown> = {}) => writeFileSync(join(output, name), JSON.stringify({ format: 'jai.fabric-explorer.operator-review/1', at: new Date().toISOString(), platform: process.platform, electron: process.versions.electron, observationsOutcome: state.outcome(), outcome: state.outcome(errors), consoleErrors: errors, observations: state.snapshot(), drafts: Object.fromEntries(drafts), ...extra }, null, 2) + '\n');
async function evaluate<T>(body: string): Promise<T> { return production.webContents.executeJavaScript(`(async()=>{${body}})()`); }
async function wait(expression: string, label: string, maximum = 15000): Promise<void> {
  assert.equal(await evaluate<boolean>(`const end=performance.now()+${maximum};while(performance.now()<end){if(${expression})return true;await new Promise(resolve=>requestAnimationFrame(resolve));}return false;`), true, label);
}
async function click(selector: string): Promise<void> { if (['#tab-sources', '#tab-search', '#tab-findings', '#show-elements'].includes(selector) && await evaluate<boolean>("return !!document.querySelector('.navigation-pane')?.hidden;")) await click('#show-navigation'); if (selector.startsWith('#inspector-tab-') && await evaluate<boolean>("return !!document.querySelector('.inspector')?.hidden;")) await click('#show-inspector'); await evaluate(`const element=document.querySelector(${JSON.stringify(selector)});if(!element||element.disabled||!element.getClientRects().length)throw new Error('Required enabled control unavailable');element.click();`); }
async function value(selector: string, text: string): Promise<void> {
  await evaluate(`const element=document.querySelector(${JSON.stringify(selector)});if(!element||!element.getClientRects().length)throw new Error('Required input unavailable');Object.getOwnPropertyDescriptor(element.tagName==='SELECT'?HTMLSelectElement.prototype:HTMLInputElement.prototype,'value').set.call(element,${JSON.stringify(text)});element.dispatchEvent(new Event(element.tagName==='SELECT'?'change':'input',{bubbles:true}));`);
}
async function showReview(): Promise<void> { if (review.isMinimized()) review.restore(); review.show(); review.focus(); }
async function capture(name: string): Promise<void> {
  await evaluate('await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));');
  writeFileSync(join(output, `${name}.png`), (await production.webContents.capturePage()).toPNG());
}
async function renderStep(): Promise<void> {
  const task = state.task; const answer = drafts.get(task.id) ?? state.snapshot()[state.index]!;
  const html = `<h1 tabindex="-1">Krok ${state.index + 1} ze ${REVIEW_TASKS.length}: ${escapeHtml(task.title)}</h1><p>${escapeHtml(task.instruction)}</p><h2>Co má být vidět</h2><p>${escapeHtml(task.expected)}</p><p><strong>F8</strong> v okně Fabric Explorer vás vrátí sem (na notebooku případně Fn+F8). Lze také obnovit okno „Kontrola vieweru“ z lišty systému. Tlačítko níže otevře prohlížeč a tento formulář minimalizuje.</p><button type="button" data-action="viewer">Přejít do prohlížeče</button><form><label>Výsledek <select name="status"><option value="unknown">Neověřeno</option><option value="pass">V pořádku — ověřil jsem</option><option value="fail">Nefunguje — ověřil jsem</option></select></label><label>Co jste skutečně viděl <textarea name="notes">${escapeHtml(answer.notes ?? '')}</textarea></label><div class="actions"><button type="button" data-action="back" ${state.index === 0 ? 'disabled' : ''}>Předchozí krok</button><button type="submit" data-action="next">${state.index === REVIEW_TASKS.length - 1 ? 'Uložit výsledky a skončit' : 'Zapsat výsledek a další krok'}</button><button type="button" data-action="stop">Přerušit a uložit rozpracované výsledky</button></div></form><p>Kontrolují se pouze syntetická data. Orca není potřeba. Bez vašeho potvrzení se nic neoznačí jako úspěšné. Zavření kteréhokoliv okna nebo Ctrl+C test ukončí.</p>`;
  await review.webContents.executeJavaScript(`document.body.innerHTML=${JSON.stringify(html)};document.querySelector('select').value=${JSON.stringify(answer.status ?? 'unknown')};document.querySelector('h1').focus();document.title=${JSON.stringify(`Kontrola vieweru — krok ${state.index + 1}/4`)};`);
  review.setTitle(`Kontrola vieweru — krok ${state.index + 1}/4`);
  console.log(`Ruční kontrola: krok ${state.index + 1}/${REVIEW_TASKS.length} — ${task.title}`);
}
async function readAction(): Promise<{ kind: string; values: Record<string, string> }> {
  return review.webContents.executeJavaScript(`new Promise(resolve=>{const listener=event=>{const button=event.target.closest('button[data-action]');if(!button||button.disabled)return;event.preventDefault();const form=document.querySelector('form');form.querySelector('textarea').required=button.dataset.action==='next'&&form.querySelector('select').value!=='unknown';if(button.dataset.action==='next'&&!form.reportValidity())return;document.removeEventListener('click',listener);resolve({kind:button.dataset.action,values:Object.fromEntries(new FormData(form))});};document.addEventListener('click',listener);})`);
}
async function finishReview(): Promise<void> {
  assert.deepEqual(readFileSync(fixture.fabric), fixture.originalFabric, 'Viewer changed synthetic Fabric input');
  assert.deepEqual(readFileSync(fixture.findings), fixture.originalFindings, 'Viewer changed synthetic findings input');
  const environment = await evaluate('return {pixelRatio:window.devicePixelRatio, viewport:{width:innerWidth,height:innerHeight}, theme:document.documentElement.dataset.theme};');
  await capture('final-viewer');
  save('observations.json', { environment, actualZoomFactor: production.webContents.getZoomFactor(), consoleErrors: errors, sourceIntegrity: 'unchanged', inputDigests: { fabric: digest(fixture.originalFabric), findings: digest(fixture.originalFindings) }, preparation: 'automatic synthetic picker/import/role-routing neighbourhood; not manual source-admission evidence', scope: 'four explicit visual/keyboard observations; no sound-reader, security, performance or cross-platform claim' });
  const outcome = state.outcome(errors); console.log(`Výsledky uloženy: ${state.snapshot().filter(answer => answer.status === 'pass').length}/4 v pořádku; celkový stav ${outcome}; chyb rendereru: ${errors.length}.`);
  termination.finish(outcome === 'passed' ? 0 : outcome === 'failed' ? 1 : 2);
}
async function run(): Promise<void> {
  const watchdog = setTimeout(() => { save('failure.json', { error: 'Automatic setup exceeded 60 seconds' }); termination.finish(2); }, 60000);
  console.log('Příprava 1/4: otevření skutečného vieweru se syntetickým výběrem zdrojů.');
  fixture = accessibilityFixture(__dirname, output);
  production = await accessibilityHost(__dirname, fixture, false);
  production.webContents.on('console-message', event => { if (event.level === 'error') errors.push(event.message); });
  await wait("document.querySelector('#open')&&!document.querySelector('#open').disabled", 'Source controls ready');
  console.log('Příprava 2/4: automatické načtení syntetických dat; žádný ruční výběr souborů.');
  await click('#open');
  await wait("document.querySelector('.semantic-panel tbody button') && document.querySelector('#cancel').disabled", 'Initial snapshot', 30000);
  console.log('Příprava 3/4: zobrazení ověřeného okolí role-routing; celkové počty a výřez grafu se liší.');
  await click('#tab-search'); await value('#search-text', 'role-routing'); await evaluate("document.querySelector('#search-text').form.requestSubmit();");
  await wait("Array.from(document.querySelector('#search-text').form.closest('section').querySelectorAll('.results button')).some(button=>button.querySelector('small')?.textContent==='version')", 'Recorded seed search');
  await evaluate("Array.from(document.querySelector('#search-text').form.closest('section').querySelectorAll('.results button')).find(button=>button.querySelector('small')?.textContent==='version').click();");
  await wait("!document.querySelector('#expand').disabled", 'Seed selection'); await evaluate("const options=document.querySelector('#direction').closest('details');if(options)options.open=true;"); await value('#direction', 'both'); await value('#hops', '1'); await evaluate("const options=document.querySelector('#direction').closest('details');if(options)options.open=false;"); await click('#expand'); await click('#show-elements'); await value('#element-kind', 'vertices');
  await wait("document.querySelector('.semantic-panel table')?.getAttribute('aria-rowcount')==='306'&&document.querySelector('.graph-canvas canvas')&&!document.querySelector('#fit-graph').disabled", 'Bounded 305-vertex visual review', 30000);
  production.webContents.setZoomFactor(1); await click('#menu-file'); await click('#preferences-open'); await value('#theme', 'light'); await click('#save'); await wait("document.documentElement.dataset.theme==='light'&&!document.querySelector('.preferences-dialog')?.open", 'Light baseline'); await click('#fit-graph');
  clearTimeout(watchdog);
  console.log('Příprava 4/4: hotovo. Následují čtyři ruční kroky, bez animace a bez časového limitu.');
  review = new BrowserWindow({ title: 'Kontrola vieweru', width: 760, height: 800, webPreferences: { sandbox: true, contextIsolation: true, nodeIntegration: false, webSecurity: true, devTools: false } });
  review.webContents.setWindowOpenHandler(() => ({ action: 'deny' })); review.webContents.on('will-navigate', event => event.preventDefault());
  await review.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent('<!doctype html><html lang="cs"><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; form-action \'none\'"><title>Kontrola vieweru</title><style>body{font:16px system-ui;line-height:1.6;margin:24px;color:#152d42;background:#fff}h1{font-size:23px}h2{font-size:18px}button,input,select,textarea{font:inherit;padding:8px;max-width:100%}label{display:block;margin:16px 0}textarea{width:96%;min-height:100px}*:focus-visible,h1:focus{outline:3px solid #145ba8;outline-offset:3px}.actions{display:flex;gap:12px;flex-wrap:wrap}</style><body></body></html>')}`);
  production.webContents.on('before-input-event', (event, input) => { if (input.type === 'keyDown' && input.key === 'F8') { event.preventDefault(); void showReview(); } });
  for (const window of [production, review]) window.on('close', event => {
    if (termination.finished) return; event.preventDefault(); if (stopping) return; stopping = true;
    const deadline = setTimeout(() => termination.finish(130), 3000);
    void review.webContents.executeJavaScript("Object.fromEntries(new FormData(document.querySelector('form')))").then(values => { drafts.set(state.task.id, values); save('interrupted.json', { reason: 'window-close' }); }).catch(() => save('interrupted.json', { reason: 'window-close-form-unavailable' })).finally(() => { clearTimeout(deadline); termination.finish(130); });
  });
  await renderStep(); await showReview();
  while (!termination.finished) {
    const action = await readAction(); drafts.set(state.task.id, action.values); save('in-progress.json');
    if (action.kind === 'stop') { save('interrupted.json', { reason: 'operator-stop' }); termination.finish(130); return; }
    if (action.kind === 'viewer') { review.minimize(); production.show(); production.focus(); continue; }
    if (action.kind === 'back') { state.move(state.index - 1); await renderStep(); continue; }
    if (action.kind === 'next') {
      state.answer(action.values.status ?? 'unknown', action.values.notes ?? ''); await capture(`step-${state.index + 1}`); save('in-progress.json');
      if (state.index === REVIEW_TASKS.length - 1) { await finishReview(); return; }
      state.move(state.index + 1); await renderStep();
    }
  }
}
void run().catch(error => { save('failure.json', { error: error instanceof Error ? error.message : 'Unknown review helper failure', consoleErrors: errors }); console.error(error); termination.finish(1); });
