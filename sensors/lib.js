// Field numbers are the contract with the firmware. Changing one here means
// changing it in net.cpp too.
export const METRICS = [
  { field: 1, key: 'temp_f',   label: 'Temperature',   unit: 'degF' },
  { field: 2, key: 'humidity', label: 'Humidity',      unit: '%RH' },
  { field: 3, key: 'altitude', label: 'Altitude',      unit: 'ft' },
  { field: 4, key: 'v_rail',   label: 'Rail Voltage',  unit: 'V' },
  { field: 5, key: 'pm_count', label: 'Particles 0.3–2.5 µm', unit: 'count / 0.1 L' },
  { field: 6, key: 'co2',      label: 'CO2',           unit: 'ppm' },
  { field: 7, key: 'gas',      label: 'Gas Resistance', unit: 'ohm' }
];

// ThingSpeak hands back every field as a string, and a skipped field as null.
// Number(null) is 0, which would silently plot a real-looking zero, so null
// has to be checked before conversion.
function num(raw) {
  if (raw === null || raw === undefined || raw === '') return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : null;
}

export function parseFeed(json) {
  const feeds = (json && json.feeds) || [];
  const points = feeds.map(row => {
    const values = {};
    for (const m of METRICS) values[m.key] = num(row['field' + m.field]);
    return { t: new Date(row.created_at), values };
  });
  return { points, channel: (json && json.channel) || {} };
}

export function isStale(newest, now, maxAgeMs) {
  if (!newest) return true;
  return (now.getTime() - newest.getTime()) > maxAgeMs;
}

export function seriesFor(points, key) {
  return points.map(p => ({ x: p.t, y: p.values[key] }));
}
