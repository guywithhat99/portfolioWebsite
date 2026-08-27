import { METRICS, parseFeed, isStale, seriesFor } from './lib.js';

const CHANNEL_ID = '3472589';
const RESULTS = 144;             // 144 points at 10 min = 24 hours
const STALE_MS = 25 * 60 * 1000; // one missed window plus slack
const FEED_URL =
  `https://api.thingspeak.com/channels/${CHANNEL_ID}/feeds.json?results=${RESULTS}`;

const statusEl = document.getElementById('status');
const chartsEl = document.getElementById('charts');
const charts = [];

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = 'status' + (cls ? ' ' + cls : '');
}

function humanAge(ms) {
  const min = Math.round(ms / 60000);
  if (min < 60) return `${min} min`;
  const hr = Math.floor(min / 60);
  return `${hr} hr ${min % 60} min`;
}

// With pointRadius 0 a reading whose neighbours are both null has no line
// segment to sit on and draws nothing at all. Give those a visible dot, so a
// sparse or intermittent sensor reads as sparse rather than as broken.
function isolatedPointRadius(ctx) {
  const d = ctx.dataset.data;
  const i = ctx.dataIndex;
  const at = k => (k >= 0 && k < d.length && d[k] ? d[k].y : null);
  if (at(i) === null) return 0;
  return (at(i - 1) === null && at(i + 1) === null) ? 3 : 0;
}

function renderChart(metric, points) {
  const card = document.createElement('section');
  card.className = 'chart-card';
  card.innerHTML =
    `<h2>${metric.label} (${metric.unit})</h2><div class="chart-wrap"><canvas></canvas></div>`;
  chartsEl.appendChild(card);

  charts.push(new Chart(card.querySelector('canvas'), {
    type: 'line',
    data: {
      datasets: [{
        label: `${metric.label} (${metric.unit})`,
        data: seriesFor(points, metric.key),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37,99,235,0.08)',
        borderWidth: 2,
        pointRadius: isolatedPointRadius,
        tension: 0.2,
        spanGaps: false   // a dropped window must read as a gap, not a straight line
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { type: 'time',
             time: { unit: 'hour', displayFormats: { hour: 'HH:mm' } },
             title: { display: true, text: 'Time' } },
        y: { title: { display: true, text: metric.unit } }
      }
    }
  }));
}

async function load() {
  let json;
  try {
    const res = await fetch(FEED_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    json = await res.json();
  } catch (err) {
    setStatus(`Could not reach ThingSpeak: ${err.message}`, 'error');
    return;
  }

  const { points } = parseFeed(json);
  if (points.length === 0) {
    setStatus('Channel is live but has no data yet.', 'error');
    return;
  }

  const newest = points[points.length - 1].t;
  const now = new Date();
  if (isStale(newest, now, STALE_MS)) {
    setStatus(
      `Node may be offline. Last reading was ${humanAge(now - newest)} ago ` +
      `(${newest.toLocaleString()}). Showing the most recent data available.`,
      'stale');
  } else {
    setStatus(
      `Live. ${points.length} ${points.length === 1 ? 'point' : 'points'} ` +
      `over the last 24 hours. ` +
      `Last reading ${humanAge(now - newest)} ago.`, '');
  }

  // Refresh in place on the interval rather than stacking duplicate canvases.
  if (charts.length) {
    METRICS.forEach((m, i) => {
      charts[i].data.datasets[0].data = seriesFor(points, m.key);
      charts[i].update('none');
    });
  } else {
    for (const m of METRICS) renderChart(m, points);
  }
}

const link = document.getElementById('channel-link');
link.href = `https://thingspeak.com/channels/${CHANNEL_ID}`;
link.textContent = CHANNEL_ID;

load();
setInterval(load, 5 * 60 * 1000);
