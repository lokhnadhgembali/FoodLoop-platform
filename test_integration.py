import os, sys
from dotenv import load_dotenv
load_dotenv('e:/FoodLoop/.env')

print("=== FoodLoop Full Integration Test ===\n")

# 1. MongoDB
from pymongo import MongoClient
uri = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')
client = MongoClient(uri, serverSelectionTimeoutMS=8000)
client.admin.command('ping')
db = client[db_name]
print("[OK] MongoDB: connected to", db_name)
print("     Collections:", db.list_collection_names())

# 2. Database helpers
sys.path.insert(0, 'e:/FoodLoop')
import database as dbmod
lid = dbmod.add_listing('TestDonor','Paneer Rolls','Cooked Meals',10,'pieces','Jalandhar',4,'Test')
print("[OK] add_listing:", lid)
listings = dbmod.get_available_listings()
print("[OK] get_available_listings:", len(listings), "found")
rid = dbmod.request_food(lid, 'TestNGO', 2, 'pieces')
print("[OK] request_food:", rid)
pin = dbmod.approve_request(rid)
print("[OK] approve_request: PIN =", pin)
ok = dbmod.verify_and_complete_pickup(rid, pin)
print("[OK] verify_and_complete_pickup:", ok)
stats = dbmod.get_platform_analytics()
print("[OK] analytics: listed =", stats["total_listed"], "| collected =", stats["total_collected"])

# cleanup
from bson import ObjectId
db['food_listings'].delete_one({'_id': ObjectId(lid)})
db['donation_requests'].delete_one({'_id': ObjectId(rid)})
db['donation_history'].delete_one({'request_id': ObjectId(rid)})
print("[OK] Test data cleaned up")

# 3. Gemini
from google import genai
gc = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
resp = gc.models.generate_content(model='gemini-3.5-flash', contents='Give 1 food safety tip in 1 sentence.')
print("[OK] Gemini AI:", resp.text.strip()[:100])

print("\n=== ALL SYSTEMS GO ===")
print("Run: streamlit run e:/FoodLoop/app.py")

