# 📖 Detailed Setup Guide - Autonomous Jarvis AI

Complete step-by-step guide to install and run your autonomous AI system.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Install Ollama & AI Models](#step-1-install-ollama--ai-models)
3. [Step 2: Setup Backend](#step-2-setup-backend)
4. [Step 3: Setup Frontend](#step-3-setup-frontend)
5. [Step 4: Launch Application](#step-4-launch-application)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### System Requirements

**Minimum:**
- Windows 10/11 (64-bit)
- AMD Ryzen 5 or Intel Core i5 (6th gen+)
- 8GB RAM
- 20GB free disk space
- Internet connection (for initial setup)

**Recommended:**
- Windows 11
- AMD Ryzen 7 or Intel Core i7
- 16GB+ RAM
- 30GB+ free disk space
- SSD for better performance

### Software Requirements

**Required:**
1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

2. **Node.js 18.x or higher**
   - Download: https://nodejs.org/
   - LTS version recommended

3. **Git** (optional, for cloning)
   - Download: https://git-scm.com/download/win

### Verify Prerequisites

Open PowerShell or Command Prompt and run:

```powershell
# Check Python
python --version
# Should show: Python 3.10.x or higher

# Check pip
pip --version

# Check Node.js
node --version
# Should show: v18.x.x or higher

# Check npm
npm --version
```

If any command fails, install the missing software first.

---

## Step 1: Install Ollama & AI Models

### Option A: Automated Installation (Recommended)

1. **Open PowerShell as Administrator**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to project directory**
   ```powershell
   cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous
   ```

3. **Run installation script**
   ```powershell
   .\install_ollama.ps1
   ```

4. **What happens:**
   - Downloads Ollama installer (~100MB)
   - Installs Ollama service
   - Downloads Qwen2.5-Coder 14B model (~8.5GB)
   - This takes 10-20 minutes depending on internet speed

5. **Follow prompts:**
   - Ollama installer may require admin approval
   - Model download shows progress bar
   - Optional: Choose to download 7B model for faster testing

### Option B: Manual Installation

If the script fails, install manually:

1. **Download Ollama**
   - Visit: https://ollama.com/download
   - Download Windows installer
   - Run `OllamaSetup.exe`
   - Follow installation wizard

2. **Start Ollama service**
   ```powershell
   ollama serve
   ```
   - Leave this terminal open
   - You should see "Ollama is running"

3. **Open new terminal and pull model**
   ```powershell
   # Main model (8.5GB, ~10-15 min download)
   ollama pull qwen2.5-coder:14b-instruct-q4_K_M
   
   # Optional: Smaller, faster model (4GB)
   ollama pull qwen2.5-coder:7b-instruct
   ```

4. **Verify installation**
   ```powershell
   ollama list
   ```
   - Should show installed models

---

## Step 2: Setup Backend

### 2.1 Create Virtual Environment (Recommended)

```powershell
# Navigate to backend directory
cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Note: If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Your prompt should now show `(venv)` prefix.

### 2.2 Install Python Dependencies

```powershell
# Make sure you're in backend directory with venv activated
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Installing collected packages: fastapi, uvicorn, ollama, langchain...
Successfully installed 30+ packages
```

**Troubleshooting:**
- If `faster-whisper` fails: Install Microsoft C++ Build Tools
- If `chromadb` fails: Try `pip install chromadb --no-binary chromadb`

### 2.3 Configure Environment

```powershell
# Copy example env file
copy .env.example .env

# Edit .env if needed (optional)
notepad .env
```

**Default configuration** (in `.env`):
```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M
WHISPER_MODEL=base
BACKEND_PORT=8001
CORS_ORIGINS=http://localhost:5174
MAX_ITERATIONS=10
ENABLE_CODE_EXECUTION=true
```

**Adjust if needed:**
- Use `qwen2.5-coder:7b-instruct` for faster responses
- Change ports if already in use
- Disable code execution if not needed

---

## Step 3: Setup Frontend

### 3.1 Install Node Dependencies

```powershell
# Open new terminal (or deactivate venv)
cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous\frontend

# Install dependencies
npm install
```

**Expected output:**
```
added 500+ packages in 30s
```

**Troubleshooting:**
- If npm is slow: Try `npm install --no-audit`
- If errors occur: Delete `node_modules` and `package-lock.json`, then retry
- If still fails: Try `npm install --legacy-peer-deps`

### 3.2 Verify Installation

```powershell
# Check if all packages installed
npm list --depth=0
```

Should show:
- react
- axios
- lucide-react
- react-markdown
- framer-motion
- And others...

---

## Step 4: Launch Application

### Option A: Automated Startup (Easiest)

```powershell
# From root directory
cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous

# Run startup script
.\start_autonomous_jarvis.bat
```

**What happens:**
1. Checks if Ollama is running (starts if not)
2. Opens new window for backend
3. Waits 5 seconds
4. Opens new window for frontend
5. Both servers run in separate windows

**You'll see:**
- Backend window: "Uvicorn running on http://0.0.0.0:8001"
- Frontend window: "Local: http://localhost:5174"

### Option B: Manual Startup (More Control)

**Terminal 1 - Ollama:**
```powershell
ollama serve
```
Keep this running.

**Terminal 2 - Backend:**
```powershell
cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous\backend

# Activate venv if created
.\venv\Scripts\Activate.ps1

# Start backend
python main.py
```

**Terminal 3 - Frontend:**
```powershell
cd c:\Users\vishn\.gemini\antigravity\scratch\jarvis_autonomous\frontend

# Start dev server
npm run dev
```

**Wait for:**
- Backend: "Application startup complete"
- Frontend: "ready in Xms"

---

## Verification & Testing

### 1. Check Backend Health

Open browser and visit:
```
http://localhost:8001/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "llm": "Ollama",
  "time": "Tuesday, November 26, 2024 at 11:25 AM"
}
```

### 2. Check API Documentation

Visit:
```
http://localhost:8001/docs
```

You should see FastAPI's interactive API documentation (Swagger UI).

### 3. Open Frontend

Visit:
```
http://localhost:5174
```

**You should see:**
- Futuristic dark interface with neon blue accents
- "Jarvis AI" branding with animated effects
- "New Chat" button
- Four feature cards
- Animated background grid

### 4. Test Basic Chat

1. Click "New Chat" button
2. Type a message: "Hello, introduce yourself"
3. Press Enter
4. Wait for response (5-15 seconds for first message)

**Expected:**
- Your message appears on right (gradient background)
- Jarvis responds on left (glass effect with glow)
- Audio play button appears

### 5. Test Agent Mode

1. Click Settings ⚙️ icon (top right of sidebar)
2. Enable "Autonomous Agent" checkbox
3. Try: "Search the web for latest Python features and summarize"
4. Watch agent use tools

**Expected:**
- Agent status shows "Agent Active" (green dot)
- Response shows tool usage (WebSearch, etc.)
- Detailed answer with sources

### 6. Test File Upload

1. Find a PDF or DOCX file
2. Click file icon 📎 in chat
3. Select file
4. Ask: "What is this document about?"

**Expected:**
- File name shows above input
- Document processed and added to RAG
- Relevant answer about document content

### 7. Test Voice Output

1. Send any message
2. After response, click "Play Audio" button

**Expected:**
- Audio plays with synthesized voice
- Button changes to "Playing..."

---

## Troubleshooting

### Backend Issues

**Error: "Ollama connection failed"**
```powershell
# Solution 1: Check if Ollama is running
ollama list

# Solution 2: Restart Ollama
# Close ollama serve terminal and restart

# Solution 3: Check URL in .env
# Make sure OLLAMA_BASE_URL=http://localhost:11434
```

**Error: "Module not found"**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific missing module
pip install <module-name>
```

**Error: Port 8001 already in use**
```powershell
# Change port in backend/.env
BACKEND_PORT=8002

# Also update frontend/vite.config.ts proxy target
```

**Slow responses**
```bash
# Switch to faster model in .env
OLLAMA_MODEL=qwen2.5-coder:7b-instruct

# Restart backend
```

### Frontend Issues

**Error: "Cannot GET /"**
```powershell
# Make sure you're accessing correct URL
# Frontend: http://localhost:5174
# Backend: http://localhost:8001

# Check terminal for actual port number
```

**Error: "Network Error" when sending message**
```powershell
# 1. Check backend is running
# 2. Check CORS settings in backend/.env
# 3. Try clearing browser cache
```

**TypeScript/ESLint errors in editor**
- These are normal before `npm install`
- Restart VS Code after npm install
- Or run: `npm run build` to verify

**Blank screen / not loading**
```powershell
# Clear Vite cache
rm -rf frontend/node_modules/.vite

# Restart dev server
npm run dev
```

### Model Issues

**Error: "Model not found"**
```powershell
# Pull model again
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# Verify model name matches .env exactly
```

**Out of memory errors**
```bash
# Use smaller model
OLLAMA_MODEL=qwen2.5-coder:7b-instruct

# Close other applications
# Restart computer to free RAM
```

---

## Advanced Configuration

### Using Different Models

**Available models:**
```bash
# Coding-optimized (recommended)
qwen2.5-coder:14b-instruct-q4_K_M  # 8.5GB, balanced
qwen2.5-coder:7b-instruct          # 4GB, faster

# General purpose
llama3.2:latest                     # 2.6GB, very fast
llama3.1:8b                        # 5GB, good balance

# Larger models (if you have >24GB RAM)
qwen2.5:32b                        # 19GB, best quality
```

**To switch:**
1. Pull new model: `ollama pull <model-name>`
2. Update `backend/.env`: `OLLAMA_MODEL=<model-name>`
3. Restart backend

### Frontend Customization

**Change colors** - Edit `frontend/src/index.css`:
```css
:root {
  --neon-blue: #00f0ff;    /* Change to your color */
  --neon-purple: #b24bf3;
  --neon-pink: #ff006e;
}
```

**Change fonts** - Edit `frontend/tailwind.config.js`:
```js
fontFamily: {
  cyber: ['Orbitron', 'sans-serif'],  // Change font
}
```

### Performance Tuning

**For faster responses:**
```bash
# .env changes
OLLAMA_MODEL=qwen2.5-coder:7b-instruct
MAX_ITERATIONS=5  # Reduce agent iterations
```

**For better quality:**
```bash
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M
MAX_ITERATIONS=15  # Allow more agent thinking
```

### Running on Different Ports

**Backend:**
```bash
# In backend/.env
BACKEND_PORT=8080
```

**Frontend:**
```js
// In frontend/vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8080',  // Match backend port
    }
  }
}
```

---

## Next Steps

1. ✅ **Explore Features**
   - Try different AI modes (coding, quiz, eli5)
   - Upload and query documents
   - Test agent with complex tasks

2. ✅ **Customize**
   - Adjust colors and themes
   - Add custom prompts
   - Configure models

3. ✅ **Share**
   - Show friends your autonomous AI
   - Deploy to cloud (see deployment guide)
   - Contribute improvements on GitHub

4. ✅ **Learn More**
   - Read [walkthrough.md](walkthrough.md) for architecture
   - Check [README.md](README.md) for features
   - See [UI_ENHANCEMENTS.md](UI_ENHANCEMENTS.md) for design details

---

## Support & Resources

**Issues?**
- Check [Troubleshooting](#troubleshooting) section above
- Review backend logs in terminal
- Check browser console (F12) for frontend errors

**Documentation:**
- Ollama: https://ollama.com/docs
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev

**Community:**
- Create GitHub Issues for bugs
- Share screenshots and feedback
- Contribute improvements

---

## Summary Commands

**Quick start (after first-time setup):**
```powershell
# From project root
.\start_autonomous_jarvis.bat

# Then open: http://localhost:5174
```

**Stop servers:**
- Close terminal windows
- Or press `Ctrl+C` in each terminal

**Update models:**
```powershell
ollama pull qwen2.5-coder:14b-instruct-q4_K_M
```

**Reinstall dependencies:**
```powershell
# Backend
cd backend
pip install -r requirements.txt --force-reinstall

# Frontend
cd frontend
rm -rf node_modules
npm install
```

---

**🎉 You're all set! Enjoy your autonomous AI assistant!**

For questions or issues, refer to the troubleshooting section or check the main documentation files.
