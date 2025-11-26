"""
RAG System (Retrieval Augmented Generation)
Handles document indexing and retrieval.
Gracefully degrades if ML dependencies are missing.
"""

import json
import os
from typing import List, Dict, Any

class RAGSystem:
    def __init__(self):
        self.enabled = False
        self.collection = None
        self.model = None
        
        try:
            print("📚 Initializing RAG System...")
            import chromadb
            from sentence_transformers import SentenceTransformer
            
            # Initialize Vector DB
            self.client = chromadb.PersistentClient(path="./backend/data/chromadb")
            self.collection = self.client.get_or_create_collection(name="jarvis_knowledge")
            
            # Initialize Embedding Model
            # using all-MiniLM-L6-v2 which is small and fast
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.enabled = True
            print("✅ RAG System Initialized Successfully")
            
        except ImportError as e:
            print(f"⚠️  RAG System Disabled: Missing dependencies ({e})")
            print("   To enable: pip install chromadb sentence-transformers")
        except Exception as e:
            print(f"❌ RAG System Error: {e}")

    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the knowledge base"""
        if not self.enabled:
            return "rag_disabled"
            
        try:
            # Generate ID
            doc_id = f"doc_{hash(text)}"
            
            # Generate embedding
            embedding = self.model.encode(text).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            return doc_id
        except Exception as e:
            print(f"Error adding document: {e}")
            return "error"

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        if not self.enabled:
            return []
            
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []

    def get_context_for_query(self, query: str, n_results: int = 3) -> str:
        """Get formatted context string for LLM prompt"""
        if not self.enabled:
            return ""
            
        results = self.search(query, n_results)
        if not results:
            return ""
            
        context = "Relevant Context from Knowledge Base:\n"
        for i, res in enumerate(results):
            context += f"[{i+1}] {res['content'][:500]}...\n"
            
        return context

    def get_stats(self) -> Dict:
        if not self.enabled:
            return {"status": "disabled"}
        return {
            "status": "active",
            "count": self.collection.count()
        }

# Global instance
rag_system = RAGSystem()
