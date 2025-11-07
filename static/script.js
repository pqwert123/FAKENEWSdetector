// script.js – Pratima Sahu (Fake News Detector logic)

document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('detectBtn');
  const textInput = document.getElementById('news');
  const resultDiv = document.getElementById('result');
  const loader = document.getElementById('loader');

  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const text = textInput.value.trim();

    // 🧩 1. Input validation
    if (!text) {
      alert("⚠️ Please enter news text first!");
      return;
    }
    if (text.length > 20000) {
      alert("⚠️ Text too long! Please paste shorter content.");
      return;
    }

    // 🌀 2. Reset UI
    resultDiv.innerHTML = "";
    loader.style.display = 'block';

    try {
      // 🌐 3. Use absolute URL (works on localhost + Render)
      const apiURL = window.location.origin + "/predict";

      const res = await fetch(apiURL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
      });

      // 🧠 4. Handle non-JSON responses safely
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server error ${res.status}: ${errorText}`);
      }

      const data = await res.json();
      loader.style.display = 'none';

      // ⚠️ 5. Handle Flask-side error messages
      if (data.error) {
        resultDiv.innerHTML = `<div class="result fake">⚠️ Error: ${data.error}</div>`;
        return;
      }

      // ✅ 6. Show results
      const label = (data.label || "Unknown").toUpperCase();
      const conf = data.confidence ? ` (${Math.round(data.confidence * 100)}%)` : "";

      if (label === "FAKE") {
        resultDiv.innerHTML = `<div class="result fake">🚨 FAKE NEWS DETECTED${conf}</div>`;
      } else if (label === "REAL") {
        resultDiv.innerHTML = `<div class="result real">✅ This News Seems REAL${conf}</div>`;
      } else {
        resultDiv.innerHTML = `<div class="result" style="background:rgba(255,255,255,0.05); color:#fff;">❓ Unknown prediction</div>`;
      }

    } catch (err) {
      loader.style.display = 'none';
      resultDiv.innerHTML = `<div class="result fake">❌ Backend Error: ${err.message}</div>`;
      console.error("Error in detectFakeNews:", err);
    }
  });
});

