document.addEventListener("DOMContentLoaded", async () => {
  // Cookie'den token okumak
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

  // 1) Mevcut kullanıcı bilgilerini çek
  try {
    const res = await fetch("/auth/me", { headers });
    if (!res.ok) throw new Error("Profil bilgileri alınamadı");
    const user = await res.json();

    // Formu doldur
    document.getElementById("username").value     = user.username || "";
    document.getElementById("email").value        = user.email || "";
    document.getElementById("first_name").value   = user.first_name || "";
    document.getElementById("last_name").value    = user.last_name || "";
    document.getElementById("phone_number").value = user.phone_number || "";
  } catch (e) {
    console.error("Profil yükleme hatası:", e);
  }

  // 2) Güncelleme işlemi
  const form = document.getElementById("profile-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      first_name: document.getElementById("first_name").value,
      last_name:  document.getElementById("last_name").value,
      phone_number: document.getElementById("phone_number").value
    };

    try {
      const res = await fetch("/auth/me", {
        method: "PUT",
        headers,
        body: JSON.stringify(data)
      });
      const msgDiv = document.getElementById("profile-msg");
      if (res.ok) {
        msgDiv.textContent = "Güncelleme başarılı!";
        msgDiv.style.color = "green";
      } else {
        const err = await res.json();
        msgDiv.textContent = err.detail || "Güncelleme hatası";
        msgDiv.style.color = "red";
      }
    } catch (e) {
      const msgDiv = document.getElementById("profile-msg");
      msgDiv.textContent = "Sunucu hatası.";
      msgDiv.style.color = "red";
      console.error("Profil güncelleme hatası:", e);
    }
  });
});
