import asyncio
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading

from livekit.agents import Agent, AgentServer, AgentSession, AutoSubscribe, JobContext, WorkerOptions, cli, llm
#from livekit.agents.pipeline import VoicePipelineAgent
#from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from app.agents.tools import TaskAssistantTools

from app.config import settings
from app.routes import auth_routes
from app.error_handler import CoreExceptionMiddleware

import warnings
# Suppress annoying Pydantic V2 namespace warnings caused by LiveKit
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task_agent")

app = FastAPI(title="Voice Task CRUD Agent API")
app.add_middleware(CoreExceptionMiddleware)
app.include_router(auth_routes.router) #auth api paths

# CORS for frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are an expert real-time AI voice assistant for task management.\n"
                "Keep responses short, conversational, and direct. Avoid repeating markdown syntax or punctuation.\n"
                "You have direct database tooling capability to create, view, update, and delete entries via tasks IDs.\n"
                "Before deleting any task, verify with the user vocally to confirm their permission."
            )
        )


server = AgentServer() #liveKit AgentServer instance

@server.rtc_session()   
async def entrypoint(ctx: JobContext):
   logger.info(f"New RTC session started in room: {ctx.room.name}")
   await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
   fnc_ctx = TaskAssistantTools()
   #assistant = VoiceAssistant(
   #assistant = VoicePipelineAgent(
   session = AgentSession(
       vad=silero.VAD.load(),
       stt=openai.STT(),  #open ai speech to text
       llm=openai.LLM(),  # open ai language model
       tts=openai.TTS(),  # open ai text to speech
      # chat_ctx=initial_ctx
      fnc_ctx = fnc_ctx,
    )
   
   await session.start(
       room=ctx.room,
       agent=Assistant(),
       )
   
   #assistant.start(ctx.room)

   await session.generate_reply(
       instructions="Say hello to the user and ask how you can help them today."
   )
   while ctx.room.is_connected:
    await asyncio.sleep(1)
   #await assistant.say("Hello, What can I do for you today?", allow_interruptions=True)

def start_fastapi():
    """Runs the FastAPI server cleanly inside a dedicated thread."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")  

if __name__ == "__main__":    # Run the entrypoint with the specified worker options
    api_thread = threading.Thread(target=start_fastapi, daemon=True)
    api_thread.start()
    logger.info("Starting up LiveKit Agent Worker Loop...")
    cli.run_app(server)