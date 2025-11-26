# 🤖 Autonomous Jarvis AI

**A fully autonomous AI assistant powered by local LLMs, designed to replace cloud-based APIs like Gemini and ChatGPT.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

---

## ✨ Features

### 🧠 **Core Capabilities**
- 🤖 **Local LLM**: Runs Qwen2.5-Coder (14B) via Ollama - no cloud dependencies
- 🎯 **Autonomous Agent**: LangChain-powered agent with tool use and multi-step reasoning
- 🌐 **Internet Access**: Real-time web search using DuckDuckGo
- 💻 **Code Execution**: Safe Python sandbox for running code
- 📚 **RAG System**: Vector database (ChromaDB) for document retrieval
- 🗣️ **Voice I/O**: Local text-to-speech and speech-to-text

### 🛠️ **Agent Tools**
- Web search & news search
- Web page scraping
- Mathematical calculator
- Code execution (Python)
- File system operations (sandboxed)
- Current time/date

### 🎓 **Educational Modes**
- **Quiz Mode**: Generate practice questions
- **ELI5 Mode**: Explain like I'm 5
- **Flashcard Mode**: Create study flashcards
- **Coding Mode**: Optimized for programming tasks
- **Tutor Mode**: Socratic teaching method

### 🎨 **Modern UI**
- Dark theme with glassmorphism
- Real-time chat interface
- Session management
- File upload (PDF, DOCX, images)
- Markdown rendering with syntax highlighting
- Voice playback

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11**
- **Python 3.10+**
- **Node.js 18+**
- **16GB RAM** (minimum)
- **20GB free disk space** (for models)

### Installation

**1. Install Ollama and Models**
```powershell
# Run the installation script
.\install_ollama.ps1
```

This will:
- Download and install Ollama
- Pull Qwen2.5-Coder 14B model (~9GB)
- Optionally download smaller 7B model

**2. Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**3. Install Frontend Dependencies**
```bash
cd frontend
npm install
```

### Running the Application

**Option 1: Automated Startup (Recommended)**
```batch
start_autonomous_jarvis.bat
```

**Option 2: Manual Startup**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Backend
cd backend
python main.py

# Terminal 3: Start Frontend
cd frontend
npm run dev
```

**Access the App**
- Frontend: http://localhost:5174
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

---

## 📖 Usage Guide

### Basic Chat
1. Type your message in the input box
2. Press Enter to send
3. View AI response with optional audio playback

### Autonomous Agent Mode
1. Click **Settings** icon
2. Enable "Use Autonomous Agent"
3. Agent will use tools to complete complex tasks

**Example Agent Tasks:**
```
"Search the web for latest Python features and create a summary"
"Calculate the ROI of investing $10,000 at 7% for 20 years"
"Write a Python function to sort a list and execute it with [3,1,4,1,5]"
```

### Educational Features
Set mode in Settings panel:
- **Quiz**: "Create a quiz about Python classes"
- **ELI5**: "Explain machine learning like I'm 5"
- **Flashcards**: "Generate flashcards for React hooks"
- **Coding**: "Write a binary search algorithm"

### Document Upload
1. Click file icon 📎
2. Upload PDF or DOCX
3. Content is extracted and added to RAG system
4. Ask questions about the document

---

## 🏗️ Architecture

```
jarvis_autonomous/
├── backend/
│   ├── core/
│   │   ├── llm_engine.py        # Ollama LLM integration
│   │   ├── agent.py              # LangChain autonomous agent
│   │   ├── memory.py             # Session management
│   │   ├── rag.py                # Vector database
│   │   ├── voice_local.py        # TTS/STT
│   │   ├── document_processor.py
│   │   └── tools/
│   │       ├── web_search.py
│   │       ├── calculator.py
│   │       ├── code_executor.py
│   │       └── file_manager.py
│   ├── main.py                   # FastAPI server
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.tsx
│   │   ├── App.tsx
│   │   └── index.css
│   └── package.json
├── install_ollama.ps1
└── start_autonomous_jarvis.bat
```

---

## 🔧 Configuration

### Environment Variables
Edit `backend/.env`:

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M

# Voice
WHISPER_MODEL=base
PIPER_VOICE=en_US-lessac-medium

# Agent
MAX_ITERATIONS=10
ENABLE_CODE_EXECUTION=true

# Server
BACKEND_PORT=8001
CORS_ORIGINS=http://localhost:5174
```

### Model Selection
Switch models in `.env`:
```bash
# Smaller, faster model
OLLAMA_MODEL=qwen2.5-coder:7b-instruct

# Or use Llama
OLLAMA_MODEL=llama3.2:latest
```

---

## 📊 Performance

**Hardware**: AMD Ryzen 7 7730U, 16GB RAM, Integrated Graphics

| Metric | Performance |
|--------|-------------|
| Inference Speed | 8-12 tokens/sec |
| First Token Latency | 1-2 seconds |
| RAM Usage | 10-12 GB |
| Model Size | ~9 GB (14B model) |
| TTS Generation | <500ms |
| STT Processing | <2 sec (10s audio) |

---

## 🛤️ Roadmap

- [ ] Add Piper TTS (currently using edge-tts)
- [ ] Implement multi-agent collaboration
- [ ] Add more tools (email, calendar, etc.)
- [ ] Mobile app (React Native)
- [ ] Voice activation ("Hey Jarvis")
- [ ] Local image generation (Stable Diffusion)
- [ ] Plugin system for custom tools

---

## 💰 Monetization Options

This project is open-source (MIT), but here are monetization paths:

1. **SaaS Hosted Version**: Offer cloud hosting
2. **Premium Features**: Advanced models, team features
3. **Consulting**: Help businesses deploy
4. **Training**: Workshops and courses
5. **Support Plans**: Enterprise support contracts

See [MONETIZATION.md](./MONETIZATION.md) for details.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md)

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit PRs
- 📚 Improve documentation
- 🌟 Star the repo!

---

## 📜 License

MIT License - see [LICENSE](./LICENSE)

**TL;DR**: Free to use, modify, distribute, and commercialize. Just keep the copyright notice.

---

## 🙏 Acknowledgments

- **Ollama**: Local LLM runtime
- **Qwen Team**: Excellent coding models
- **LangChain**: Agent framework
- **FastAPI**: Modern Python backend
- **React**: Beautiful frontend

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/jarvis-autonomous/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jarvis-autonomous/discussions)
- **Email**: your.email@example.com

---

## ⚠️ Disclaimer

This is an educational project. Code execution and web access features should be used responsibly. Always review generated code before executing.

---

<div align="center">

**Built with ❤️ for the open-source community**

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/jarvis-autonomous?style=social)](https://github.com/yourusername/jarvis-autonomous)

</div>
