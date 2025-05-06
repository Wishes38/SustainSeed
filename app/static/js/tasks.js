// static/js/tasks.js
document.addEventListener("DOMContentLoaded", () => {
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

  const btn       = document.getElementById("take-mission-btn");
  const subtitleEl = document.getElementById("hp-subtitle");

  btn.addEventListener("click", async () => {
    subtitleEl.textContent = "Görev alınıyor...";
    try {
      const res = await fetch("/eco-actions/", {
        method: "POST",
        headers,
        credentials: "same-origin"
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }
      const action = await res.json();
      const { title, description, xp_earned } = action;
      subtitleEl.textContent = `Yeni Eco-Action: ${title} — ${description} (+${xp_earned} XP)`;
    } catch (err) {
      console.error("Eco-action error:", err);
      subtitleEl.textContent = "Görev alınamadı.";
    }
  });
});
