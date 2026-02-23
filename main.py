from fastapi import FastAPI
import aiohttp
import json
import base64
from datetime import datetime

app = FastAPI()

API_URL = "https://semyjwtgen.vercel.app/token?uid={uid}&password={password}"

def decode_jwt(token):
    try:
        payload = token.split('.')[1]
        payload += "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except:
        return None


@app.get("/")
async def home(uid: str, password: str):

    # External API call
    url = API_URL.format(uid=uid, password=password)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    token = data.get("token")

    if not token:
        return {
            "developer": "SEMY",
            "error": "Token not found",
            "raw": data
        }

    decoded = decode_jwt(token)
    if not decoded:
        return {
            "developer": "SEMY",
            "error": "JWT decode failed"
        }

    return {
        "developer": "SEMY",
        "account_id": decoded.get("account_id"),
        "region": decoded.get("lock_region") or decoded.get("noti_region"),
        "external_uid": decoded.get("external_uid")
    }
