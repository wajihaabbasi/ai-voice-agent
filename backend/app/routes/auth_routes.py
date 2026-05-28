import uuid
import os
from fastapi import APIRouter, HTTPException, Query
from livekit import api
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth Pipeline"])

@router.post("/token")
async def generate_webrtc_token(
    room_name: str = Query(default="voice_crud_workspace", description="The livekit room to join")
):

    #DEbugging
    print(f"--- DEBUGGING KEYS ---")
    print(f"KEY: {settings.LIVEKIT_API_KEY}")
    print(f"SECRET: {settings.LIVEKIT_API_SECRET}")
    print(f"----------------------")

    if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LiveKit server credentials are not set.")
    """Generates an encrypted JWT access token for WebRTC connection authentication."""
    if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LiveKit server credentials are not set.")

    identity = f"voice_user_{uuid.uuid4().hex[:6]}"
    room_name = room_name

    token = api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET) \
        .with_identity(identity) \
        .with_name("Web Client") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True
        ))

    return {
        "token": token.to_jwt(),
        "room": room_name,
        "identity": identity,
        "server_url": os.getenv("LIVEKIT_URL") or settings.LIVEKIT_KEY
        }


