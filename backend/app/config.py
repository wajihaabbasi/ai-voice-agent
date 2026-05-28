import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Voice Task CRUD Agent API"
    DEBUG: bool = True
    
    # Database Configuration
    # Fallback default links directly to a local postgres instance
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/voice_crud"
    
    # LiveKit Credentials (Required for WebRTC voice streaming rooms)
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    LIVEKIT_URL: str = ""
    
    # AI Engine Provider Configurations
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        extra="ignore"
    )

settings = Settings()