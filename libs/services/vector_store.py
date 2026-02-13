import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional

class VectorStore:
    """
    NumPy-based vector store for document embeddings and similarity search.
    """
    
    def __init__(self, rag_dir: str = "rag"):
        self.rag_dir = rag_dir
        self.documents_dir = os.path.join(rag_dir, "documents")
        self.index_file = os.path.join(rag_dir, "index.json")
        os.makedirs(self.documents_dir, exist_ok=True)
        
        # In-memory index
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load the document index."""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except:
                return {"documents": {}}
        return {"documents": {}}
    
    def _save_index(self) -> None:
        """Save the document index."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            print(f"Failed to save index: {e}")
    
    def add_document(self, doc_id: str, chunks: List[str], 
                     embeddings: np.ndarray, metadata: Dict) -> bool:
        """
        Add a document to the vector store.
        
        Args:
            doc_id: Unique document ID
            chunks: List of text chunks
            embeddings: Embedding vectors for chunks (N x D)
            metadata: Document metadata
            
        Returns:
            True if successful
        """
        try:
            # Save embeddings as numpy array
            embeddings_file = os.path.join(self.documents_dir, f"{doc_id}_embeddings.npy")
            np.save(embeddings_file, embeddings)
            
            # Save metadata and chunks
            metadata_file = os.path.join(self.documents_dir, f"{doc_id}_metadata.json")
            doc_data = {
                "id": doc_id,
                "chunks": chunks,
                "metadata": metadata,
                "embedding_dim": embeddings.shape[1],
                "chunk_count": len(chunks)
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, indent=2, ensure_ascii=False)
            
            # Update index
            self.index["documents"][doc_id] = {
                "embeddings_file": embeddings_file,
                "metadata_file": metadata_file,
                "chunk_count": len(chunks)
            }
            self._save_index()
            
            return True
            
        except Exception as e:
            print(f"Failed to add document: {e}")
            return False
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        """
        Search for similar chunks across all documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of top-k similar chunks with metadata
        """
        results = []
        
        for doc_id, doc_info in self.index["documents"].items():
            try:
                # Load embeddings
                embeddings = np.load(doc_info["embeddings_file"])
                
                # Load metadata
                with open(doc_info["metadata_file"], 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                
                # Compute similarities
                similarities = self._cosine_similarity(query_embedding, embeddings)
                
                # Add results with chunk info
                for i, sim in enumerate(similarities):
                    results.append({
                        "doc_id": doc_id,
                        "chunk_index": i,
                        "chunk_text": doc_data["chunks"][i],
                        "similarity": float(sim),
                        "metadata": doc_data["metadata"]
                    })
                    
            except Exception as e:
                print(f"Error searching document {doc_id}: {e}")
        
        # Sort by similarity and return top-k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store."""
        if doc_id not in self.index["documents"]:
            return False
        
        try:
            doc_info = self.index["documents"][doc_id]
            
            # Delete files
            if os.path.exists(doc_info["embeddings_file"]):
                os.remove(doc_info["embeddings_file"])
            if os.path.exists(doc_info["metadata_file"]):
                os.remove(doc_info["metadata_file"])
            
            # Remove from index
            del self.index["documents"][doc_id]
            self._save_index()
            
            return True
            
        except Exception as e:
            print(f"Failed to delete document: {e}")
            return False
    
    def list_documents(self) -> List[Dict]:
        """List all documents in the store."""
        docs = []
        for doc_id, doc_info in self.index["documents"].items():
            try:
                with open(doc_info["metadata_file"], 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                    docs.append({
                        "id": doc_id,
                        "chunk_count": doc_data["chunk_count"],
                        "metadata": doc_data["metadata"]
                    })
            except:
                pass
        return docs
    
    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between a vector and a matrix of vectors.
        
        Args:
            vec1: Query vector (D,)
            vec2: Document vectors (N x D)
            
        Returns:
            Similarity scores (N,)
        """
        # Normalize vectors
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2_norm = vec2 / (np.linalg.norm(vec2, axis=1, keepdims=True) + 1e-8)
        
        # Compute dot product
        similarities = np.dot(vec2_norm, vec1_norm)
        
        return similarities
