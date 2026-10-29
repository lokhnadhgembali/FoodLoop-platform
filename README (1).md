# FoodLoop

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)

A web platform that moves surplus food from the places that have too much to the shelters and NGOs that don't have enough, and tracks the waste and emissions saved along the way.

---

## Problem

Restaurants, college hostels and event caterers regularly end up with large amounts of cooked food that is still safe to eat. Most of it goes to the landfill because nobody can arrange a pickup in time.

On the other side, local NGOs and relief shelters often run short of food. They can't see what's available nearby, or how long it stays safe to collect.

## Overview

FoodLoop connects food donors with verified recipient agencies in real time. Donors post surplus food with a quantity and a pickup window. Recipients browse what's nearby, reserve what they need, and collect it. A 4-digit PIN confirms each handover. Reservations update inventory atomically, so the same food can't be claimed twice. Dashboards show how much food was diverted from landfills and the carbon emissions that avoided.

---

## Key features

### Donors
- Register as a restaurant, hostel or caterer.
- Post surplus listings with food type, quantity, pickup window and location.
- See which listings are open, reserved or collected.
- Confirm a handover by entering the recipient's PIN.

### Recipients and NGOs
- Register as a recipient agency and wait for admin verification.
- Browse live surplus listings and see the collection window for each.
- Reserve a portion of a listing.
- Get a PIN for every reservation to show at pickup.

### Admin
- Review and approve or reject recipient agencies.
- Monitor all users, listings and reservations.
- Remove fraudulent or expired entries.

### 4-digit PIN verification
- A PIN is generated when a reservation is confirmed.
- The recipient shows it at pickup and the donor enters it to complete the handover.
- A listing counts as collected only after the PIN matches.

### Atomic inventory updates
- Reservations use a single conditional update in MongoDB, so quantity is checked and reduced in one step.
- Two recipients can't reserve the last portion at the same moment.

### Impact analytics
- Interactive dashboards built with Streamlit.
- Total food rescued (kg), meals served, pickups completed and donors active.
- Estimated carbon emissions averted, based on a configurable emission factor per kg of food.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| Web framework | Streamlit |
| Database | MongoDB |
| DB driver | PyMongo |
| Data handling | Pandas |
| Charts | Plotly |
| Config | python-dotenv |

---

## Getting started

### Prerequisites

- Python 3.10 or newer
- Git
- A MongoDB instance, either local or a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster

### 1. Clone the repository

```bash
git clone https://github.com/lokhnadhgembali/FoodLoop-platform.git
cd FoodLoop-platform
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=foodloop
CO2_FACTOR_PER_KG=2.5
```

| Variable | Description |
|---|---|
| `MONGO_URI` | Connection string for your MongoDB instance. For Atlas, use the `mongodb+srv://...` string. |
| `DB_NAME` | Name of the database FoodLoop will use. |
| `CO2_FACTOR_PER_KG` | kg of CO2e counted as avoided for each kg of food rescued. Adjust it to the figure you want to use. |

Keep `.env` out of version control by adding it to `.gitignore`.

### 5. Run the app

```bash
streamlit run app.py
```

Streamlit will open the app at `http://localhost:8501`.

---

## MongoDB collections

| Collection | Purpose | Main fields |
|---|---|---|
| `users` | Donors, recipients and admins | name, email, password hash, role, organisation, verified, created_at |
| `donations` | Surplus food listings | donor_id, food_item, quantity_available, unit, pickup_from, pickup_until, location, status |
| `reservations` | Claims made by recipients | donation_id, recipient_id, quantity, pin, status, created_at, collected_at |
| `impact_logs` | One record per completed pickup, used by the dashboards | reservation_id, kg_rescued, meals, co2_averted, date |

Field names above are a starting point. Update them to match your actual schema.

### How a reservation stays atomic

```python
result = donations.find_one_and_update(
    {"_id": donation_id, "quantity_available": {"$gte": requested_qty}},
    {"$inc": {"quantity_available": -requested_qty}},
)
if result is None:
    # Not enough left, another recipient got there first
    ...
```

The quantity check and the decrement happen in one operation, so the stock can't go negative.

---

## Project structure

```
FoodLoop-platform/
├── app.py              # Streamlit entry point
├── requirements.txt
├── .env                # Local config (not committed)
└── ...
```

Adjust this to match your folders as the project grows.

---

## Contributing

Issues and pull requests are welcome. For larger changes, open an issue first so we can talk it through.

## License

Add a license of your choice, for example MIT, and link it here.
