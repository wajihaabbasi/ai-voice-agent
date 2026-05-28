# Real-Time Voice Task Assistant 

An advanced WebRTC-powered voice assistant capable of executing CRUD schedule tasks using natural spoken language. Built with a unified Python event loop + background FastAPI multi-threaded daemon architecture and a reactive TypeScript client interface.

## 🏗️ Architectural Overview
Unlike traditional setups that decouple configurations, this project leverages a **Backend-Driven Configuration Handshake**. The frontend uses a dynamic handshake mechanism—querying the FastAPI endpoint for both its ephemeral WebRTC connection token and its target server configuration. This ensures zero frontend setup variables are needed for local execution or deployments.

- **Backend:** FastAPI, LiveKit Agents SDK, OpenAI Whisper (STT), GPT-4o-Mini (LLM), and OpenAI TTS.
- **Frontend:** React, TypeScript, Tailwind CSS, LiveKit Components.

---
