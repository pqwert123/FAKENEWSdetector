// script.js – Pratima Sahu (Fake News Detector logic)

document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('detectBtn');
  const textInput = document.getElementById('news');
  const resultDiv = document.getElementById('result');
  const loader = document.getElementById('loader');

  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const text = textInput.value.trim();
    if (!text) {
      alert("Please enter news text first!");
      return;
    }

    resultDiv.innerHTML = "";
    loader.style.display = 'block';

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      });

      const data = await res.json();
      loader.style.display = 'none';

      if (data.error) {
        resultDiv.innerHTML = `<div class="result fake">⚠️ Error: ${data.error}</div>`;
        return;
      }

      const label = data.label.toUpperCase();
      const conf = data.confidence ? ` (${Math.round(data.confidence * 100)}%)` : "";

      if (label === "FAKE") {
        resultDiv.innerHTML = `<div class="result fake">🚨 FAKE NEWS DETECTED${conf}</div>`;
      } else {
        resultDiv.innerHTML = `<div class="result real">✅ This News Seems REAL${conf}</div>`;
      }
    } catch (err) {
      loader.style.display = 'none';
      resultDiv.innerHTML = `<div class="result fake">❌ Backend Error: ${err.message}</div>`;
    }
  });
});
