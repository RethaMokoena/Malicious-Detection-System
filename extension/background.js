chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    checkURL(tab.url);
  }
});

function checkURL(currentUrl) {
  fetch("http://127.0.0.1:5000/predict_url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // You’ll eventually extract features from the URL before sending
    body: JSON.stringify({ url: currentUrl })
  })
  .then(response => response.json())
  .then(data => {
    console.log("URL check result:", data);
    if (data.result === "malicious") {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "warning.png",
        title: "⚠️ Malicious Website Detected",
        message: "The site you're visiting may be unsafe."
      });
    }
  })
  .catch(err => console.error("Error checking URL:", err));
}
