"""
FastAPI Backend for Autonomous Jarvis AI
Main server with all endpoints
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import os
import json
from dotenv import load_dotenv

load_dotenv()

from core.llm_engine import llm_engine
from core.agent import autonomous_agent
from core.memory import memory_manager
from core.rag import rag_system
from core.document_processor import process_document
from core.voice_local import speak, listen
from core.tools.web_search import get_current_time
from core.image_gen import image_gen
from core.video_gen import video_gen

app = FastAPI(
    title="Autonomous Jarvis AI",
    description="Autonomous AI system with local LLM and agent capabilities",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5174").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for audio files
os.makedirs("backend/data/audio", exist_ok=True)
app.mount("/audio", StaticFiles(directory="backend/data/audio"), name="audio")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Autonomous Jarvis AI Backend Operational",
        "version": "1.0.0",
        "features": [
            "Local LLM (Ollama)",
            "Autonomous Agent",
            "Web Search",
            "Code Execution",
            "RAG System",
            "Code Execution",
            "RAG System",
            "Voice Features",
            "Image Generation (Gemini 2.5)",
            "Video Generation (Veo)"
        ]
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm": "Ollama",
        "time": get_current_time()
    }

# ==================== Session Management ====================

@app.get("/sessions")
async def list_sessions():
    """List all conversation sessions"""
    return memory_manager.list_sessions()

@app.post("/sessions")
async def create_session(title: str = Form("New Chat")):
    """Create new conversation session"""
    session_id = memory_manager.create_session(title)
    return {"id": session_id}

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session by ID"""
    session = memory_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    success = memory_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

# ==================== Chat Endpoints ====================

@app.post("/chat")
async def chat(
    message: str = Form(...),
    session_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    mode: str = Form("normal"),  # normal, quiz, eli5, flashcard, coding
    use_agent: bool = Form(False)  # Use autonomous agent
):
    """
    Main chat endpoint
    
    Supports:
    - Text-only chat
    - Image upload and analysis
    - Document upload (PDF, DOCX)
    - Educational modes
    - Autonomous agent mode
    """
    # Create session if not provided
    if not session_id:
        session_id = memory_manager.create_session()
    
    # Process uploaded file if any
    file_content = None
    file_type = None
    
    if file:
        file_bytes = await file.read()
        filename = file.filename.lower()
        
        # Process document
        if filename.endswith(('.pdf', '.docx')):
            extracted_text = process_document(file_bytes, filename)
            if extracted_text:
                message = f"{message}\n\n[Document Content]:\n{extracted_text}"
                
                # Add to RAG system
                rag_system.add_document(
                    extracted_text,
                    metadata={"filename": file.filename, "session_id": session_id}
                )
        else:
            # Assume it's an image
            file_content = file_bytes
            file_type = "image"
    
    # Save user message
    memory_manager.add_message(session_id, "user", message)
    
    # Get conversation history
    history = memory_manager.get_conversation_history(session_id, max_messages=10)
    
    # Generate response based on mode
    if use_agent:
        # Use autonomous agent
        result = autonomous_agent.execute(message)
        response_text = result.get("output", "Agent execution failed")
    else:
        # Use direct LLM
        # Check if we need RAG context
        rag_context = rag_system.get_context_for_query(message, n_results=2)
        
        # Create system prompt based on mode
        if mode == "coding":
            system_prompt = llm_engine.create_coding_prompt(message)
        elif mode in ["quiz", "eli5", "flashcard", "tutor"]:
            system_prompt = llm_engine.create_educational_prompt(message, mode)
        else:
            # Normal mode with web search detection
            message_lower = message.lower()
            search_keywords = ['search', 'latest', 'news', 'weather', 'current', 'price']
            
            if any(kw in message_lower for kw in search_keywords):
                from core.tools.web_search import search_web
                search_results = search_web(message, max_results=3)
                system_prompt = f"""You are Jarvis, an advanced AI assistant.
                
Current time: {get_current_time()}

Web Search Results:
{search_results}

{rag_context}

Use the above information to answer the user's question accurately."""
            else:
                system_prompt = f"""You are Jarvis, an advanced AI assistant specializing in coding, education, and general knowledge.

Current time: {get_current_time()}

{rag_context}

Be helpful, concise, and accurate."""
        
        # Generate response
        response_text = llm_engine.generate_response(
            message,
            system_prompt=system_prompt,
            history=history[:-1],  # Exclude current message
            temperature=0.7
        )
    
    # Generate audio (TTS)
    audio_bytes = await speak(response_text, voice="female", rate="+0%")
    audio_path = f"backend/data/audio/response_{hash(response_text)}.mp3"
    with open(audio_path, 'wb') as f:
        f.write(audio_bytes)
    audio_url = f"/audio/response_{hash(response_text)}.mp3"
    
    # Save assistant response
    memory_manager.add_message(session_id, "assistant", response_text)
    
    return {
        "response": response_text,
        "session_id": session_id,
        "audio_url": audio_url
    }

# ==================== Media Generation ====================

@app.post("/generate-image")
async def generate_image_endpoint(
    prompt: str = Form(...),
    width: int = Form(1024),
    height: int = Form(1024),
    seed: int = Form(None),
    model: str = Form("gemini-2.5-flash-image"),
    enhance: bool = Form(True)
):
    """Generate image using Gemini 2.5 Flash Image"""
    image_url = image_gen.generate(prompt, width=width, height=height, seed=seed, model=model, enhance=enhance)
    return {"image_url": image_url}

@app.post("/generate-video")
async def generate_video_endpoint(
    prompt: str = Form(...),
    duration: int = Form(8),
    aspect_ratio: str = Form("16:9"),
    reference_image: Optional[UploadFile] = File(None)
):
    """Generate video using Google Veo"""
    ref_image_bytes = await reference_image.read() if reference_image else None
    result = video_gen.generate(prompt, duration=duration, aspect_ratio=aspect_ratio, reference_image=ref_image_bytes)
    return result

@app.get("/check-video-status/{operation_id}")
async def check_video_status(operation_id: str):
    """Check video generation status"""
    result = video_gen.check_status(operation_id)
    return result

# ==================== Agent Endpoints ====================

@app.post("/agent/execute")
async def execute_agent_task(
    task: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Execute autonomous agent task"""
    result = autonomous_agent.execute(task, context)
    return result

# ==================== Voice Endpoints ====================

@app.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    voice: str = Form("female"),
    rate: str = Form("+0%")
):
    """Text-to-speech endpoint"""
    audio_bytes = await speak(text, voice=voice, rate=rate)
    audio_path = f"backend/data/audio/tts_{hash(text)}.mp3"
    with open(audio_path, 'wb') as f:
        f.write(audio_bytes)
    return {"audio_url": f"/audio/tts_{hash(text)}.mp3"}

@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """Speech-to-text endpoint"""
    audio_bytes = await file.read()
    text = await listen(audio_bytes)
    return {"text": text}

# ==================== RAG Endpoints ====================

@app.post("/rag/add")
async def add_to_knowledge_base(
    text: str = Form(...),
    metadata: Optional[str] = Form(None)
):
    """Add document to RAG knowledge base"""
    meta_dict = json.loads(metadata) if metadata else {}
    doc_id = rag_system.add_document(text, metadata=meta_dict)
    return {"document_id": doc_id, "status": "added"}

@app.post("/rag/search")
async def search_knowledge_base(
    query: str = Form(...),
    n_results: int = Form(5)
):
    """Search RAG knowledge base"""
    results = rag_system.search(query, n_results=n_results)
    return {"results": results}

@app.get("/rag/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    return rag_system.get_stats()

# ==================== Document Upload ====================

@app.post("/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """Upload and process document (PDF, DOCX)"""
    file_bytes = await file.read()
    extracted_text = process_document(file_bytes, file.filename)
    
    if not extracted_text or extracted_text.startswith("Error"):
        raise HTTPException(status_code=400, detail=extracted_text or "Failed to process document")
    
    # Add to RAG
    doc_id = rag_system.add_document(
        extracted_text,
        metadata={
            "filename": file.filename,
            "session_id": session_id or "unknown"
        }
    )
    
    return {
        "status": "success",
        "filename": file.filename,
        "document_id": doc_id,
        "text_length": len(extracted_text)
    }

# ==================== Memory Search ====================

@app.post("/memory/search")
async def search_memory(query: str = Form(...)):
    """Search across all conversation history"""
    results = memory_manager.search_messages(query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", "8001"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
