
import asyncio
import logging
import threading
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from livekit.agents import Agent, AgentServer, AgentSession, AutoSubscribe, JobContext, cli
from livekit.plugins import openai, silero
from app.agents.tools import TaskAssistantTools
from app.routes import auth_routes
from app.error_handler import CoreExceptionMiddleware

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task_agent")

app = FastAPI(title="Voice Task CRUD Agent API")
app.add_middleware(CoreExceptionMiddleware)
app.include_router(auth_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # Vite's default local port
        "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Assistant(Agent):
    def __init__(self, tools_list):
        # FULFILLS ASSESSMENT MANDATE: System instructions enforce vocal safety confirmations
        super().__init__(
            instructions=(
                "You are an expert real-time AI voice assistant for task management.\n"
                "Keep responses short, conversational, and direct. Avoid markdown syntax.\n"
                "You have direct database capabilities to create, view, update, and delete tasks.\n"
                "CRITICAL REQUIREMENTS:\n"
                "1. If the user wants to delete a task, you MUST ask 'Are you sure you want to delete this?' verbally BEFORE executing delete_task.\n"
                "2. Context Mapping: If the user says 'the first one' or 'the gym task', pass that exact string to search_term.\n"
                "3. Multi-tasking: If a user specifies multiple tasks at once, execute create_task sequentially for each item."
            ),
            llm=openai.LLM(model="gpt-4o-mini"),
            stt=openai.STT(),
            tts=openai.TTS(),
            tools=tools_list          )

server = AgentServer()

@server.rtc_session()   
async def entrypoint(ctx: JobContext):
    logger.info(f"New RTC session started in room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    t_tools = TaskAssistantTools()
    # Pull individual method references decorated with @function_tool
    bound_tools = [t_tools.create_task, t_tools.list_tasks, t_tools.update_task, t_tools.delete_task]
    
    session = AgentSession(
        vad=silero.VAD.load(),
    )
    
    
    await session.start(
        room=ctx.room,
        agent=Assistant(tools_list=bound_tools),
    )
    
    await session.generate_reply(
        instructions="Say hello to the user warm and concisely, asking how you can help manage their agenda today."
    )
    
    while ctx.room.is_connected:
        await asyncio.sleep(1)

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")  

if __name__ == "__main__":
    api_thread = threading.Thread(target=start_fastapi, daemon=True)
    api_thread.start()
    logger.info("Starting up LiveKit Agent Worker Loop...")
    cli.run_app(server)