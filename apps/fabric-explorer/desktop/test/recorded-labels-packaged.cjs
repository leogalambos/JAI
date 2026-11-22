// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Run the pinned Electron with this driver, an extracted package app directory and a fresh output directory. */
const assert = require('node:assert/strict');
const { readFileSync, writeFileSync, mkdirSync, unlinkSync } = require('node:fs');
const { join, resolve } = require('node:path');
const { app, BrowserWindow, dialog } = require('electron');

const [packagedApp, output] = process.argv.slice(-2);
if (!packagedApp || !output) throw Error('Supply extracted application and fresh evidence directories.');
const fixture = JSON.parse(readFileSync(join(__dirname, '../../packages/contracts/test/fixtures/recorded-labels.json')));
const sample = name => {
  const row = fixture.cases.find(item => item.case === name);
  assert(row, name);
  return row;
};
const legacy = sample('legacy-companion');
const missing = sample('missing');
const literal = sample('literal-markup');
const first = sample('superseded-answer');
const replacement = sample('supported-replacement');
const review = sample('supporting-review');
const conflict = sample('conflict-finding');
const project = resolve(output, 'synthetic-project');
const sourceDir = join(project, '.fabric');
const journal = join(sourceDir, 'qualification.jsonl');
const blobs = journal + '.blobs';
mkdirSync(blobs, { recursive: true });
const data = resolve(output, 'app-data');
mkdirSync(data);
app.setPath('appData', data);

const attachments = row => Object.entries(row.materialDesignations).map(([pointer, designation]) => {
  const blobId = row.manifest.content.record.material[Number(pointer.split('/').at(-1))];
  const material = fixture.companions[blobId];
  return { blob_id: blobId, byte_length: material.byteLength, media_type: designation.media,
    classification: 'internal', access_handle: 'synthetic-companion' };
});
const cases = [first, replacement, legacy, missing, literal, review, conflict];
const journalBytes = Buffer.from(cases.map((row, index) => JSON.stringify({
  format: 9, protocol: 'jai.governed-delivery/1', sequence: index + 1, hash: 'a'.repeat(64),
  operations: [{ op: 'governed', data: { message: { scope: 'default', attachments: attachments(row) },
    effects: [{ op: 'register', manifest: row.manifest,
      origin: { kind: 'controller', id: 'synthetic' }, context: null, dependencies: [] },
      ...([first, replacement].includes(row)
        ? [{ op: 'qualify', subject: row.versionId, applicable: row === replacement }]
        : [])] } }],
})).join('\n') + '\n');
writeFileSync(journal, journalBytes);
const legacyDigest = legacy.expected.source.blobId;
const legacyPath = join(blobs, legacyDigest);
const legacyBytes = Buffer.from(fixture.companions[legacyDigest].contentBase64, 'base64');
for (const row of cases) {
  for (const { blob_id: digest } of attachments(row)) {
    const companion = fixture.companions[digest];
    if (companion.availability === 'available') writeFileSync(join(blobs, digest), Buffer.from(companion.contentBase64, 'base64'));
  }
}

// Replace only native dialog interaction. The package supplies the real main, picker,
// preload, renderer, import worker and hardened window configuration.
dialog.showOpenDialog = async (_window, options) => {
  assert.deepEqual(options.properties, ['openDirectory']);
  return { canceled: false, filePaths: [project] };
};
require(resolve(packagedApp, 'main.cjs'));

let window;
const observations = [];
const evaluate = body => window.webContents.executeJavaScript(`(async () => { ${body} })()`);
const quoted = JSON.stringify;
const wait = async (expression, description) => {
  const matched = await evaluate(`const end = performance.now() + 12000;
    do { if (${expression}) return true; await new Promise(resolve => setTimeout(resolve, 25)); } while (performance.now() < end);
    return false;`);
  if (!matched) {
    const status = await evaluate("return ['#snapshot-state', '#status', '.error'].map(selector => document.querySelector(selector)?.textContent).filter(Boolean).join(' | ');");
    const table = await evaluate("return [document.querySelector('#element-kind')?.value, ...Array.from(document.querySelectorAll('.semantic-panel tbody button'), node => node.textContent)];");
    assert.fail(description + " (" + status + "; table: " + table.join(', ') + ")");
  }
};
const click = selector => evaluate(`const button = document.querySelector(${quoted(selector)});
  if (!button || button.disabled) throw Error('Control unavailable: ' + ${quoted(selector)}); button.click();`);
const set = (selector, value) => evaluate(`const input = document.querySelector(${quoted(selector)});
  Object.getOwnPropertyDescriptor(input.tagName === 'SELECT' ? HTMLSelectElement.prototype : HTMLInputElement.prototype, 'value').set.call(input, ${quoted(value)});
  input.dispatchEvent(new Event(input.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true }));`);
const search = async (query, labels) => {
  await click('#tab-search');
  await set('#search-text', query);
  await evaluate("document.querySelector('#search-text').form.requestSubmit();");
  await wait(`!document.querySelector('#status').textContent.includes('Working:') &&
    JSON.stringify(Array.from(document.querySelectorAll('#search-content .results button'), node => node.firstChild.textContent).sort())
    === ${quoted(JSON.stringify([...labels].sort()))}`, 'Search result labels for ' + query);
};
const selectVersion = async (row, label = row.expected.text) => {
  await search(row.versionId, [label, label]);
  await evaluate(`const button = Array.from(document.querySelectorAll('#search-content .results button')).find(node => node.querySelector('small').textContent === 'version');
    if (!button) throw Error('Version result unavailable'); button.click();`);
  await wait(`document.querySelector('[data-testid=selected-id]')?.textContent.includes(${quoted(row.versionId)}) &&
    document.querySelector('[data-testid=selected-label]')?.textContent === ${quoted(label)}`, 'Exact inspector label');
};
const openProvenance = async () => {
  await click('#inspector-tab-evidence');
  await evaluate("const details = document.querySelector('#inspector-evidence details'); if (!details.open) details.querySelector('summary').click();");
};
const showReviewRelation = async () => {
  await selectVersion(review);
  await evaluate('window.recordedPaint.clear();');
  await click('#expand');
  await wait("!document.querySelector('#status').textContent.includes('Working:')", 'Completed assessment neighbourhood');
  await click('#show-elements');
  await set('#element-kind', 'vertices');
  await wait(`Array.from(document.querySelectorAll('.semantic-panel tbody button')).some(node => node.textContent === ${quoted(review.expected.text)})`, 'Exact graph table label');
  await wait(`Array.from(window.recordedPaint).some(text => text === ${quoted(review.expected.text)}
    || (text.endsWith('…') && text.includes('supported · Restore') && ${quoted(review.expected.text)}.startsWith(text.slice(0, -1))))`, 'Actual graph canvas label');
  await set('#element-kind', 'edges');
  await wait("document.querySelector('.semantic-panel caption')?.textContent.startsWith('Visible relations')", 'Relation table committed');
  // The relation table is paged by exact key. Locate the subject edge even
  // when other associations occupy the first page.
  const edgeFound = await evaluate(`for (let page = 0; page < 10; page++) {
    const match = Array.from(document.querySelectorAll('.semantic-panel tbody button')).find(node =>
      node.textContent === '/subject' && node.title.includes(${quoted(review.versionId)}) &&
      node.title.includes(${quoted(replacement.versionId)}));
    if (match) { match.click(); return true; }
    const next = Array.from(document.querySelectorAll('.semantic-panel button')).find(button => button.textContent === 'Next elements');
    if (!next || next.getAttribute('aria-disabled') === 'true') return false;
    next.click();
    await new Promise(resolve => setTimeout(resolve, 25));
  } return false;`);
  assert(edgeFound, 'Exact recorded subject relation');
  await wait("document.querySelector('#inspector-heading')?.textContent === 'Relation inspector'", 'Selected exact relation');
  await click('#inspector-tab-relations');
  await wait(`!document.querySelector('#inspector-relations').hidden &&
    Array.from(document.querySelectorAll('#inspector-relations dd button')).every((node, index) =>
      node.title.includes([${quoted(replacement.versionId)}, ${quoted(review.versionId)}][index])) &&
    Array.from(document.querySelectorAll('#inspector-relations dd button')).map(node => node.textContent).join('|') ===
    ${quoted(replacement.expected.text + '|' + review.expected.text)}`, 'Canonical labels on both relationship endpoints');
};
const generation = n => wait(`document.querySelector('#snapshot-state')?.textContent === 'Snapshot ${n} · 1 sources'
  && !document.querySelector('#refresh').disabled`, 'Accepted generation ' + n);

async function run() {
  await app.whenReady();
  const deadline = Date.now() + 12000;
  while (!BrowserWindow.getAllWindows().length && Date.now() < deadline) await new Promise(resolve => setTimeout(resolve, 20));
  window = BrowserWindow.getAllWindows()[0];
  assert(window, 'Packaged window did not start');
  window.setSize(1440, 1050);
  await wait("document.querySelector('#open') && !document.querySelector('#open').disabled", 'Packaged renderer ready');
  // Observe production canvas text without changing what the renderer paints.
  await evaluate(`window.recordedPaint = new Set();
    const paint = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function (text, ...args) {
      if (window.recordedPaint.size < 1000) window.recordedPaint.add(text);
      return paint.call(this, text, ...args);
    };`);
  await click('#families input[value=findings]');
  await click('#open');
  await generation(1);
  await search('Restore shared catalogue records', [first.expected.text, first.expected.text, replacement.expected.text, replacement.expected.text, review.expected.text, review.expected.text]);
  for (const row of [first, replacement, conflict]) await selectVersion(row);
  for (const [row, applicable] of [[first, false], [replacement, true]]) {
    await search(row.versionId, [row.expected.text, row.expected.text]);
    await evaluate("Array.from(document.querySelectorAll('#search-content .results button')).find(node => node.querySelector('small').textContent === 'use').click();");
    await wait(`document.querySelector('[data-testid=selected-id]')?.textContent.includes(${quoted(row.versionId)}) &&
      document.querySelector('#inspector-overview').textContent.includes('Use scopedefault') &&
      JSON.parse(document.querySelector('[data-testid=attributes]').textContent).value.entries.some(entry => entry.key === 'applicable' &&
        entry.value.value === ${applicable})`, 'Exact use scope and applicability');
  }
  await selectVersion(literal);
  assert(await evaluate("return !document.querySelector('[data-testid=selected-label] em');"), 'Literal markup must stay text');
  await selectVersion(missing);
  await openProvenance();
  assert(await evaluate("return document.querySelector('#inspector-evidence').textContent.includes('Unavailable reasonmissing');"));
  await selectVersion(legacy);
  await openProvenance();
  const provenance = await evaluate("return Array.from(document.querySelectorAll('#inspector-evidence details dd'), node => node.textContent);");
  assert.deepEqual(provenance, [legacy.versionId, legacy.expected.source.pointer, legacyDigest]);
  observations.push('Exact versions, duplicate labels, literal markup, missing reason and companion provenance');

  await showReviewRelation();
  observations.push('Canvas paint, element table and exact relationship endpoints');

  unlinkSync(legacyPath);
  await click('#refresh');
  await generation(2);
  await selectVersion(legacy, missing.expected.text);
  await openProvenance();
  assert(await evaluate("return document.querySelector('#inspector-evidence').textContent.includes('Unavailable reasonmissing');"));
  writeFileSync(legacyPath, legacyBytes);
  await click('#refresh');
  await generation(3);
  await selectVersion(legacy);
  await showReviewRelation();
  assert.deepEqual(readFileSync(journal), journalBytes);
  observations.push('Companion-only refresh in both directions with identical journal bytes');
  await click('#close');
  await wait("document.querySelector('#snapshot-state').textContent === 'No snapshot imported.'", 'Packaged sources closed');
}

const watchdog = setTimeout(() => { console.error('Packaged recorded-label journey timed out.'); app.exit(1); }, 100000);
run().then(() => {
  clearTimeout(watchdog);
  writeFileSync(join(output, 'recorded-labels-native.json'), JSON.stringify({ status: 'pass', electron: process.versions.electron, observations }, null, 2) + '\n');
  console.log('Packaged recorded-label journey passed.');
  app.quit();
}, error => {
  clearTimeout(watchdog);
  console.error(error);
  app.exit(1);
});
