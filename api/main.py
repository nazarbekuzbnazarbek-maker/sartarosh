from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = "https://mxxorrauzwberjzllxhj.supabase.co"
SUPABASE_KEY = "sb_publishable_ZB1fTkEf6Jf4E5U9OTtVBw_ttATFD6R"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

class DBData(BaseModel):
    data: dict

@app.get("/api/db")
def get_db():
    url = f"{SUPABASE_URL}/rest/v1/app_data?id=eq.1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.json():
        return response.json()[0]["data"]
    raise HTTPException(status_code=404, detail="Ma'lumot topilmadi")

@app.post("/api/db")
def save_db(payload: DBData):
    url = f"{SUPABASE_URL}/rest/v1/app_data?id=eq.1"
    response = requests.patch(url, headers=HEADERS, json={"data": payload.data})
    if response.status_code in [200, 204]:
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Saqlashda xatolik yuz berdi")