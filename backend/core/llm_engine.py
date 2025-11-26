"""
Local LLM Engine using Ollama
Replaces Google Gemini API with local Qwen2.5-Coder model
"""

import os
import time
from typing import List, Dict, Optional, Generator
import ollama
from dotenv import load_dotenv

load_dotenv()

class LocalLLMEngine:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b-instruct-q4_K_M")
        self.client = ollama.Client(host=self.base_url)
        self.last_call_time = 0
        self.min_delay = 0.5  # Small delay to prevent overload
        
        # Verify Ollama is running and model exists
        self._verify_setup()
    
    def _verify_setup(self):
        """Verify Ollama connection and model availability"""
        try:
            # Test connection
            models = self.client.list()
            
            # Handle different response formats
            model_list = []
            if hasattr(models, 'models'):
                model_list = models.models
            elif isinstance(models, dict) and 'models' in models:
                model_list = models['models']
            else:
                model_list = models if isinstance(models, list) else []
            
            # Extract model names
            model_names = []
            for m in model_list:
                if hasattr(m, 'model'):
                    model_names.append(m.model)
                elif isinstance(m, dict):
                    model_names.append(m.get('name', '') or m.get('model', ''))
                else:
                    model_names.append(str(m))
            
            # Check if our model is available
            if not any(self.model in name for name in model_names):
                print(f"⚠️  Model {self.model} not found")
                print(f"💡 Available models: {', '.join(model_names) if model_names else 'None'}")
                print(f"💡 Run: ollama pull {self.model}")
            else:
                print(f"✅ Ollama connected: {self.model}")
                
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            print("💡 Make sure Ollama is running: ollama serve")
    
    def generate_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False
    ) -> str | Generator:
        """
        Generate response from local LLM
        
        Args:
            message: User message
            system_prompt: System instruction
            history: Conversation history
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
        
        Returns:
            str or Generator of response chunks
        """
        # Rate limiting
        time_since_last = time.time() - self.last_call_time
        if time_since_last < self.min_delay:
            time.sleep(self.min_delay - time_since_last)
        
        # Build messages
        messages = []
        
        # Add system prompt
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history
        if history:
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role in ["user", "assistant", "system"]:
                    messages.append({
                        "role": role,
                        "content": content
                    })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        try:
            if stream:
                return self._generate_stream(messages, temperature, max_tokens)
            else:
                return self._generate_complete(messages, temperature, max_tokens)
        
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return "I apologize, I encountered an error processing your request. Please ensure Ollama is running."
        
        finally:
            self.last_call_time = time.time()
    
    def _generate_complete(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Generate complete response"""
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        )
        
        return response['message']['content']
    
    def _generate_stream(self, messages: List[Dict], temperature: float, max_tokens: int) -> Generator:
        """Generate streaming response"""
        stream = self.client.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    
    def create_educational_prompt(self, message: str, mode: str = "tutor") -> str:
        """
        Create educational system prompts for different modes
        
        Args:
            message: User's question/request
            mode: Educational mode (quiz, eli5, flashcard, tutor)
        
        Returns:
            System prompt for the mode
        """
        base = "You are Professor Jarvis, an expert educational AI tutor specializing in coding, reasoning, and educational support."
        
        modes = {
            "quiz": f"""{base}
            
MODE: QUIZ GENERATOR
Generate 3-5 challenging multiple-choice questions on the topic: "{message}"
- Provide options (A, B, C, D)
- DO NOT reveal answers immediately
- Ask user to attempt first
- After user answers, provide detailed explanations

Focus on: reasoning, problem-solving, and practical application.""",
            
            "eli5": f"""{base}
            
MODE: ELI5 (Explain Like I'm 5)
Explain "{message}" using:
- Simple, real-world analogies
- No complex jargon
- Bullet points for clarity
- Fun and engaging examples

Make it accessible to beginners while being accurate.""",
            
            "flashcard": f"""{base}
            
MODE: FLASHCARD GENERATOR
Generate 5 key term-definition pairs for: "{message}"
Format:
**Term**: Clear, concise definition

Focus on high-yield concepts for learning and retention.""",
            
            "tutor": f"""{base}
            
MODE: SOCRATIC TUTOR
For the question: "{message}"
- Guide the user to discover the answer
- Ask probing questions
- Check understanding at each step
- If they make mistakes, explain gently
- Focus on building intuition and reasoning

Be encouraging and supportive."""
        }
        
        return modes.get(mode, modes["tutor"])
    
    def create_coding_prompt(self, message: str) -> str:
        """Create optimized prompt for coding tasks"""
        return f"""You are Jarvis, an expert programming assistant with deep knowledge of software development, algorithms, and best practices.

For coding tasks:
- Write clean, well-documented code
- Follow best practices and design patterns
- Include comments explaining complex logic
- Consider edge cases and error handling
- Optimize for readability and maintainability

User request: {message}

Provide code with explanations. If debugging, explain the issue and solution clearly."""

# Global instance
llm_engine = LocalLLMEngine()
