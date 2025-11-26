import time
import os
from langchain_community.llms import Ollama
from core.agent import autonomous_agent

def benchmark():
    print("🚀 Starting Performance Benchmark...")
    
    # 1. Test Ollama Raw Speed
    print("\n1. Testing Ollama Raw Response Time...")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    llm = Ollama(model=model, base_url="http://localhost:11434")
    
    start_time = time.time()
    response = llm.invoke("Hello, are you ready?")
    end_time = time.time()
    duration = end_time - start_time
    print(f"   Model: {model}")
    print(f"   Response: {response.strip()}")
    print(f"   Time: {duration:.2f} seconds")
    
    if duration > 5:
        print("   ⚠️  Ollama is running SLOWly (>5s for simple prompt)")
    else:
        print("   ✅ Ollama speed is acceptable")

    # 2. Test Agent Execution Speed
    print("\n2. Testing Full Agent Execution Loop...")
    task = "Calculate 25 * 4"
    start_time = time.time()
    result = autonomous_agent.execute(task)
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"   Task: {task}")
    print(f"   Result: {result.get('output', '')[:50]}...")
    print(f"   Time: {duration:.2f} seconds")
    
    if duration > 10:
        print("   ⚠️  Agent is running SLOWly (>10s for simple task)")
    else:
        print("   ✅ Agent speed is acceptable")

if __name__ == "__main__":
    benchmark()
