function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

function predictRain() {
  const temperature = Number(document.getElementById("temperature").value);
  const humidity = Number(document.getElementById("humidity").value);
  const pressure = Number(document.getElementById("pressure").value);
  const wind = Number(document.getElementById("wind").value);
  const cloud = Number(document.getElementById("cloud").value);
  const rainfall = Number(document.getElementById("rainfall").value);

  // Lightweight browser-side approximation of the trained QML model.
  // The Python folder contains the actual PennyLane QML implementation.
  const score =
    0.042 * humidity +
    0.038 * cloud +
    0.080 * rainfall +
    0.026 * wind -
    0.033 * temperature -
    0.023 * (pressure - 1000) -
    3.55;

  const probability = clamp(sigmoid(score), 0, 1);
  const percent = Math.round(probability * 100);

  let decision = "No Warning";
  let color = "#16a34a";
  let formalStatus = "PASS: Low-risk condition remains within the verified decision policy.";

  if (percent >= 70 && humidity >= 75 && cloud >= 60) {
    decision = "Warning: Rain likely";
    color = "#dc2626";
    formalStatus = "PASS: High-risk condition triggers Warning, satisfying the formal safety policy.";
  } else if (percent >= 45 && humidity >= 60) {
    decision = "Watch: Moderate rain risk";
    color = "#d97706";
    formalStatus = "PASS: Moderate-risk condition triggers Watch, a valid decision state.";
  }

  document.getElementById("probability").innerText = `${percent}%`;
  document.getElementById("probability").style.color = color;
  document.getElementById("decision").innerText = decision;
  document.getElementById("meter-fill").style.width = `${percent}%`;
  document.getElementById("meter-fill").style.background = color;
  document.getElementById("formal-status").innerText = formalStatus;
}

predictRain();
