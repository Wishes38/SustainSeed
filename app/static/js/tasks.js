// static/js/tasks.js

/**
 * Helper: Cookie’den access_token oku
 */
function getCookie(name) {
  const v = "; " + document.cookie;
  const parts = v.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(";").shift() : null;
}

/**
 * Günlük & Eco görevleri yükleyip render eden ana fonksiyon.
 */
async function loadTasks() {
  const token = getCookie("access_token");
  if (!token) {
    console.warn("Token bulunamadı. Lütfen giriş yapın.");
    return;
  }
  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };

  // ——— A) Günlük görevleri atama ———
  try {
    await fetch("/daily-tasks/assign", {
      method: "POST",
      headers,
      credentials: "same-origin"
    });
  } catch (err) {
    console.warn("Daily assign hatası:", err);
  }

  // ——— B) Günlük görevleri çek & render et ———
  try {
    const res = await fetch("/daily-tasks/my-assignments", {
      method: "GET",
      headers,
      credentials: "same-origin"
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const daily = await res.json();
    const dailyContainer = document.getElementById("daily-tasks-body");
    dailyContainer.innerHTML = "";

    if (daily.length === 0) {
      dailyContainer.textContent = "Yeni görev bulunamadı.";
    } else {
      daily.forEach(asg => {
        const label = document.createElement("label");
        label.className = "task-item";

        // — toggle butonu
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "task-complete-circle";
        if (asg.completed) btn.classList.add("completed");
        btn.addEventListener("click", async () => {
          const url = asg.completed
            ? `/daily-tasks/uncomplete/${asg.id}`
            : `/daily-tasks/complete/${asg.id}`;
          const r2 = await fetch(url, {
            method: "POST",
            headers,
            credentials: "same-origin"
          });
          if (!r2.ok) return console.error("Toggle daily hata", await r2.text());
          const updated = await r2.json();
          asg.completed = updated.completed;
          btn.classList.toggle("completed", asg.completed);
          // XP bar güncelle (isteğe bağlı)
          if (updated.new_xp !== undefined && updated.percent !== undefined) {
            document.querySelector(".hp-xp-fill").style.width = `${updated.percent}%`;
            document.querySelector(".hp-xp-label").textContent = `${updated.new_xp.toFixed(1)} XP`;
          }
        });
        label.appendChild(btn);

        // — başlık & açıklama
        const info = document.createElement("div");
        const title = document.createElement("div");
        title.className = "task-title";
        title.textContent = asg.daily_task.title;
        const desc = document.createElement("div");
        desc.className = "task-desc";
        desc.textContent = asg.daily_task.description;
        info.append(title, desc);
        label.appendChild(info);

        // — XP etiketi
        const xp = document.createElement("div");
        xp.className = "task-xp";
        xp.textContent = `${asg.daily_task.xp_earned.toFixed(1)} XP`;
        label.appendChild(xp);

        dailyContainer.appendChild(label);
      });
    }
  } catch (err) {
    console.error("Daily yükleme hatası:", err);
  }

  // ——— C) Eco-action log’larını çek ———
  let logs = [];
  try {
    const lRes = await fetch("/user-task-logs", {
      method: "GET",
      headers,
      credentials: "same-origin"
    });
    if (lRes.ok) logs = await lRes.json();
  } catch (err) {
    console.error("Log fetch hatası:", err);
  }

  // ——— D) Ekolojik aksiyonları çek & render et ———
  try {
    const eRes = await fetch("/eco-actions", {
      method: "GET",
      headers,
      credentials: "same-origin"
    });
    if (!eRes.ok) throw new Error(`Status ${eRes.status}`);
    const eco = await eRes.json();
    const ecoContainer = document.getElementById("eco-tasks-body");
    ecoContainer.innerHTML = "";

    if (eco.length === 0) {
      ecoContainer.textContent = "Henüz eco–action yok.";
    } else {
      eco.forEach(action => {
        const label = document.createElement("label");
        label.className = "task-item";

        // — toggle butonu
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "task-complete-circle";
        let done = logs.some(log => log.eco_action_id === action.id && log.completed);
        if (done) btn.classList.add("completed");
        btn.addEventListener("click", async () => {
          const url = done
            ? `/eco-actions/${action.id}/uncomplete`
            : `/eco-actions/${action.id}/complete`;
          const r2 = await fetch(url, {
            method: "POST",
            headers,
            credentials: "same-origin"
          });
          if (!r2.ok) {
            console.error("Eco toggle hata", await r2.text());
            return;
          }
          const upd = await r2.json();
          done = upd.completed;
          btn.classList.toggle("completed", done);
          // XP bar güncelle
          if (upd.new_xp !== undefined && upd.percent !== undefined) {
            document.querySelector(".hp-xp-fill").style.width = `${upd.percent}%`;
            document.querySelector(".hp-xp-label").textContent = `${upd.new_xp.toFixed(1)} XP`;
          }
        });
        label.appendChild(btn);

        // — başlık & açıklama
        const info = document.createElement("div");
        const t = document.createElement("div");
        t.className = "task-title";
        t.textContent = action.title;
        const d = document.createElement("div");
        d.className = "task-desc";
        d.textContent = action.description || "";
        info.append(t, d);
        label.appendChild(info);

        // — XP etiketi
        const xp = document.createElement("div");
        xp.className = "task-xp";
        xp.textContent = `${action.xp_earned.toFixed(1)} XP`;
        label.appendChild(xp);

        ecoContainer.appendChild(label);
      });
    }
  } catch (err) {
    console.error("Eco yükleme hatası:", err);
  }
}

// ——— Sayfa yüklendiğinde yükle ve global fonksiyon tanımla ———
document.addEventListener("DOMContentLoaded", () => {
  window.reloadTasks = loadTasks;  // chat.js tarafından çağrılabilir
  loadTasks();
});
