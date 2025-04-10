async function start() {
  const sources = (await fetch("/sources").then((r) => r.json())).map((r) => [
    r.name,
    r.topic,
  ]);
  const chartsElt = document.getElementById("charts");

  const width = 500;
  const height = 250;
  const padding = 30;
  const maxPoints = 100;
  const charts = {};

  function createCanvasChart(name, topic) {
    const container = document.createElement("div");
    container.className = "chart-container";

    const title = document.createElement("div");
    title.className = "chart-title";
    title.textContent = `Chart for ${name}`;
    container.appendChild(title);

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    container.appendChild(canvas);

    chartsElt.appendChild(container);

    charts[topic] = {
      canvas,
      ctx: canvas.getContext("2d"),
      data: [],
    };
  }

  function drawCanvasChart(sourceId) {
    const { canvas, ctx, data } = charts[sourceId];
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const plotWidth = width - padding * 2;
    const plotHeight = height - padding * 2;

    if (data.length < 2) return;

    const values = data.map((d) => d.value).filter((v) => v !== undefined);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    // Axes and grid
    ctx.strokeStyle = "#ddd";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const yTicks = 5;
    for (let i = 0; i <= yTicks; i++) {
      const y = padding + (plotHeight / yTicks) * i;
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);

      // Y labels
      ctx.fillStyle = "#444";
      ctx.font = "10px sans-serif";
      const val = max - (range / yTicks) * i;
      ctx.fillText(val.toFixed(1), 5, y + 3);
    }
    ctx.stroke();

    // Data line
    ctx.beginPath();
    ctx.strokeStyle = "steelblue";
    ctx.lineWidth = 2;

    let stopDrawing = true;
    data.forEach((d, i) => {
      if (d.value === undefined) {
        stopDrawing = true;
        return;
      }

      const x = padding + (i / (maxPoints - 1)) * plotWidth;
      const y = padding + plotHeight - ((d.value - min) / range) * plotHeight;
      if (stopDrawing) {
        ctx.moveTo(x, y);
        stopDrawing = false;
      } else {
        ctx.lineTo(x, y);
      }
    });
    ctx.stroke();
  }

  function subscribeToSource([name, topic]) {
    createCanvasChart(name, topic);

    const eventSource = new EventSource(`/events/${topic}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const chart = charts[topic];

      if (chart) {
        chart.data.push(data);
        if (chart.data.length > maxPoints) {
          chart.data.shift();
        }

        drawCanvasChart(topic);

        clearTimeout(chart.timer);
        chart.timer = setTimeout(waitForNextPoint(topic), 1500);
      }
    };
  }

  const waitForNextPoint = (topic) => () => {
    let chart = charts[topic];
    let tsSeconds = Date.now() / 1000;
    if (
      chart.data.length > 0 &&
      tsSeconds - chart.data.at(-1).timestamp >= 1.5
    ) {
      chart.data.push({ value: undefined, timestamp: tsSeconds });
      if (chart.data.length > maxPoints) {
        chart.data.shift();
      }

      drawCanvasChart(topic);

      clearTimeout(chart.timer);
      chart.timer = setTimeout(waitForNextPoint(topic), 1500);
    }
  };

  sources.forEach(subscribeToSource);
}

start();
