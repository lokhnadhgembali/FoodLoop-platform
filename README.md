# FoodLoop – Smart Surplus Food Redistribution Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.60%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MongoDB Atlas](https://img.shields.io/badge/MongoDB%20Atlas-PyMongo-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![Plotly](https://img.shields.io/badge/Plotly-Data%20Viz-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Google Gemini API](https://img.shields.io/badge/Google%20GenAI-Gemini%20API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![UN SDG](https://img.shields.io/badge/UN%20SDG-12%20%7C%208-E5243B)](https://sdgs.un.org/)

**FoodLoop** is an intelligent, real-time surplus food redistribution and waste reduction platform. It bridges the gap between commercial kitchens, university messes, banquet halls, and hostels with verified NGOs, food banks, and relief shelters before edible food goes to waste.

Built directly in support of:
- **UN Sustainable Development Goal 12:** Responsible Consumption & Production (Target 12.3: Halving per capita global food waste).
- **UN Sustainable Development Goal 8:** Decent Work & Economic Growth (Strengthening community resilience and resource efficiency).

---

## 🌟 Highlights & Architecture

- **SaaS-Style Micro-UI:** Custom Streamlit injection featuring floating pill navbars, light cream palettes (`#F8F3F0`), royal blue accents (`#014BAA`), and responsive card grids.
- **Role-Isolated Dashboards:** Distinct workflows tailored for **Donors**, **NGOs / Recipients**, and **System Administrators**.
- **Tamper-Resistant 4-Digit PIN Handshake:** Cryptographically sound, single-use handover verification tokens ensuring physical pickup accountability.
- **Atomic Inventory Updates:** MongoDB conditional decrement (`$inc` with `$gte`) preventing duplicate reservations or race conditions.
- **Automated Fallback Architecture:** Automatically utilizes PyMongo with MongoDB Atlas when configured, with an embedded in-memory mock engine for testing without external dependencies.
- **Real-Time Sustainability Ledger:** Live dynamic calculation of kilograms diverted, meals rescued, and carbon emissions averted ($\sim 2.5\text{ kg CO}_2\text{e}$ saved per kilogram rescued).

---

## 👥 Role Workflows

### 1. Food Donors (Commercial Kitchens, Messes, Caterers)
- **Publish Surplus Food:** Post listings specifying food name, category (*Cooked Meals, Bakery, Produce, Packaged, Beverages*), quantity in kg, estimated servings, storage guidelines, and safe pickup window (hours).
- **Manage Requests:** Review incoming claims from verified recipient NGOs in real time with one-click approval or rejection.
- **Handover Verification:** Input the recipient NGO's secret 4-digit PIN at the pickup counter to authenticate the collector and mark the donation as completed.

### 🤝 2. Recipient NGOs & Food Banks
- **Live Marketplace:** Filter and browse available surplus food within their vicinity with dynamic countdown timers and urgent expiry badges (<2 hours).
- **Claim Food:** Request portions or entire listings with instant quantity validation.
- **PIN Pass Ticket:** Automatically receive a generated 4-digit PIN ticket upon donor approval to present during physical collection.

### ⚙️ 3. System Administrator
- **Organization Vetting:** Verify or revoke credentials for registering donors and NGOs to ensure food safety and trust.
- **Platform Monitoring:** Audit active food listings, pending reservations, and transaction history.
- **Data Export:** Download comprehensive audit logs in CSV format for sustainability and regulatory reporting.

---

## 🔐 4-Digit PIN Handshake Mechanism

```
[NGO Claims Food] ──► [Donor Approves] ──► [Secret 4-Digit PIN Issued to NGO]
                                                            │
[Completed Impact Logged] ◄── [Donor Validates PIN at Venue] ◄──┘
```

1. **Claim Submission:** NGO claims a quantity of surplus food.
2. **Approval & Token Generation:** Upon donor approval, a secure, 4-digit numeric PIN is generated and visible exclusively on the NGO's **"My Passes"** ticket.
3. **Physical Verification:** At pickup, the recipient presents the PIN. The donor enters the PIN into the verification terminal.
4. **Instant Settlement:** When verified, the listing is finalized, recorded to `donation_history`, and impact metrics update across the platform.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend / UI** | Streamlit 1.60+, HTML5, Custom CSS | Modern SaaS responsive interface |
| **Backend / Runtime** | Python 3.10+ | Business logic, session routing, and API layer |
| **Database** | MongoDB Atlas / PyMongo | Scalable NoSQL store for users, listings, requests, and history |
| **Data & Visualizations** | Plotly Express & Pandas | Weekly donation trends, category distributions, status donuts |
| **AI Integration** | Google GenAI SDK (`google-genai`) | Gemini-powered surplus shelf-life and routing intelligence |
| **Authentication & Security** | Python `hashlib` (SHA-256) / `bcrypt` | Secure salted password hashing and role-based access control |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- MongoDB Atlas cluster connection string (or run in-memory fallback mode)

### 1. Clone the Repository
```bash
git clone https://github.com/lokhnadhgembali/FoodLoop-platform.git
cd FoodLoop-platform
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (refer to `.env.example`):
```bash
cp .env.example .env
```
Populate `.env` with your credentials:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/foodloopDB
DB_NAME=foodloopDB
GEMINI_API_KEY=your_gemini_api_key_here
```
> *Note: If `MONGODB_URI` is omitted or inaccessible, FoodLoop automatically boots with an active in-memory test database seeded with demo listings.*

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` (or the configured port).

---

## ⚡ 1-Click Demo Accounts

For instant evaluation and demonstrations, the login portal includes pre-configured 1-click credentials:

| Role | Organization / User | Email | Password |
|---|---|---|---|
| **Donor** | LPU Central Mess | `mess@lpu.in` | `demo123` |
| **NGO** | Robin Hood Army - Phagwara | `rha@ngo.org` | `demo123` |
| **Admin** | FoodLoop System Admin | `admin@foodloop.in` | `demo123` |

---

## 📂 Project Structure

```
FoodLoop-platform/
├── app.py                  # Main Streamlit application router & session controller
├── styles.py               # Custom design system, typography & injected CSS
├── database.py             # MongoDB Atlas connection, seeding & atomic CRUD operations
├── utils.py                # Impact calculators, PIN generator, countdown & CSV export
├── requirements.txt        # Pinned python project dependencies
├── .env.example            # Safe environment template
├── .gitignore              # Strict secret and cache exclusion rules
├── logo.png                # Original brand identity badge
├── logo_blue.png           # Theme-matched light mode brand asset
├── logo_white.png          # Dark surface brand asset
└── views/
    ├── __init__.py         # Modular package marker
    ├── landing.py          # Hero showcase, SDG highlights & live platform pulse
    ├── auth.py             # Split-screen login, multi-role registration & demo logins
    ├── donor.py            # Surplus food publishing, request approvals & PIN verification
    ├── recipient.py        # Live surplus marketplace, claim engine & PIN pass tickets
    ├── admin.py            # Organization verification, platform monitors & CSV audits
    └── analytics.py        # Plotly charts, weekly velocity & carbon avoidance counters
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
