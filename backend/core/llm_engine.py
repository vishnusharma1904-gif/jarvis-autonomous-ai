"""
Hybrid LLM Engine
Routes queries between Local Qwen 2.5 (Low Latency) and Google Gemini (Complex Reasoning)
"""

import os
import time
import re
from typing import List, Dict, Optional, Generator
import ollama
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class HybridLLMEngine:
    def __init__(self):
        # Local Setup (Qwen 2.5)
        self.local_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.local_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
        self.ollama_client = ollama.Client(host=self.local_base_url)
        
        # Cloud Setup (Gemini)
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = None
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        self.last_call_time = 0
        self.min_delay = 0.5
        
        # Verify Local Setup
        self._verify_local_setup()
    
    def _verify_local_setup(self):
        """Verify Ollama connection"""
        try:
            self.ollama_client.list()
            print(f"✅ Local LLM connected: {self.local_model}")
        except Exception as e:
            print(f"❌ Local LLM connection failed: {e}")

    def _is_complex_query(self, message: str) -> bool:
        """
        Determine if a query requires complex reasoning (Gemini) or is simple (Local).
        Heuristics:
        - Length > 300 chars
        - Keywords: plan, strategy, analyze, compare, reason, design, architecture
        - Multi-step instructions
        """
        if len(message) > 300:
            return True
        
        complex_keywords = [
            "plan", "strategy", "analyze", "compare", "reason", 
            "design", "architecture", "evaluate", "critique", 
            "complex", "step by step", "explain in detail"
        ]
        
        message_lower = message.lower()
        if any(kw in message_lower for kw in complex_keywords):
            return True
            
        return False

    def generate_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
        force_local: bool = False
    ) -> str | Generator:
        """
        Generate response using Hybrid Routing
        """
        # Rate limiting
        time_since_last = time.time() - self.last_call_time
        if time_since_last < self.min_delay:
            time.sleep(self.min_delay - time_since_last)
        
        # Routing Logic
        use_gemini = False
        if not force_local and self.gemini_model and self._is_complex_query(message):
            use_gemini = True
            print(f"🧠 Routing to Gemini (Complex Query)")
        else:
            print(f"⚡ Routing to Local Qwen (Low Latency)")

        try:
            if use_gemini:
                return self._generate_gemini(message, system_prompt, history, temperature, stream)
            else:
                return self._generate_local(message, system_prompt, history, temperature, max_tokens, stream)
        
        except Exception as e:
            print(f"❌ Primary model failed: {e}")
            # Fallback logic
            if use_gemini:
                print("⚠️ Falling back to Local Qwen...")
                return self._generate_local(message, system_prompt, history, temperature, max_tokens, stream)
            else:
                return "I apologize, but I'm having trouble processing your request locally."
        
        finally:
            self.last_call_time = time.time()

    def _generate_gemini(self, message: str, system_prompt: str, history: List[Dict], temperature: float, stream: bool):
        """Generate using Gemini API"""
        # Convert history to Gemini format
        chat_history = []
        if history:
            for msg in history:
                role = "user" if msg['role'] == 'user' else "model"
                chat_history.append({"role": role, "parts": [msg['content']]})
        
        # Add system prompt to the first message or configure it if supported (Gemini 1.5 supports system instructions)
        # For simplicity, we'll prepend it to the history or current message if needed, 
        # but Gemini 1.5 Pro/Flash supports system_instruction in GenerativeModel constructor.
        # Here we initialized without it, so we can pass it in countent or just rely on context.
        # Better: Prepend to chat session.
        
        if system_prompt:
             # Gemini doesn't strictly have "system" role in chat history for all versions, 
             # but we can prepend it to the first user message or use system_instruction.
             # We'll use a simple approach: Prepend to the current message context.
             pass # Gemini is smart enough usually.
        
        chat = self.gemini_model.start_chat(history=chat_history)
        
        full_prompt = message
        if system_prompt:
            full_prompt = f"System Instruction: {system_prompt}\n\nUser Query: {message}"

        if stream:
            response = chat.send_message(full_prompt, stream=True, generation_config=genai.GenerationConfig(temperature=temperature))
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        else:
            response = chat.send_message(full_prompt, generation_config=genai.GenerationConfig(temperature=temperature))
            return response.text

    def _generate_local(self, message: str, system_prompt: str, history: List[Dict], temperature: float, max_tokens: int, stream: bool):
        """Generate using Local Ollama"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            for msg in history:
                if msg['role'] in ['user', 'assistant', 'system']:
                    messages.append({"role": msg['role'], "content": msg['content']})
        
        messages.append({"role": "user", "content": message})
        
        if stream:
            stream_response = self.ollama_client.chat(
                model=self.local_model,
                messages=messages,
                stream=True,
                options={"temperature": temperature, "num_predict": max_tokens}
            )
            for chunk in stream_response:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
        else:
            response = self.ollama_client.chat(
                model=self.local_model,
                messages=messages,
                options={"temperature": temperature, "num_predict": max_tokens}
            )
            return response['message']['content']

    def create_educational_prompt(self, message: str, mode: str = "tutor") -> str:
        """Same as before"""
        base = "You are Professor Jarvis, an expert educational AI tutor."
        modes = {
            "quiz": f"{base}\nMODE: QUIZ\nGenerate 3-5 multiple choice questions on: {message}",
            "eli5": f"{base}\nMODE: ELI5\nExplain simply: {message}",
            "flashcard": f"{base}\nMODE: FLASHCARDS\nGenerate terms for: {message}",
            "tutor": f"{base}\nMODE: TUTOR\nGuide the user on: {message}"
        }
        return modes.get(mode, modes["tutor"])

    def create_coding_prompt(self, message: str) -> str:
        return f"You are Jarvis, an expert programming assistant.\nTask: {message}\nProvide clean, documented code."

# Global instance
llm_engine = HybridLLMEngine()
