# 🚀 Quick Start Guide - Autonomous Jarvis AI

## ⏱️ 15-Minute Setup

### Step 1: Install Ollama & Models (10 minutes)
```powershell
.\install_ollama.ps1
```
This will download ~9GB. Grab a coffee! ☕

### Step 2: Install Python Dependencies (2 minutes)
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies (2 minutes)
```bash
cd frontend
npm install
```

### Step 4: Launch! (1 minute)
```batch
start_autonomous_jarvis.bat
```

**That's it!** Open http://localhost:5174

---

## 📱 First Time Using

1. **Create a new chat** - Click "New Chat" button
2. **Try normal chat** - "Explain how neural networks work"
3. **Try agent mode** - Enable in Settings, then "Search web for latest AI news"
4. **Upload a document** - Click 📎, upload PDF, ask questions about it
5. **Try coding mode** - Switch mode, ask "Write a binary search function"

---

## 🎯 Example Prompts

**Normal Chat:**
- "Explain quantum computing simply"
- "What are the best practices for React?"

**Agent Mode (Enable in Settings):**
- "Search for Python 3.13 new features and summarize"
- "Calculate compound interest on $5000 at 6% for 15 years"
- "Write and execute code to find prime numbers under 100"

**Quiz Mode:**
- "Create a quiz about JavaScript closures"
- "Test me on Python data structures"

**Coding Mode:**
- "Write a merge sort algorithm with comments"
- "Debug this code: [paste code]"
- "Explain this function: [paste code]"

---

## ❓ Troubleshooting

**"Ollama connection failed"**
- Make sure Ollama is running: `ollama serve`
- Check if model is installed: `ollama list`

**"Backend not responding"**
- Ensure backend is running on port 8001
- Check `backend/.env` configuration

**"Frontend won't load"**
- Check if running on port 5174
- Try `npm run dev` again

**"Slow responses"**
- Normal on first query (model loading)
- For faster responses, use 7B model:
  ```bash
  # In backend/.env
  OLLAMA_MODEL=qwen2.5-coder:7b-instruct
  ```

---

## 🎛️ Quick Configuration

### Change Model
Edit `backend/.env`:
```bash
# Smaller, faster
OLLAMA_MODEL=qwen2.5-coder:7b-instruct

# Default, balanced
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M
```

### Change Ports
`backend/.env`:
```bash
BACKEND_PORT=8080
```

`frontend/vite.config.ts`:
```typescript
server: { port: 3000 }
```

---

## 📚 Learn More

- Full Documentation: [README.md](README.md)
- Architecture Details: [Walkthrough](walkthrough.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Enjoy your autonomous AI assistant!** 🎉
