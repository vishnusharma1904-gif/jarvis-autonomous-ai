import unittest
from backend.core.llm_engine import llm_engine

class TestHybridRouter(unittest.TestCase):
    def test_simple_query(self):
        query = "Write a python function to add two numbers."
        is_complex = llm_engine._is_complex_query(query)
        print(f"Query: '{query}' -> Complex: {is_complex}")
        self.assertFalse(is_complex, "Simple coding query should be routed to Local")

    def test_complex_query(self):
        query = "Analyze the geopolitical implications of Mars colonization and design a comprehensive 10-year strategy for a sustainable colony."
        is_complex = llm_engine._is_complex_query(query)
        print(f"Query: '{query}' -> Complex: {is_complex}")
        self.assertTrue(is_complex, "Complex strategy query should be routed to Gemini")

    def test_complex_keywords(self):
        query = "Compare and contrast React and Vue."
        is_complex = llm_engine._is_complex_query(query)
        print(f"Query: '{query}' -> Complex: {is_complex}")
        self.assertTrue(is_complex, "Query with 'compare' should be complex")

if __name__ == '__main__':
    unittest.main()
