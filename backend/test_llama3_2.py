"""
Test script for the new lightweight Llama 3.2 3B model
"""

import sys
import os
import time

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.llm_engine import llm_engine

def test_basic_response():
    """Test basic conversation"""
    print("🧪 Testing basic conversation...")
    start = time.time()
    
    response = llm_engine.generate_response(
        message="Hello! What model are you and what can you help me with?",
        system_prompt="You are Jarvis, a helpful AI assistant.",
        temperature=0.7
    )
    
    elapsed = time.time() - start
    print(f"✅ Response received in {elapsed:.2f}s")
    print(f"📝 Response: {response[:200]}...")
    print()
    return elapsed

def test_code_generation():
    """Test code generation"""
    print("🧪 Testing code generation...")
    start = time.time()
    
    response = llm_engine.generate_response(
        message="Write a Python function to calculate fibonacci numbers",
        system_prompt=llm_engine.create_coding_prompt("fibonacci"),
        temperature=0.3
    )
    
    elapsed = time.time() - start
    print(f"✅ Code generated in {elapsed:.2f}s")
    print(f"📝 Response: {response[:300]}...")
    print()
    return elapsed

def test_reasoning():
    """Test reasoning capability"""
    print("🧪 Testing reasoning...")
    start = time.time()
    
    response = llm_engine.generate_response(
        message="If I have 3 apples and buy 2 more, then give 1 to my friend, how many do I have?",
        temperature=0.2
    )
    
    elapsed = time.time() - start
    print(f"✅ Reasoning completed in {elapsed:.2f}s")
    print(f"📝 Response: {response}")
    print()
    return elapsed

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Llama 3.2 3B Model Performance Test")
    print("=" * 60)
    print()
    
    try:
        # Run tests
        times = []
        times.append(test_basic_response())
        times.append(test_code_generation())
        times.append(test_reasoning())
        
        # Summary
        avg_time = sum(times) / len(times)
        print("=" * 60)
        print(f"📊 Performance Summary")
        print("=" * 60)
        print(f"Average response time: {avg_time:.2f}s")
        print(f"Total test time: {sum(times):.2f}s")
        print()
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
