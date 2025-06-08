# SustainSeed 🌱 — Sana bir tohum, gezegene umut  
> **“Ekranda başlar, dünyada yeşerir.”**  
> Küçük sürdürülebilir eylemleri oyunlaştırarak gerçek hayatta ağaçlandırmaya dönüştüren yapay zekâ destekli ekosistem.

---

## Hakkımızda
“Sana bir tohum, gezegene umut. Ekranda başlar, dünyada yeşerir. Yaz, büyüt, yeşert! 🌱🌍”  

SustainSeed AI, yalnızca dijital bir bitki yetiştirme uygulaması değil; küçük eylemlerle büyük anlamlar yeşerten bir deneyimdir.  
Bir tohum büyüdüğünde yalnızca bir filiz ortaya çıkmaz—geleceğe dair umutlar da kök salar.  

- 🌿 “Bugün termosla kahve aldım” dediğinde dijital tohumun azıcık büyür.  
- 🌿 “Lambaları kapattım, bisikletle geldim” dedikçe filiz serpilmeye devam eder.  
- 🌿 Büyüyen sadece bitkin değildir… dünyanın da daha yaşanabilir hâle geldiğini görürsün.

Misyonumuz sürdürülebilirliği sıkıcı yapılacaklar listeleri yerine **oyun, sohbet ve günlük alışkanlık** hâline getirmek.  
Gelecekte dijital ormandaki her ağaç, gerçek hayatta da bir fidana dönüşecek.

---

## Öne Çıkan Özellikler
| Başlık | Ayrıntı |
| ------ | ------- |
| 🧠 **AI Sohbet & Görev Motoru** | Google Gemini Flash-2.5, bitkinin seviyesine göre farklı kişilikle cevap üretir. “Görev” modunda JSON görev döner. |
| 🎮 **Oyunlaştırılmış İlerleme** | 6 evre (Seed → Mature Tree). XP birikince bitki büyür, kişiliği olgunlaşır. Olgun ağaç “or­man”a eklenir, yeni tohum döngüye girer. |
| 📅 **Günlük Görev Planlayıcı** | Sunucu scheduler’ı her gün otomatik görev atar, tamamlayınca XP kazandırır. |
| 🔐 **JWT Kimlik & Swagger UI** | Güvenli API; otomatik dokümantasyon `/docs`. |
| 🗄️ **PostgreSQL + Alembic** | Tam şema göçleri; `alembic revision --autogenerate` ile kolay migration. |
| ☁️ **Docker Compose** | Veritabanı + API tek komutla ayağa kalkar. |
| 🌳 **Gerçek Fidan Bağışı (Planlanan)** | Dijital ormandaki her bin ağaç, partner STK’lara fidan olarak dikilir. |

---

## Teknik Yığın
Backend   : FastAPI · Python 3.12 · SQLAlchemy 2 · Alembic · JWT  
AI        : Google Generative AI (Gemini Flash-2.5)  
Frontend  : React 18 + Vite · Jinja2 (SSR) · HTML/CSS/JS  
Veritabanı: PostgreSQL 16 (Docker)  
DevOps    : Docker Compose · GitHub Actions CI · pre-commit (ruff, black)  
Tasarım   : Adobe Illustrator · After Effects

---

## Kurulum & Çalıştırma

  ### 1 ▪ Docker
 ````` 
  git clone https://github.com/Wishes38/SustainSeed.git
  
  cd SustainSeed 
  
  cp .env.example .env      # API anahtarlarını doldur 
  
  docker compose up --build
  `````
  #### ➜ API      : http://localhost:8000 
  #### ➜ Swagger  : http://localhost:8000/docs 
  
  ### 2 ▪ Yerel Venv
  `````
  python -m venv venv && source venv/bin/activate
  
  pip install -r requirements.txt
  
  alembic upgrade head
  
  export GENAI_API_KEY=<anahtar>
  
  uvicorn app.main:app --reload
  `````
  ### .env Örneği:
  
    POSTGRES_USER=docker
    POSTGRES_PASSWORD=docker
    POSTGRES_DB=susseeddb
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    
    GENAI_API_KEY=your_google_api_key
    JWT_SECRET=my_super_secret


## API Uç Noktaları

### Genel (Jinja2 Sayfaları)
| Metot | URL | Açıklama  |
|-------|-----|-----------|
| `GET` | `/`            | Home |
| `GET` | `/profile`     | Profil sayfası |
| `GET` | `/tasks`       | Görevler sayfası |
| `GET` | `/settings`    | Ayarlar |
| `GET` | `/about`       | Hakkında |

---

### Authentication
| Metot | URL | Açıklama |
|-------|-----|----------|
| `GET`  | `/auth/register`     | Register Page |
| `POST` | `/auth/register`     | Register User |
| `GET`  | `/auth/login`        | Login Page |
| `POST` | `/auth/login`        | **Login for Access Token** |
| `GET`  | `/auth/me`           | Get Current User Info |
| `PUT`  | `/auth/me`           | Update Current User Info |
| `DELETE` | `/auth/me`         | Delete Current User |
| `POST` | `/auth/update-xp`    | Update User XP |
| `GET`  | `/auth/logout`       | Auth Logout |
| `GET`  | `/auth/profile`      | Profile Page |

---

### Eco Actions
| Metot | URL | Açıklama |
|-------|-----|----------|
| `GET`  | `/eco-actions/`                             | Kullanıcının tüm eko eylemleri |
| `POST` | `/eco-actions/`                             | Yeni eylem oluştur |
| `POST` | `/eco-actions/{eco_action_id}/complete`     | Eylemi tamamla |
| `POST` | `/eco-actions/{eco_action_id}/uncomplete`   | Tamamlamayı geri al |

## Örnek Chat isteği:
POST /chatbot
`````
  Authorization: Bearer <JWT>
  {
    "message": "Bugün çevreci bir görev önerir misin?"
  }
  Yanıt (“Görev” modu):
  {
    "mode": "task",
    "task": {
      "title": "Duş süresini 5 dakikaya düşür",
      "description": "Bugün duş süreni 5 dakikayla sınırlayarak hem su hem enerji tasarruf et!",
      "xp_earned": 6
    }
  }
`````
## Bitki Evrimi ve XP Mekaniği

| Seviye               | XP    | Davranış Özeti                   |
| -------------------- | ----- | -------------------------------- |
| Seed                 | 0–9   | Utangaç, kısa sorular            |
| Seedling             | 10–19 | Neşeli, emoji kullanır           |
| Seedling with Leaves | 20–34 | Meraklı, bilgi paylaşır          |  
| Young Tree           | 35–49 | Olgun, planlayıcı                |
| Growing Tree         | 50–79 | Koruyucu, derin öğütler          |
| Mature Tree          | ≥80   | Bilge; ağaç olur, ormana eklenir |


## XP Devir İşlemi(XP ≥ 80 olduğunda)
`````
tree_count += 1
xp         -= 80
plant_stage = Seed
`````


| Akış / Sayfa | Görsel |
|--------------|--------|
| Giriş Ekranı | <img src="https://github.com/user-attachments/assets/66766b70-1263-4a49-acee-177b286aa9b6?raw=true" width="750"/> |
| Kayıt Ekranı | <img src="https://github.com/user-attachments/assets/4da86a46-f647-4426-8282-f7d08ca03a87?raw=true" width="750"/> |
| Bitki Sohbeti – Tohum | <img src="https://github.com/user-attachments/assets/5f0eaae4-d686-49c7-9d09-91f8004c09ca?raw=true" width="750"/> |
| Bitki Sohbeti – Fidan | <img src="https://github.com/user-attachments/assets/76e0d51d-26e5-435c-8a97-6d1130bf797d?raw=true" width="750"/> |
| Bitki Sohbeti – Ağaç | <img src="https://github.com/user-attachments/assets/cbc412ac-cf7b-4645-9d30-3772b213a8b3?raw=true" width="750"/> |
| Günlük Görevler & Eco Actions | <img src="https://github.com/user-attachments/assets/797b6762-1391-4700-aa42-619b01e2d21c?raw=true" width="750"/> |
| Profil Sayfası | <img src="https://github.com/user-attachments/assets/6e8e6644-c973-449e-9402-acaabc2fb57c?raw=true" width="750"/> |





