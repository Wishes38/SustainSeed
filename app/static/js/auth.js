document.addEventListener("DOMContentLoaded", () => {

  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {
        username: registerForm.username.value,
        email: registerForm.email.value,
        first_name: registerForm.first_name.value,
        last_name: registerForm.last_name.value,
        password: registerForm.password.value,
        role: registerForm.role.value,
        phone_number: registerForm.phone_number.value
      };
      const msgDiv = document.getElementById("register-msg");
      try {
        const res = await fetch("/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        if (res.ok) {
          msgDiv.style.color = "green";
          msgDiv.textContent = "Kayıt başarılı! Yönlendiriliyorsunuz...";
          setTimeout(() => { window.location.href = "/auth/login"; }, 1500);
        } else {
          const err = await res.json();
          msgDiv.style.color = "red";
          msgDiv.textContent = err.detail || "Kayıt sırasında hata oluştu.";
        }
      } catch (error) {
        msgDiv.style.color = "red";
        msgDiv.textContent = "Sunucu bağlantı hatası.";
      }
    });
  }

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new URLSearchParams();
      formData.append("username", loginForm.username.value);
      formData.append("password", loginForm.password.value);

      const msgDiv = document.getElementById("login-msg");
      try {
        const res = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData
        });

        if (res.ok) {
          const data = await res.json();
          document.cookie = `access_token=${data.access_token}; Path=/`;
          msgDiv.style.color = "green";
          msgDiv.textContent = "Giriş başarılı! Anasayfaya yönlendiriliyorsunuz...";
          setTimeout(() => { window.location.href = "/"; }, 1000);
        } else {
          const err = await res.json();
          msgDiv.style.color = "red";
          msgDiv.textContent = err.detail || "Giriş hatası.";
        }
      } catch (error) {
        msgDiv.style.color = "red";
        msgDiv.textContent = "Sunucu bağlantı hatası.";
      }
    });
  }
});
