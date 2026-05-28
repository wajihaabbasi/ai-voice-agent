import { useState } from 'react';
import { 
  LiveKitRoom, 
  RoomAudioRenderer, 
  VoiceAssistantControlBar,
  useVoiceAssistant
} from '@livekit/components-react';



//@ts-ignore
import '@livekit/components-styles'; // Imports native layout aesthetics flawlessly

const BACKEND_URL = "http://localhost:8005"; // Points to your running FastAPI server


export default function App() {
  console.log("Vite Env Object:", import.meta.env); // Debugging line to inspect environment variables
  const [token, setToken] = useState<string | null>(null);
  const [roomName, setRoomName] = useState<string>(""); 
  const [livekitUrl, setLivekitUrl] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const startSession = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/token`, { method: "POST" });
      if (!response.ok) throw new Error("Backend authentication failed.");
      
      const data = await response.json();
      setToken(data.token);
      setRoomName(data.room);
      setLivekitUrl(data.server_url);
    } catch (error) {
      console.error("Connection error:", error);
      setErrorMessage("Could not contact FastAPI server. Ensure it is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-slate-950 text-white font-sans antialiased overflow-hidden p-6 selection:bg-cyan-500/30">
      
      {/* Background Glowing Ambient Orbs */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-tr from-cyan-500/10 to-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 left-1/3 w-[300px] h-[300px] bg-purple-500/5 rounded-full blur-[100px] pointer-events-none" />

      {/* Header Panel */}
      <header className="text-center z-10 mb-10 max-w-sm">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/80 border border-slate-800 backdrop-blur-md mb-4">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <span className="text-xs font-medium tracking-wide text-slate-400">v1.0 Real-Time Engine</span>
        </div>
        <h1 className="text-4xl font-black tracking-tight bg-gradient-to-b from-white via-slate-200 to-slate-500 bg-clip-text text-transparent">
          Voice Workspace 
          </h1>
        <h5 className="text-sm text-slate-500 mt-2 uppercase tracking-wide">  
           built for UrbanGround technical test
        </h5>
        <p className="text-slate-400 mt-2 text-xs leading-relaxed">
          Connect & press the mic icon to speak naturally and manage tasks.
        </p>
      </header>

      {/* Main Control Card Frame */}
      <main className="w-full max-w-md z-10">
        {!token ? (
          <div className="bg-slate-900/40 border border-slate-800/60 backdrop-blur-xl p-8 rounded-3xl shadow-2xl flex flex-col items-center text-center">
            <div className="w-16 h-16 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-center mb-6 shadow-inner">
              <svg className="w-6 h-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            
            <h3 className="text-lg font-semibold mb-2">Ready to Initialize</h3>
            <p className="text-sm text-slate-500 mb-8 max-w-xs">
              Press the bridge link below to grant temporary mic permissions and pipe audio stream data.
            </p>

            {errorMessage && (
              <div className="w-full mb-6 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-xs text-red-400 font-medium">
                {errorMessage}
              </div>
            )}

            <button
              onClick={startSession}
              disabled={loading}
              className="w-full py-4 bg-white text-slate-950 font-semibold rounded-2xl shadow-xl shadow-white/5 hover:bg-slate-100 transition-all active:scale-[0.98] disabled:opacity-40 tracking-tight"
            >
              {loading ? "Establishing Bridge..." : "Connect Workspace Voice Agent"}
            </button>
          </div>
        ) : (
          <div className="bg-slate-900/60 border border-slate-800/80 backdrop-blur-2xl p-8 rounded-3xl flex flex-col items-center shadow-2xl relative">
            
            {/* Dynamic Active Room Info Badge — FIXES the roomName warning */}
            <div className="absolute top-4 right-4 text-[10px] uppercase font-mono tracking-widest text-slate-500 bg-slate-950/50 px-2 py-1 rounded border border-slate-800/50">
              Channel: {roomName}
            </div>

            <LiveKitRoom
              token={token}
              serverUrl={livekitUrl}
              audio={true}
              video={false}
              connect={true}
              onDisconnected={() => {
                setToken(null);
                setErrorMessage("Session closed or disconnected from LiveKit server.");
              }}
              className="flex flex-col items-center w-full gap-6 mt-4"
            >
              {/* Animated Vocal State Module */}
              <StatusIndicator />

              {/* Underlying Browser Node Stream Router */}
              <RoomAudioRenderer />

              {/* Cleaned Native LiveKit Voice Control Bar */}
              <div className="w-full mt-2 custom-lk-bar">
                <VoiceAssistantControlBar controls={{ leave: true }} />
              </div>
            </LiveKitRoom>
          </div>
        )}
      </main>

      <footer className="mt-16 text-[11px] font-medium tracking-wide text-slate-600 uppercase z-10">
        YOUR VOICE AI ASSISTANT - VERSION 1.0 - BUILT WITH FASTAPI, LIVEKIT, AND REACT
      </footer>
    </div>
  );
}

function StatusIndicator() {
  // FIXED: Removed unused audioTrack variable to resolve compiler warning
  const { state } = useVoiceAssistant();
  
  return (
    <div className="flex flex-col items-center gap-5 py-4 w-full">
      <div className="relative flex items-center justify-center w-32 h-32">
        
        {/* Animated Radial Pulse Ring Layer */}
        {state === 'speaking' && (
          <div className="absolute inset-0 rounded-full bg-purple-500/20 animate-ping opacity-75 duration-1000" />
        )}
        {state === 'listening' && (
          <div className="absolute inset-0 rounded-full bg-cyan-500/20 animate-pulse duration-700" />
        )}

        {/* Core Bubble Center Container */}
        <div className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-500 border backdrop-blur-md shadow-2xl ${
          state === 'speaking' 
            ? 'bg-purple-500/10 border-purple-400 shadow-purple-500/20 scale-105' 
            : state === 'listening' 
            ? 'bg-cyan-500/10 border-cyan-400 shadow-cyan-500/20 scale-105' 
            : state === 'connecting'
            ? 'bg-amber-500/10 border-amber-400 animate-pulse'
            : 'bg-slate-950/40 border-slate-800 shadow-black/40'
        }`}>
          <svg className={`w-8 h-8 transition-transform duration-300 ${state === 'speaking' || state === 'listening' ? 'scale-110' : ''} ${
            state === 'speaking' ? 'text-purple-400' : state === 'listening' ? 'text-cyan-400' : 'text-slate-400'
          }`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </div>
      </div>

      {/* Plain Text Verbal Flow Status Display */}
      <p className="text-xs font-bold uppercase tracking-widest min-h-[16px] text-slate-400">
        {state === 'speaking' && <span className="text-purple-400">Agent responding</span>}
        {state === 'listening' && <span className="text-cyan-400 animate-pulse">Listening...</span>}
        {state === 'connecting' && <span className="text-amber-400">Syncing pipeline</span>}
        {state === 'idle' && <span className="text-slate-500">Connected & Idle</span>}
      </p>
    </div>
  );
}