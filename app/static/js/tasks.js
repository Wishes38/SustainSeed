document.addEventListener("DOMContentLoaded", async () => {
  function getCookie(name) {
    const v = "; " + document.cookie;
    const parts = v.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  const token = getCookie("access_token");
  if (!token) return console.warn("Token bulunamadı.");

  const headers = {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  };

  function makeDailyToggle(asg) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "task-complete-circle";
    if (asg.completed) btn.classList.add("completed");
    btn.addEventListener("click", async () => {
      const url = asg.completed
        ? `/daily-tasks/uncomplete/${asg.id}`
        : `/daily-tasks/complete/${asg.id}`;
      const res = await fetch(url, { method: "POST", headers });
      if (!res.ok) return console.error("Daily toggle hatası", await res.text());
      const data = await res.json();
      asg.completed = data.completed;
      btn.classList.toggle("completed", asg.completed);

      if (data.percent !== undefined) {
        document.querySelector(".hp-xp-fill").style.width = `${data.percent}%`;
      }
      if (data.new_xp !== undefined) {
        document.querySelector(".hp-xp-label").textContent = `${data.new_xp.toFixed(1)} XP`;
      }
    });
    return btn;
  }

  try {
    const res = await fetch("/daily-tasks/my-assignments", { headers });
    if (res.status === 401) throw new Error("Daily unauthorized");
    const daily = await res.json();
    const dailyC = document.getElementById("daily-tasks-body");
    dailyC.innerHTML = "";
    if (!daily.length) {
      dailyC.textContent = "Yeni görev bulunamadı.";
    } else {
      daily.forEach(asg => {
        const lbl = document.createElement("label");
        lbl.className = "task-item";
        lbl.appendChild(makeDailyToggle(asg));
        const info = document.createElement("div");
        const title = document.createElement("div");
        title.className = "task-title";
        title.textContent = asg.daily_task.title;
        const desc = document.createElement("div");
        desc.className = "task-desc";
        desc.textContent = asg.daily_task.description;
        info.append(title, desc);
        lbl.appendChild(info);
        const xp = document.createElement("div");
        xp.className = "task-xp";
        xp.textContent = `${asg.daily_task.xp_earned.toFixed(1)} XP`;
        lbl.appendChild(xp);
        dailyC.appendChild(lbl);
      });
    }
  } catch (e) {
    console.error("Daily yükleme hatası:", e);
  }

  let logs = [];
  try {
    const lRes = await fetch("/user-task-logs", { headers });
    if (lRes.ok) logs = await lRes.json();
  } catch (e) {
    console.error("Log fetch hatası:", e);
  }

function makeEcoToggle(action) {
  let done = logs.some(log => log.eco_action_id === action.id && log.completed);
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "task-complete-circle";
  if (done) btn.classList.add("completed");

  btn.addEventListener("click", async () => {
    const url = done
      ? `/eco-actions/${action.id}/uncomplete`
      : `/eco-actions/${action.id}/complete`;
    const res = await fetch(url, { method: "POST", headers });
    if (!res.ok) {
      console.error("Eco toggle hatası", await res.text());
      return;
    }
    const { completed, new_xp, percent } = await res.json();

    done = completed;
    btn.classList.toggle("completed", done);

    document.querySelector(".hp-xp-fill").style.width      = `${percent}%`;
    document.querySelector(".hp-xp-label").textContent    = `${new_xp.toFixed(1)} XP`;

    const totalXpEl = document.querySelector(".hp-total-earned-xp-value");
    if (totalXpEl) {
      const treeCount = parseInt(document.querySelector(".hp-tree-count-value").textContent);
      totalXpEl.textContent = (treeCount * 80 + new_xp).toFixed(1);
    }
  });

  return btn;
}


  try {
  const res = await fetch("/eco-actions", { headers });
  if (res.status === 401) throw new Error("Eco unauthorized");
  const eco = await res.json();
  const ecoC = document.getElementById("eco-tasks-body");
  ecoC.innerHTML = "";
  if (!eco.length) {
    ecoC.textContent = "Henüz eco–action yok.";
  } else {
    eco.forEach(action => {
      const lbl = document.createElement("label");
      lbl.className = "task-item";

      lbl.appendChild(makeEcoToggle(action));

      const info = document.createElement("div");
      const title = document.createElement("div");
      title.className = "task-title";
      title.textContent = action.title;
      const desc = document.createElement("div");
      desc.className = "task-desc";
      desc.textContent = action.description || "";
      info.append(title, desc);
      lbl.appendChild(info);

      const xpDiv = document.createElement("div");
      xpDiv.className = "task-xp";
      xpDiv.textContent = `${action.xp_earned.toFixed(1)} XP`;
      lbl.appendChild(xpDiv);

      ecoC.appendChild(lbl);
    });
  }
} catch (e) {
  console.error("Eco yükleme hatası:", e);
}
});
