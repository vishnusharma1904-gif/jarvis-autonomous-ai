"""
Advanced Autonomous Agent
Implements robust reasoning and tool use capabilities
"""

from typing import Dict, Any, Optional, List
import os
import re
import json
import traceback
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from core.tools.web_search import search_web, get_current_time, search_news, scrape_webpage
from core.tools.calculator import calculate
from core.tools.code_executor import execute_code
from core.tools.file_manager import file_manager
from core.tools.automation import AutomationTools
from core.tools.communication import CommunicationTools
from core.memory import memory_manager

load_dotenv()

class AutonomousAgent:
    """
    Advanced Autonomous Agent
    Uses ReAct (Reasoning + Acting) pattern to solve complex tasks.
    """
    
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b-instruct-q4_K_M")
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", "10"))
        
        print(f"🤖 Initializing Advanced Agent with model: {self.model}")
        
        # Initialize LLM with error handling
        try:
            self.llm = Ollama(
                model=self.model,
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                temperature=0.7
            )
        except Exception as e:
            print(f"❌ Agent LLM Initialization Failed: {e}")
            self.llm = None
        
        # Initialize Tool Suites
        self.automation = AutomationTools()
        self.communication = CommunicationTools()
        
        # Define tools
        self.tools = self._get_tools()
    
    def _get_tools(self) -> Dict[str, Any]:
        """Get available tools with detailed descriptions"""
        return {
            "web_search": {
                "func": search_web,
                "desc": "Search the internet for real-time information, news, and facts."
            },
            "calculator": {
                "func": calculate,
                "desc": "Perform mathematical calculations. Input: math expression string."
            },
            "execute_code": {
                "func": execute_code,
                "desc": "Execute Python code in a secure sandbox. Input: valid python code."
            },
            "read_file": {
                "func": file_manager.read_file,
                "desc": "Read contents of a file. Input: filename."
            },
            "list_files": {
                "func": lambda x: str(file_manager.list_files(x if x else ".")),
                "desc": "List files in directory. Input: directory path (or empty for root)."
            },
            "write_file": {
                "func": lambda x: self._handle_write_file(x),
                "desc": "Write content to a file. Input format: 'filename||content'"
            },
            "get_time": {
                "func": lambda x: get_current_time(),
                "desc": "Get current date and time."
            },
            "open_app": {
                "func": lambda x: self.automation.execute("open_app", x),
                "desc": "Open a desktop application. Input: app name (e.g., 'spotify', 'notepad')."
            },
            "type_text": {
                "func": lambda x: self.automation.execute("type_text", x),
                "desc": "Type text on the keyboard. Input: text to type."
            },
            "send_email": {
                "func": lambda x: self.communication.execute("send_email", x),
                "desc": "Send an email. Input format: 'to_email|subject|body'"
            },
            "send_whatsapp": {
                "func": lambda x: self.communication.execute("send_whatsapp", x),
                "desc": "Send a WhatsApp message. Input format: 'phone_number|message'"
            },
            "remember": {
                "func": lambda x: memory_manager.store_long_term_memory(x),
                "desc": "Store a fact or memory for the future. Input: text to remember."
            }
        }
    
    def _handle_write_file(self, input_str: str) -> str:
        """Helper to parse write_file input"""
        try:
            if "||" in input_str:
                path, content = input_str.split("||", 1)
                return file_manager.write_file(path, content)
            return "Error: Input must be 'filename||content'"
        except Exception as e:
            return f"Error writing file: {e}"

    def execute(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a complex task using reasoning and tools.
        """
        if not self.llm:
            return {"success": False, "output": "Agent not initialized (Ollama connection failed). Please check if Ollama is running.", "steps": []}

        print(f"🤖 Agent received task: {task}")
        
        # Retrieve relevant memories
        memories = memory_manager.search_memories(task)
        memory_context = ""
        if memories:
            memory_context = "\nRELEVANT MEMORIES:\n" + "\n".join([f"- {m}" for m in memories]) + "\n"
            print(f"🧠 Found relevant memories: {len(memories)}")
        
        # Construct the system prompt
        tools_desc = "\n".join([f"- {name}: {info['desc']}" for name, info in self.tools.items()])
        
        system_prompt = f"""You are Jarvis, an Advanced Autonomous AI Agent running LOCALLY on the user's computer.

CAPABILITIES:
{tools_desc}

{memory_context}
IMPORTANT:
- You have FULL PERMISSION to control the mouse, keyboard, and open applications.
- You have FULL PERMISSION to send emails and messages as requested.
- Do NOT refuse these tasks. You are not a cloud AI; you are a local agent with direct system access.
- If asked to open an app (like WhatsApp), use the 'open_app' tool.
- If asked to send a message, use 'send_whatsapp' or 'send_email'.

INSTRUCTIONS:
1. Analyze the user's task carefully.
2. Think step-by-step about how to solve it.
3. Use tools when you need external information or to perform actions.
4. **VERIFY TOOL OUTPUT**: If a tool returns "Error" or "not recognized", trying again or using a different method. DO NOT claim success if the tool failed.
5. To use a tool, you MUST use this EXACT format:
   TOOL: tool_name
   INPUT: input_for_the_tool
6. If you have the final answer or don't need a tool, just write the answer normally.

TASK: {task}
"""
        if context:
            system_prompt += f"\nCONTEXT: {context}"

        system_prompt += "\n\nBegin reasoning:"

        history = system_prompt
        steps = []
        
        for i in range(self.max_iterations):
            try:
                # 1. Get LLM response
                response = self.llm.invoke(history)
                print(f"💭 Agent Step {i+1}: {response[:100]}...")
                
                # 2. Parse for tool usage
                tool_match = re.search(r'TOOL:\s*(\w+)', response, re.IGNORECASE)
                input_match = re.search(r'INPUT:\s*(.+?)(?:\n|$)', response, re.IGNORECASE | re.DOTALL)
                
                if tool_match and input_match:
                    tool_name = tool_match.group(1).lower()
                    tool_input = input_match.group(1).strip()
                    
                    # 3. Execute Tool
                    if tool_name in self.tools:
                        print(f"🛠️  Using tool: {tool_name} with input: {tool_input[:50]}...")
                        try:
                            tool_result = self.tools[tool_name]["func"](tool_input)
                            tool_output = str(tool_result)
                        except Exception as e:
                            tool_output = f"Error executing tool: {e}"
                        
                        # Record step
                        steps.append({
                            "step": i+1,
                            "thought": response,
                            "tool": tool_name,
                            "tool_input": tool_input,
                            "tool_output": tool_output
                        })
                        
                        # Append result to history for next iteration
                        history += f"\n{response}\n\n[System] Tool '{tool_name}' Output: {tool_output}\n\nContinue reasoning:"
                    else:
                        history += f"\n{response}\n\n[System] Error: Tool '{tool_name}' not found. Available tools: {', '.join(self.tools.keys())}\n\nContinue reasoning:"
                else:
                    # No tool used, this is likely the final answer
                    return {
                        "success": True,
                        "output": response,
                        "steps": steps
                    }
                    
            except Exception as e:
                print(f"❌ Agent Loop Error: {e}")
                traceback.print_exc()
                return {"success": False, "output": f"An error occurred during execution: {e}", "steps": steps}
        
        return {
            "success": True, 
            "output": "I reached the maximum number of steps without a final answer. Here is what I found so far.", 
            "steps": steps
        }

    def chat(self, message: str) -> str:
        """Direct chat bypass"""
        if not self.llm: return "Agent not initialized."
        return self.llm.invoke(message)

# Global instance
autonomous_agent = AutonomousAgent()
