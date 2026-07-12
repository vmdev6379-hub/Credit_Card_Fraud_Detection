let META = null;

async function loadMeta() {
  const res = await fetch("/api/meta");
  META = await res.json();

  buildVGrid();
  buildSampleOptions();
  buildTape();
  buildDistribution();
}

function buildVGrid() {
  const grid = document.getElementById("vGrid");
  const vFeatures = META.features.filter(f => f.startsWith("V"));
  grid.innerHTML = vFeatures.map(f => `
    <div class="field">
      <label for="f_${f}">${f}</label>
      <input type="number" step="0.0001" id="f_${f}" value="0">
    </div>
  `).join("");
}

function buildSampleOptions() {
  const select = document.getElementById("sampleSelect");
  META.samples.forEach((s, i) => {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = `${s.label === "fraud" ? "Fraud" : "Normal"} sample #${i + 1} — $${s.features.Amount.toFixed(2)}`;
    select.appendChild(opt);
  });
  select.addEventListener("change", () => {
    if (select.value === "") return;
    const sample = META.samples[parseInt(select.value, 10)];
    applySample(sample.features);
  });
}

function applySample(features) {
  document.getElementById("amount").value = features.Amount;
  document.getElementById("time").value = features.Time;
  Object.keys(features).forEach(f => {
    if (f.startsWith("V")) {
      const el = document.getElementById(`f_${f}`);
      if (el) el.value = features[f];
    }
  });
}

function buildTape() {
  const track = document.getElementById("tapeTrack");
  const items = META.samples.concat(META.samples); // loop content for seamless scroll
  track.innerHTML = items.map(s => `
    <span class="tape__item">
      <span class="amt">$${s.features.Amount.toFixed(2)}</span>
      <span>t+${Math.round(s.features.Time)}s</span>
      <span class="flag flag--${s.label}">${s.label === "fraud" ? "FLAGGED" : "CLEARED"}</span>
    </span>
  `).join("");
}

function buildDistribution() {
  const { normal, fraud } = META.class_counts;
  const total = normal + fraud;
  document.getElementById("distNormal").style.width = `${(normal / total) * 100}%`;
  document.getElementById("distFraud").style.width = `${(fraud / total) * 100}%`;
  document.getElementById("distNormalCount").textContent = normal.toLocaleString();
  document.getElementById("distFraudCount").textContent = fraud.toLocaleString();
}

function collectFeatures() {
  const features = {
    Amount: parseFloat(document.getElementById("amount").value),
    Time: parseFloat(document.getElementById("time").value),
  };
  META.features.filter(f => f.startsWith("V")).forEach(f => {
    const el = document.getElementById(`f_${f}`);
    features[f] = el ? parseFloat(el.value) || 0 : 0;
  });
  return features;
}

async function screenTransaction(e) {
  e.preventDefault();
  const features = collectFeatures();

  const verdict = document.getElementById("verdict");
  const resultEl = document.getElementById("verdictResult");
  const probEl = document.getElementById("verdictProb");
  const gaugeFill = document.getElementById("gaugeFill");

  resultEl.textContent = "Scanning…";
  verdict.dataset.state = "idle";

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ features }),
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    const pct = (data.fraud_probability * 100).toFixed(1);
    verdict.dataset.state = data.label;
    resultEl.textContent = data.label === "fraud" ? "Likely fraud" : "Looks normal";
    probEl.textContent = `fraud probability: ${pct}%`;
    gaugeFill.style.width = `${pct}%`;
    gaugeFill.style.background = data.label === "fraud" ? "var(--fraud)" : "var(--normal)";
  } catch (err) {
    resultEl.textContent = "Error";
    probEl.textContent = err.message;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadMeta();
  document.getElementById("scanForm").addEventListener("submit", screenTransaction);
});
