// static/js/chat.js
document.addEventListener("DOMContentLoaded", () => {
  // Helper: cookie’den token al
  const getCookie = name => {
    const v = "; " + document.cookie;
    const parts = v.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(";").shift() : null;
  };
  const token = getCookie("access_token");
  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };

  // Elementleri seç
  const form       = document.getElementById("chat-form");
  const input      = document.getElementById("chat-input");
  const subtitleEl = document.getElementById("hp-subtitle");

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const prompt = input.value.trim();
    if (!prompt) return;

    input.value = "";
    subtitleEl.textContent = "Loading...";

    try {
      const res = await fetch("/chatbot/", {
        method: "POST",
        headers,
        credentials: "same-origin",
        body: JSON.stringify({ message: prompt })
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }
      const data = await res.json();

      if (data.mode === "chat") {
        subtitleEl.textContent = data.message;
      } else if (data.mode === "task") {
        const { title, description, xp_earned } = data.task;
        subtitleEl.textContent = `Görev: ${title} — ${description} (+${xp_earned} XP)`;
      }
    } catch (err) {
      console.error("Chat error:", err);
      subtitleEl.textContent = "Üzgünüm, bir hata oluştu.";
    }
  });
});
