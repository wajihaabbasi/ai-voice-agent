# Real-Time Voice Task Assistant 

An advanced WebRTC-powered voice assistant capable of executing CRUD schedule tasks using natural spoken language. Built with a unified Python event loop + background FastAPI multi-threaded daemon architecture and a reactive TypeScript client interface.

## 🏗️ Architectural Overview
Unlike traditional setups that decouple configurations, this project leverages a **Backend-Driven Configuration Handshake**. The frontend uses a dynamic handshake mechanism—querying the FastAPI endpoint for both its ephemeral WebRTC connection token and its target server configuration. This ensures zero frontend setup variables are needed for local execution or deployments.

- **Backend:** FastAPI, LiveKit Agents SDK, OpenAI Whisper (STT), GPT-4o-Mini (LLM), and OpenAI TTS.
- **Frontend:** React, TypeScript, Tailwind CSS, LiveKit Components.

---

## Quick Start Setup
### 1. Prerequisites

Ensure you have the following installed before starting:
* Python 3.10+
* Node.js
* [OpenAI API Key](https://platform.openai.com/)
* [LiveKit](https://livekit.io/) credentials (URL, API Key, API Secret)

### 2. Backend Initialization
Navigate to the backend directory, set up your virtual environment, and install dependencies:

```bash
cd backend
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Create a .env file inside the backend/ directory:
```

LIVEKIT_URL=wss://your-sandbox-url.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
OPENAI_API_KEY=your-openai-key
```

### 4. Start the dual FastAPI + LiveKit Worker system:
```bash

python main.py dev
```

### 4. Frontend Initialization

In a separate terminal window, set up the dashboard:
```bash

cd voice-task-frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser to view the control dashboard and initiate the connection.
