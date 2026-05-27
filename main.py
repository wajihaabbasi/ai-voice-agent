import asyncio
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, AutoSubscribe, JobContext, WorkerOptions, cli, llm
#from livekit.agents.pipeline import VoicePipelineAgent
#from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a voice assistant created by LiveKit. Your interface with users will be voice."
                "You should use short and consise responses and avoid usage of unpronouncable puntutation."
            )
        )



# Initialize the voice assistant 
#initial_ctx = llm.ChatContext().append(
#      role="system",
#      text=(
#            "You are a voice assistant created by LiveKit. Your interface with users will be voice."
#            "You should use short and consise responses and avoid usage of unpronouncable puntutation."
#            ),
#   )
   
async def entrypoint(ctx: JobContext):
   await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
   
   #assistant = VoiceAssistant(
   #assistant = VoicePipelineAgent(
   session = AgentSession(
       vad=silero.VAD.load(),
       stt=openai.STT(),  #open ai speech to text
       llm=openai.LLM(),  # open ai language model
       tts=openai.TTS(),  # open ai text to speech
      # chat_ctx=initial_ctx
    )
   
   await session.start(
       room=ctx.room,
       agent=Assistant(),
       )
   
   #assistant.start(ctx.room)

   await session.generate_reply(
       instructions="Say hello to the user and ask how you can help them today."
   )

   await asyncio.sleep(1)
   #await assistant.say("Hello, What can I do for you today?", allow_interruptions=True)

  

if __name__ == "__main__":    # Run the entrypoint with the specified worker options
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))    