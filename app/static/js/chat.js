const token =
const headers = {
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
};

const res = await fetch("/chatbot/", { method: "POST", headers });
const data = await res.json();

if (data.mode === "task") {
  console.log("Yeni görev:", data.content);
}
