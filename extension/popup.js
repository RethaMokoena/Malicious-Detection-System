document.getElementById("checkBtn").addEventListener("click", async () => {
  const input = document.getElementById("userInput").value.trim();
  if (!input) return alert("Please enter a URL.");

  const response = await fetch("http://127.0.0.1:5000/predict_url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: input })
  });

  const data = await response.json();
  
  if (data.error) {
    document.getElementById("result").innerText = `❌ Error: ${data.error}`;
    return;
  }

  const emoji = data.result === "malicious" ? "⚠️" : "✅";
  const color = data.result === "malicious" ? "red" : "green";
  
  document.getElementById("result").innerHTML = `
    <strong style="color:${color}">${emoji} ${data.result.toUpperCase()}</strong>
    <br>Confidence: ${(data.confidence * 100).toFixed(1)}%
  `;
});
