import { test } from 'node:test';
import assert from 'node:assert/strict';
import { METRICS, parseFeed, isStale, seriesFor, formatValue, formatTime } from '../sensors/lib.js';

const sample = {
  channel: { id: 123, name: 'test' },
  feeds: [
    { created_at: '2026-08-27T10:00:00Z', entry_id: 1,
      field1: '72.5', field2: '41.2', field3: '5280', field4: '5.02',
      field5: '120', field6: '680', field7: '98000' },
    { created_at: '2026-08-27T10:10:00Z', entry_id: 2,
      field1: '73.0', field2: null, field3: '5281', field4: '5.01',
      field5: '118', field6: '690', field7: '97000' }
  ]
};

test('METRICS covers all seven contract fields in order', () => {
  assert.equal(METRICS.length, 7);
  assert.deepEqual(METRICS.map(m => m.field), [1, 2, 3, 4, 5, 6, 7]);
  assert.equal(METRICS[0].key, 'temp_f');
  assert.equal(METRICS[0].unit, 'degF');
});

test('parseFeed converts ThingSpeak strings to numbers', () => {
  const { points } = parseFeed(sample);
  assert.equal(points.length, 2);
  assert.equal(points[0].values.temp_f, 72.5);
  assert.equal(typeof points[0].values.temp_f, 'number');
});

test('parseFeed maps a null field to null, not NaN or zero', () => {
  const { points } = parseFeed(sample);
  assert.equal(points[1].values.humidity, null);
});

test('parseFeed produces Date objects in chronological order', () => {
  const { points } = parseFeed(sample);
  assert.ok(points[0].t instanceof Date);
  assert.ok(points[0].t < points[1].t);
});

test('parseFeed tolerates an empty feed', () => {
  const { points } = parseFeed({ channel: {}, feeds: [] });
  assert.deepEqual(points, []);
});

test('isStale is false for a fresh point and true past the threshold', () => {
  const now = new Date('2026-08-27T10:20:00Z');
  assert.equal(isStale(new Date('2026-08-27T10:12:00Z'), now, 25 * 60000), false);
  assert.equal(isStale(new Date('2026-08-27T09:40:00Z'), now, 25 * 60000), true);
});

test('isStale treats a missing newest point as stale', () => {
  assert.equal(isStale(null, new Date(), 25 * 60000), true);
});

test('seriesFor extracts x/y pairs for one metric', () => {
  const { points } = parseFeed(sample);
  const s = seriesFor(points, 'co2');
  assert.deepEqual(s.map(p => p.y), [680, 690]);
});

test('formatValue uses per-metric precision', () => {
  const byKey = k => METRICS.find(m => m.key === k);
  assert.equal(formatValue(byKey('temp_f'), 83.027), '83.0');
  assert.equal(formatValue(byKey('v_rail'), 5.0182), '5.02');
  assert.equal(formatValue(byKey('pm_count'), 578), '578');
  assert.equal(formatValue(byKey('gas'), 33853), '33,853');
});

test('formatValue rejects nulls rather than printing them', () => {
  const m = METRICS[0];
  assert.equal(formatValue(m, null), null);
  assert.equal(formatValue(m, undefined), null);
  assert.equal(formatValue(m, NaN), null);
});

test('formatTime renders a readable 24h stamp', () => {
  assert.equal(formatTime('2026-08-27T14:20:00Z'), formatTime(new Date('2026-08-27T14:20:00Z')));
  assert.match(formatTime('2026-08-27T14:20:00Z'), /Aug 27, \d{2}:\d{2}/);
});
