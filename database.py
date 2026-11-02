"""
database.py  -  FoodLoop · MongoDB Atlas connection, schema, seeding & CRUD
Automatically falls back to an in-memory mock if MONGODB_URI is not set.
"""
from __future__ import annotations

import os
import hashlib
import random
from datetime import datetime, timezone, timedelta
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# ════════════════════════════════════════════════════════════════════════════
# IN-MEMORY MOCK (graceful fallback when no MONGODB_URI is configured)
# ════════════════════════════════════════════════════════════════════════════

class _MockResult:
    def __init__(self, ids):
        if isinstance(ids, list):
            self.inserted_ids = ids
        else:
            self.inserted_id = ids


class _MockCollection:
    def __init__(self):
        self._docs: list[dict] = []
        self._seq = 0

    def _new_id(self) -> str:
        self._seq += 1
        return f"mock_{self._seq:08x}"

    def _match(self, query: dict | None) -> list[dict]:
        if not query:
            return list(self._docs)
        out = []
        for doc in self._docs:
            if all(self._field_match(doc, k, v) for k, v in query.items()):
                out.append(doc)
        return out

    @staticmethod
    def _field_match(doc, key, val) -> bool:
        dv = doc.get(key)
        if isinstance(val, dict):
            for op, ov in val.items():
                if op == "$gt"  and not (dv is not None and dv > ov):  return False
                if op == "$gte" and not (dv is not None and dv >= ov): return False
                if op == "$lt"  and not (dv is not None and dv < ov):  return False
                if op == "$lte" and not (dv is not None and dv <= ov): return False
                if op == "$in"  and dv not in ov:                      return False
                if op == "$ne"  and dv == ov:                          return False
            return True
        return dv == val

    # ── Write ────────────────────────────────────────────────────────────────
    def insert_one(self, doc: dict) -> _MockResult:
        doc = dict(doc)
        doc.setdefault("_id", self._new_id())
        self._docs.append(doc)
        return _MockResult(doc["_id"])

    def insert_many(self, docs: list[dict]) -> _MockResult:
        ids = [self.insert_one(d).inserted_id for d in docs]
        return _MockResult(ids)

    def update_one(self, query, update, upsert=False):
        hits = self._match(query)
        if hits:
            doc = hits[0]
            if "$set" in update:
                doc.update(update["$set"])
            if "$inc" in update:
                for k, v in update["$inc"].items():
                    doc[k] = doc.get(k, 0) + v
        elif upsert:
            new_doc = {**query}
            if "$set" in update:
                new_doc.update(update["$set"])
            self.insert_one(new_doc)

    def delete_one(self, query):
        hits = self._match(query)
        if hits:
            self._docs.remove(hits[0])

    # ── Read ─────────────────────────────────────────────────────────────────
    def find(self, query=None, *_, **__) -> "_MockCursor":
        return _MockCursor(self._match(query))

    def find_one(self, query=None) -> Optional[dict]:
        hits = self._match(query)
        return hits[0] if hits else None

    def count_documents(self, query=None) -> int:
        return len(self._match(query))

    def create_index(self, *_, **__): pass

    def aggregate(self, pipeline) -> list:
        # Basic $group support for analytics
        docs = list(self._docs)
        for stage in pipeline:
            if "$match" in stage:
                q = stage["$match"]
                docs = [d for d in docs if all(
                    _MockCollection._field_match(d, k, v) for k, v in q.items()
                )]
            elif "$group" in stage:
                grp = stage["$group"]
                _id_key = grp.get("_id")
                buckets: dict = {}
                for doc in docs:
                    key = doc.get(_id_key.lstrip("$")) if isinstance(_id_key, str) and _id_key.startswith("$") else _id_key
                    if key not in buckets:
                        buckets[key] = {"_id": key}
                        for field, agg in grp.items():
                            if field == "_id": continue
                            if "$sum" in agg:
                                buckets[key][field] = 0
                            elif "$count" in agg:
                                buckets[key][field] = 0
                    for field, agg in grp.items():
                        if field == "_id": continue
                        if "$sum" in agg:
                            src = agg["$sum"]
                            if isinstance(src, str) and src.startswith("$"):
                                buckets[key][field] += doc.get(src.lstrip("$"), 0) or 0
                            else:
                                buckets[key][field] += src
                docs = list(buckets.values())
            elif "$sort" in stage:
                srt = stage["$sort"]
                for k, direction in reversed(list(srt.items())):
                    docs.sort(key=lambda d: (d.get(k) is None, d.get(k)), reverse=(direction == -1))
            elif "$limit" in stage:
                docs = docs[: stage["$limit"]]
        return docs


class _MockCursor:
    def __init__(self, docs): self._docs = list(docs)
    def sort(self, key, direction=1):
        self._docs.sort(key=lambda d: (d.get(key) is None, d.get(key)), reverse=(direction == -1))
        return self
    def limit(self, n): self._docs = self._docs[:n]; return self
    def __iter__(self): return iter(self._docs)
    def __list__(self): return self._docs


class _MockDB:
    def __init__(self): self._cols: dict[str, _MockCollection] = {}
    def __getitem__(self, name):
        if name not in self._cols: self._cols[name] = _MockCollection()
        return self._cols[name]
    def list_collection_names(self): return list(self._cols.keys())
    class admin:
        @staticmethod
        def command(cmd): return {"ok": 1}


# ════════════════════════════════════════════════════════════════════════════
# CONNECTION
# ════════════════════════════════════════════════════════════════════════════

_client = None
_mock_db: Optional[_MockDB] = None
MOCK_MODE = False


def get_db():
    global _client, _mock_db, MOCK_MODE
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        MOCK_MODE = True
        if _mock_db is None:
            _mock_db = _MockDB()
            _seed(_mock_db)
        return _mock_db
    if _client is None:
        try:
            from pymongo import MongoClient
            test_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            test_client.admin.command("ping")
            _client = test_client
        except Exception as e:
            print(f"MongoDB connection notice ({e}). Using robust fallback mode.")
            MOCK_MODE = True
            if _mock_db is None:
                _mock_db = _MockDB()
                _seed(_mock_db)
            return _mock_db
    try:
        db = _client[os.getenv("DB_NAME", "foodloopDB")]
        return db
    except Exception:
        if _mock_db is None:
            _mock_db = _MockDB()
            _seed(_mock_db)
        return _mock_db


def get_collections(db=None):
    if db is None:
        db = get_db()
    return {
        "users":             db["users"],
        "food_listings":     db["food_listings"],
        "donation_requests": db["donation_requests"],
        "donation_history":  db["donation_history"],
        "impact_records":    db["impact_records"],
    }


# ════════════════════════════════════════════════════════════════════════════
# PASSWORD HASHING
# ════════════════════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


# ════════════════════════════════════════════════════════════════════════════
# INDEXES
# ════════════════════════════════════════════════════════════════════════════

def ensure_indexes(db):
    try:
        from pymongo import ASCENDING
        db["users"].create_index("email", unique=True)
        db["food_listings"].create_index([("pickup_deadline", ASCENDING)])
        db["food_listings"].create_index("status")
        db["food_listings"].create_index("donor_id")
        db["donation_requests"].create_index("listing_id")
        db["donation_requests"].create_index("recipient_id")
    except Exception:
        pass


# ════════════════════════════════════════════════════════════════════════════
# SEED DATA
# ════════════════════════════════════════════════════════════════════════════

CATEGORIES  = ["Cooked Meals", "Bakery", "Produce", "Dairy", "Packaged"]
FOOD_NAMES  = {
    "Cooked Meals": ["Dal Makhani & Rice", "Paneer Butter Masala", "Chole Bhature", "Biryani", "Rajma Chawal"],
    "Bakery":       ["Whole Wheat Bread", "Dinner Rolls", "Muffins", "Croissants", "Cake Slices"],
    "Produce":      ["Mixed Vegetables", "Fresh Tomatoes", "Spinach Leaves", "Carrots", "Apples"],
    "Dairy":        ["Pasteurised Milk (2L)", "Paneer Block", "Curd Packets", "Butter", "Cheese"],
    "Packaged":     ["Biscuit Packets", "Instant Noodles", "Juice Cartons", "Chips", "Energy Bars"],
}
STORAGE     = ["Room Temp", "Refrigerated", "Frozen"]


def _seed(db):
    """Insert demo accounts + 90 days of rich historical data."""
    cols = get_collections(db)

    # ── Users ────────────────────────────────────────────────────────────────
    if cols["users"].count_documents({"email": "mess@lpu.in"}) > 0:
        return  # already seeded

    users_data = [
        {
            "name": "LPU Central Mess", "email": "mess@lpu.in",
            "password_hash": hash_password("demo123"), "role": "donor",
            "phone": "9876543210", "address": "LPU Campus, Phagwara, Punjab",
            "is_verified": True, "reward_points": 150,
        },
        {
            "name": "Robin Hood Army - Phagwara", "email": "rha@ngo.org",
            "password_hash": hash_password("demo123"), "role": "recipient",
            "phone": "9876543211", "address": "Phagwara, Punjab",
            "is_verified": True, "reward_points": 0,
        },
        {
            "name": "Feeding India - Jalandhar", "email": "fi@ngo.org",
            "password_hash": hash_password("demo123"), "role": "recipient",
            "phone": "9876543215", "address": "Jalandhar, Punjab",
            "is_verified": True, "reward_points": 0,
        },
        {
            "name": "Hotel Radisson Surplus Kitchen", "email": "radisson@donor.in",
            "password_hash": hash_password("demo123"), "role": "donor",
            "phone": "9876543213", "address": "GT Road, Jalandhar, Punjab",
            "is_verified": True, "reward_points": 80,
        },
        {
            "name": "FoodLoop System Admin", "email": "admin@foodloop.in",
            "password_hash": hash_password("demo123"), "role": "admin",
            "phone": "9876543212", "address": "Jalandhar, Punjab",
            "is_verified": True, "reward_points": 0,
        },
    ]
    res = cols["users"].insert_many(users_data)
    donor1_id   = str(res.inserted_ids[0])
    donor2_id   = str(res.inserted_ids[3])
    recip1_id   = str(res.inserted_ids[1])
    recip2_id   = str(res.inserted_ids[2])

    now = datetime.now(timezone.utc)

    # ── Historical donation_history (90 days, ~120 records) ─────────────────
    history_docs = []
    random.seed(42)
    donors = [
        (donor1_id, "LPU Central Mess"),
        (donor2_id, "Hotel Radisson Surplus Kitchen"),
    ]
    recipients = [
        (recip1_id, "Robin Hood Army - Phagwara"),
        (recip2_id, "Feeding India - Jalandhar"),
    ]
    for day_offset in range(90, 0, -1):
        # 0–3 donations per day
        n = random.randint(0, 3)
        for _ in range(n):
            cat = random.choice(CATEGORIES)
            qty = round(random.uniform(2, 25), 1)
            d_id, d_name = random.choice(donors)
            r_id, r_name = random.choice(recipients)
            completed = now - timedelta(days=day_offset, hours=random.uniform(0, 8))
            history_docs.append({
                "donor_id":       d_id,
                "donor_name":     d_name,
                "recipient_id":   r_id,
                "recipient_name": r_name,
                "food_category":  cat,
                "quantity_kg":    qty,
                "meals_saved":    int(qty * 2),
                "co2e_avoided_kg": round(qty * 2.5, 2),
                "completed_at":   completed,
                "listing_id":     "hist",
                "request_id":     "hist",
            })

    if history_docs:
        cols["donation_history"].insert_many(history_docs)

    # ── Active food_listings (mix of available + other statuses) ─────────────
    listing_docs = []
    for i, (cat, names) in enumerate(FOOD_NAMES.items()):
        for j, fname in enumerate(names[:3]):
            qty   = round(random.uniform(3, 30), 1)
            hours = random.choice([1, 2, 4, 6, 12, 24])
            d_id, d_name = random.choice(donors)
            listing_docs.append({
                "donor_id":          d_id,
                "donor_name":        d_name,
                "food_name":         fname,
                "category":          cat,
                "quantity_kg":       qty,
                "remaining_qty_kg":  qty,
                "servings_estimate": int(qty * 2),
                "storage_condition": random.choice(STORAGE),
                "description":       "",
                "created_at":        now - timedelta(hours=random.randint(1, 4)),
                "pickup_deadline":   now + timedelta(hours=hours),
                "status":            "available",
            })
    # Add a couple of 'reserved' and 'collected' for realism
    for stat in ("reserved", "collected", "expired"):
        cat = random.choice(CATEGORIES)
        qty = round(random.uniform(5, 20), 1)
        d_id, d_name = random.choice(donors)
        listing_docs.append({
            "donor_id": d_id, "donor_name": d_name,
            "food_name": random.choice(FOOD_NAMES[cat]),
            "category": cat, "quantity_kg": qty,
            "remaining_qty_kg": 0 if stat in ("collected", "expired") else qty,
            "servings_estimate": int(qty * 2),
            "storage_condition": "Room Temp",
            "description": "", "created_at": now - timedelta(days=1),
            "pickup_deadline": now - timedelta(hours=2),
            "status": stat,
        })

    cols["food_listings"].insert_many(listing_docs)

    # ── Sample donation_requests (for request status donut chart) ─────────────
    all_listings = list(cols["food_listings"].find({"status": "available"}))
    if all_listings:
        for i, listing in enumerate(all_listings[:6]):
            r_id, r_name = random.choice(recipients)
            status = random.choice(["pending", "approved", "completed", "rejected"])
            pin = str(random.randint(1000, 9999)) if status in ("approved", "completed") else None
            cols["donation_requests"].insert_one({
                "listing_id":      str(listing["_id"]),
                "recipient_id":    r_id,
                "recipient_name":  r_name,
                "donor_id":        listing["donor_id"],
                "donor_name":      listing["donor_name"],
                "food_name":       listing["food_name"],
                "requested_qty_kg": round(listing["quantity_kg"] * 0.5, 1),
                "status":          status,
                "pickup_pin":      pin,
                "created_at":      now - timedelta(hours=random.randint(1, 12)),
            })


def initialize():
    """Call on app startup: connect, index, seed."""
    db = get_db()
    ensure_indexes(db)
    _seed(db)
    return db


# ════════════════════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════════════════════

def get_user_by_email(email: str) -> Optional[dict]:
    cols = get_collections()
    return cols["users"].find_one({"email": email.strip().lower()})


def authenticate(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)
    if user and verify_password(password, user["password_hash"]):
        return user
    return None


def create_user(name, email, password, phone, address, role) -> tuple[bool, str]:
    cols = get_collections()
    if cols["users"].find_one({"email": email.strip().lower()}):
        return False, "Email already registered."
    cols["users"].insert_one({
        "name":          name.strip(),
        "email":         email.strip().lower(),
        "password_hash": hash_password(password),
        "role":          role,
        "phone":         phone.strip(),
        "address":       address.strip(),
        "is_verified":   True,   # Phase 1: auto-verify
        "reward_points": 0,
    })
    return True, "Account created successfully."


# ════════════════════════════════════════════════════════════════════════════
# FOOD LISTINGS
# ════════════════════════════════════════════════════════════════════════════

def add_listing(donor_id, donor_name, food_name, category, quantity_kg,
                servings, storage, safe_hours, description="") -> str:
    from datetime import timedelta
    cols = get_collections()
    now  = datetime.now(timezone.utc)
    doc  = {
        "donor_id":          donor_id,
        "donor_name":        donor_name,
        "food_name":         food_name,
        "category":          category,
        "quantity_kg":       float(quantity_kg),
        "remaining_qty_kg":  float(quantity_kg),
        "servings_estimate": int(servings),
        "storage_condition": storage,
        "description":       description,
        "created_at":        now,
        "pickup_deadline":   now + timedelta(hours=safe_hours),
        "status":            "available",
    }
    result = cols["food_listings"].insert_one(doc)
    return str(result.inserted_id)


def get_available_listings(category=None, location=None) -> list:
    cols = get_collections()
    now  = datetime.now(timezone.utc)
    q: dict = {"status": "available", "pickup_deadline": {"$gt": now}}
    if category and category != "All":
        q["category"] = category
    try:
        from pymongo import ASCENDING
        return list(cols["food_listings"].find(q).sort("pickup_deadline", ASCENDING))
    except Exception:
        docs = list(cols["food_listings"].find(q))
        docs.sort(key=lambda d: d.get("pickup_deadline") or datetime.max.replace(tzinfo=timezone.utc))
        return docs


def get_donor_listings(donor_id: str) -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["food_listings"].find({"donor_id": donor_id}).sort("created_at", DESCENDING))
    except Exception:
        return list(cols["food_listings"].find({"donor_id": donor_id}))


def cancel_listing(listing_id: str):
    from bson import ObjectId
    cols = get_collections()
    try:
        oid = ObjectId(listing_id)
    except Exception:
        oid = listing_id
    cols["food_listings"].update_one({"_id": oid}, {"$set": {"status": "cancelled"}})


def expire_old_listings():
    """Mark past-deadline available listings as expired."""
    cols = get_collections()
    now = datetime.now(timezone.utc)
    cols["food_listings"].update_one(
        {"status": "available", "pickup_deadline": {"$lt": now}},
        {"$set": {"status": "expired"}},
    )


# ════════════════════════════════════════════════════════════════════════════
# DONATION REQUESTS
# ════════════════════════════════════════════════════════════════════════════

def create_request(listing_id: str, recipient_id: str, recipient_name: str, qty_kg: float) -> tuple[bool, str]:
    from bson import ObjectId
    cols = get_collections()
    try:
        oid = ObjectId(listing_id)
    except Exception:
        oid = listing_id
    listing = cols["food_listings"].find_one({"_id": oid})
    if not listing:
        return False, "Listing not found."
    if listing["status"] != "available":
        return False, f"Listing is no longer available (status: {listing['status']})."
    if listing["remaining_qty_kg"] < qty_kg:
        return False, f"Only {listing['remaining_qty_kg']} kg remaining."
    cols["donation_requests"].insert_one({
        "listing_id":      listing_id,
        "donor_id":        listing["donor_id"],
        "donor_name":      listing["donor_name"],
        "food_name":       listing["food_name"],
        "recipient_id":    recipient_id,
        "recipient_name":  recipient_name,
        "requested_qty_kg": float(qty_kg),
        "status":          "pending",
        "pickup_pin":      None,
        "created_at":      datetime.now(timezone.utc),
    })
    return True, "Claim submitted successfully."


def get_requests_for_donor(donor_id: str) -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["donation_requests"].find({"donor_id": donor_id}).sort("created_at", DESCENDING))
    except Exception:
        return list(cols["donation_requests"].find({"donor_id": donor_id}))


def get_requests_for_recipient(recipient_id: str) -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["donation_requests"].find({"recipient_id": recipient_id}).sort("created_at", DESCENDING))
    except Exception:
        return list(cols["donation_requests"].find({"recipient_id": recipient_id}))


def approve_request(request_id: str) -> tuple[bool, str]:
    from bson import ObjectId
    from utils import generate_pin
    cols = get_collections()
    try:
        oid = ObjectId(request_id)
    except Exception:
        oid = request_id
    req = cols["donation_requests"].find_one({"_id": oid})
    if not req or req["status"] != "pending":
        return False, "Request not found or not pending."
    pin = generate_pin()
    cols["donation_requests"].update_one(
        {"_id": oid},
        {"$set": {"status": "approved", "pickup_pin": pin, "approved_at": datetime.now(timezone.utc)}},
    )
    # Reduce available qty on listing
    try:
        lid = ObjectId(req["listing_id"])
    except Exception:
        lid = req["listing_id"]
    listing = cols["food_listings"].find_one({"_id": lid})
    if listing:
        new_qty = max(listing["remaining_qty_kg"] - req["requested_qty_kg"], 0)
        new_status = "reserved" if new_qty <= 0 else "available"
        cols["food_listings"].update_one(
            {"_id": lid},
            {"$set": {"remaining_qty_kg": new_qty, "status": new_status}},
        )
    return True, pin


def reject_request(request_id: str) -> bool:
    from bson import ObjectId
    cols = get_collections()
    try:
        oid = ObjectId(request_id)
    except Exception:
        oid = request_id
    cols["donation_requests"].update_one(
        {"_id": oid}, {"$set": {"status": "rejected"}}
    )
    return True


def verify_pickup_pin(request_id: str, entered_pin: str) -> tuple[bool, str]:
    """Verify PIN → complete pickup → write to donation_history → reward donor."""
    from bson import ObjectId
    from utils import co2e_avoided, meals_saved
    cols = get_collections()
    try:
        oid = ObjectId(request_id)
    except Exception:
        oid = request_id
    req = cols["donation_requests"].find_one({"_id": oid})
    if not req:
        return False, "Request not found."
    if req["status"] != "approved":
        return False, f"Request is not in approved state (current: {req['status']})."
    if str(req.get("pickup_pin", "")) != str(entered_pin).strip():
        return False, "Incorrect PIN. Please ask the NGO to recheck."

    now = datetime.now(timezone.utc)
    qty = req["requested_qty_kg"]

    # Mark request completed
    cols["donation_requests"].update_one(
        {"_id": oid}, {"$set": {"status": "completed", "completed_at": now}}
    )

    # Mark listing collected
    try:
        lid = ObjectId(req["listing_id"])
    except Exception:
        lid = req["listing_id"]
    listing = cols["food_listings"].find_one({"_id": lid})
    cols["food_listings"].update_one({"_id": lid}, {"$set": {"status": "collected"}})

    # Write donation_history
    cols["donation_history"].insert_one({
        "listing_id":      req["listing_id"],
        "request_id":      request_id,
        "donor_id":        req.get("donor_id", ""),
        "donor_name":      req.get("donor_name", ""),
        "recipient_id":    req.get("recipient_id", ""),
        "recipient_name":  req.get("recipient_name", ""),
        "food_category":   listing.get("category", "") if listing else "",
        "quantity_kg":     qty,
        "meals_saved":     meals_saved(qty),
        "co2e_avoided_kg": co2e_avoided(qty),
        "completed_at":    now,
    })

    # Reward donor +10 points
    try:
        d_oid = ObjectId(req["donor_id"])
    except Exception:
        d_oid = req["donor_id"]
    cols["users"].update_one({"_id": d_oid}, {"$inc": {"reward_points": 10}})

    return True, "Pickup verified and logged successfully!"


# ════════════════════════════════════════════════════════════════════════════
# ADMIN
# ════════════════════════════════════════════════════════════════════════════

def get_all_users() -> list:
    cols = get_collections()
    return list(cols["users"].find())


def toggle_user_verification(user_id: str, status: bool):
    from bson import ObjectId
    cols = get_collections()
    try:
        oid = ObjectId(user_id)
    except Exception:
        oid = user_id
    cols["users"].update_one({"_id": oid}, {"$set": {"is_verified": status}})


def get_all_listings() -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["food_listings"].find().sort("created_at", DESCENDING).limit(100))
    except Exception:
        return list(cols["food_listings"].find())


def get_all_requests() -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["donation_requests"].find().sort("created_at", DESCENDING).limit(100))
    except Exception:
        return list(cols["donation_requests"].find())


def get_all_history() -> list:
    cols = get_collections()
    try:
        from pymongo import DESCENDING
        return list(cols["donation_history"].find().sort("completed_at", DESCENDING).limit(500))
    except Exception:
        return list(cols["donation_history"].find())


# ════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ════════════════════════════════════════════════════════════════════════════

def get_platform_stats() -> dict:
    cols  = get_collections()
    now   = datetime.now(timezone.utc)
    hist  = list(cols["donation_history"].find())
    total_kg      = sum(h.get("quantity_kg", 0) for h in hist)
    total_meals   = sum(h.get("meals_saved", 0) for h in hist)
    total_co2     = sum(h.get("co2e_avoided_kg", 0) for h in hist)
    active        = cols["food_listings"].count_documents({"status": "available", "pickup_deadline": {"$gt": now}})
    pickups_done  = cols["donation_history"].count_documents({})
    pending_reqs  = cols["donation_requests"].count_documents({"status": "pending"})
    total_listed  = cols["food_listings"].count_documents({})
    return {
        "total_kg": total_kg,
        "total_meals": total_meals,
        "total_co2": total_co2,
        "active_listings": active,
        "completed_pickups": pickups_done,
        "pending_requests": pending_reqs,
        "total_listings": total_listed,
    }


def get_weekly_trend() -> list:
    """Returns list of {week, qty_kg} dicts for bar chart."""
    hist = get_all_history()
    buckets: dict = {}
    for h in hist:
        dt = h.get("completed_at")
        if not dt:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # ISO week label
        label = dt.strftime("%Y-W%W")
        buckets[label] = buckets.get(label, 0) + h.get("quantity_kg", 0)
    result = [{"week": k, "qty_kg": round(v, 1)} for k, v in sorted(buckets.items())]
    return result[-13:]   # last 13 weeks


def get_category_totals() -> list:
    hist = get_all_history()
    buckets: dict = {}
    for h in hist:
        cat = h.get("food_category", "Other")
        buckets[cat] = buckets.get(cat, 0) + h.get("quantity_kg", 0)
    return [{"category": k, "qty_kg": round(v, 1)} for k, v in sorted(buckets.items(), key=lambda x: -x[1])]


def get_request_status_counts() -> dict:
    cols = get_collections()
    statuses = ["pending", "approved", "completed", "rejected"]
    return {s: cols["donation_requests"].count_documents({"status": s}) for s in statuses}


def get_expiring_listings() -> list:
    cols = get_collections()
    now  = datetime.now(timezone.utc)
    future = now + timedelta(hours=24)
    q = {"status": "available", "pickup_deadline": {"$gt": now, "$lt": future}}
    try:
        from pymongo import ASCENDING
        return list(cols["food_listings"].find(q).sort("pickup_deadline", ASCENDING))
    except Exception:
        docs = list(cols["food_listings"].find(q))
        docs.sort(key=lambda d: d.get("pickup_deadline") or datetime.max.replace(tzinfo=timezone.utc))
        return docs
