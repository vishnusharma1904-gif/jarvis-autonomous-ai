from core.memory import memory_manager
from core.rag import rag_system
import time

def test_memory():
    print("🧠 Testing Memory System...")
    
    if not rag_system.enabled:
        print("❌ RAG System is disabled. Cannot test long-term memory.")
        return

    # Test 1: Store Memory
    print("\n1. Storing Memory...")
    fact = "My favorite color is neon blue."
    result = memory_manager.store_long_term_memory(fact)
    print(f"Result: {result}")
    
    # Wait for indexing (simulated)
    time.sleep(1)
    
    # Test 2: Retrieve Memory
    print("\n2. Retrieving Memory...")
    query = "What is my favorite color?"
    memories = memory_manager.search_memories(query)
    print(f"Query: {query}")
    print(f"Retrieved: {memories}")
    
    if any("neon blue" in m for m in memories):
        print("✅ Memory Test PASSED")
    else:
        print("❌ Memory Test FAILED")

if __name__ == "__main__":
    test_memory()
