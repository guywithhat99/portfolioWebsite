// Field numbers are the contract with the firmware. Changing one here means
// changing it in net.cpp too.
// digits is tooltip precision only. The firmware posts 3 decimals for every
// field, which is noise on a particle count and not enough on a rail voltage.
export const METRICS = [
  { field: 1, key: 'temp_f',   label: 'Temperature',   unit: 'degF', digits: 1 },
  { field: 2, key: 'humidity', label: 'Humidity',      unit: '%RH',  digits: 1 },
  { field: 3, key: 'altitude', label: 'Altitude',      unit: 'ft',   digits: 0 },
  { field: 4, key: 'v_rail',   label: 'Rail Voltage',  unit: 'V',    digits: 2 },
  { field: 5, key: 'pm_count', label: 'Particles 0.3–2.5 µm', unit: 'count / 0.1 L', digits: 0 },
  { field: 6, key: 'co2',      label: 'CO2',           unit: 'ppm',  digits: 0 },
  { field: 7, key: 'gas',      label: 'Gas Resistance', unit: 'ohm', digits: 0 }
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

// Locale is pinned rather than left to the browser so a screenshot of the
// dashboard reads the same on any machine, including in the report.
export function formatValue(metric, v) {
  if (v === null || v === undefined || !Number.isFinite(v)) return null;
  return v.toLocaleString('en-US', {
    minimumFractionDigits: metric.digits,
    maximumFractionDigits: metric.digits
  });
}

export function formatTime(t) {
  return new Date(t).toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: false
  });
}
