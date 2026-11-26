import assert from 'node:assert/strict'
import test from 'node:test'
import { evidence, parseReport, profile, validate } from '../operator.js'
import { schedule } from '../schedule.js'

const source = '#EVOLVE_START\nx = propose()\nif valid(x):\n    x = repair(x)\n#EVOLVE_END\nprint(x)'
const report = { hypothesis: { claim: 'Missing global move', evidence: ['repair called twice'], confidence: 0.8, test: 'paired score' },
  operator: { name: 'global repair', change: 'repair all', scope: 'state', components: ['a'] } }

test('M1 extracts inline writes, calls and conditions', () => {
  const [region] = profile(source).regions
  assert.deepEqual(region.writes, ['x'])
  assert.deepEqual(region.calls, ['propose', 'valid', 'repair'])
  assert.equal(region.branches.length, 1)
})

test('M2/M3 use arbitrary hypotheses, lineage and confidence; enforce composition metadata', () => {
  const rows = [{ id: 'base', fitness: 2 }, { id: 'a', parent: 'base', fitness: 1 }]
  const trace = evidence(rows, Number, 1)
  assert.equal(trace.stagnant, 1)
  assert.equal(trace.trajectory[0].parentDelta, -1)
  assert.deepEqual(parseReport(JSON.stringify(report), 0.6, ['a']).operator, report.operator)
  assert.equal(parseReport(JSON.stringify(report), 0.9), null)
  assert.equal(parseReport(JSON.stringify(report), 0.6, ['b']), null)
})

test('M4 rejects out-of-scope edits before evaluation and gates multi-seed promotion', async () => {
  const options = {
    parent: { fitness: 1, id: 'base' }, candidate: { id: 'a' }, before: source,
    merit: Number, signal: new AbortController().signal, seeds: [1, 2, 3],
    trial: (item, seed) => item.id === 'a' ? seed + 1 : seed,
  }
  assert.equal((await validate({ ...options, after: source + 'changed' })).stage, 'scope')
  const after = source.replace('propose()', 'build()')
  assert.equal((await validate({ ...options, after, evaluate: () => 2, spend: () => false })).stage, 'trial-budget')
  const result = await validate({ ...options, after, evaluate: () => 2, spend: () => true })
  assert.equal(result.accepted, true)
  assert.equal(result.mean, 1)
  assert.equal(result.pairs.length, 3)
})

test('M5 explores reuse and composition after distinct accepted discoveries', () => {
  const make = (id, kind) => ({
    id, phase: 'plateau', plan: { kind }, report: { operator: { name: id } }, result: { accepted: true, gain: 1 },
  })
  const items = [make('a', 'discover'), make('b', 'discover')]
  assert.equal(schedule(items, 'plateau').kind, 'reuse')
  const reuse = { ...make('r', 'reuse'), result: { accepted: false } }
  const plan = schedule([...items, reuse], 'plateau')
  assert.equal(plan.kind, 'compose')
  assert.deepEqual(plan.components.map(item => item.id), ['a', 'b'])
})

