"""
RAG (Retrieval-Augmented Generation) service for Study Assistant Bot.
Manages embeddings, vector storage, and document retrieval.
"""

import logging
import os
import json
from typing import Optional, List, Tuple
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from services.ai_service import get_ai_service
from config import Config

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval-Augmented Generation."""
    
    def __init__(self):
        """Initialize RAG service."""
        self.enabled = Config.RAG_ENABLED and Config.ENABLE_RAG
        self.embeddings_model_name = Config.EMBEDDINGS_MODEL
        self.vector_db_path = Path(Config.VECTOR_DB_PATH)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        if self.enabled:
            try:
                self.embeddings_model = SentenceTransformer(self.embeddings_model_name)
                logger.info(f"RAG service initialized with model: {self.embeddings_model_name}")
            except Exception as e:
                logger.error(f"Error loading embeddings model: {e}")
                self.enabled = False
        else:
            self.embeddings_model = None
    
    def get_index_path(self, user_id: int) -> Path:
        """Get FAISS index path for user."""
        return self.vector_db_path / f"user_{user_id}.index"
    
    def get_metadata_path(self, user_id: int) -> Path:
        """Get metadata path for user."""
        return self.vector_db_path / f"user_{user_id}_metadata.json"
    
    def create_index(self, user_id: int, dimension: int = 384) -> faiss.IndexFlatL2:
        """Create new FAISS index for user."""
        try:
            index = faiss.IndexFlatL2(dimension)
            return index
        except Exception as e:
            logger.error(f"Error creating FAISS index: {e}")
            return None
    
    def load_or_create_index(self, user_id: int) -> Tuple[Optional[faiss.IndexFlatL2], dict]:
        """Load existing FAISS index or create new one."""
        try:
            if not self.enabled:
                return None, {}
            
            index_path = self.get_index_path(user_id)
            metadata_path = self.get_metadata_path(user_id)
            
            if index_path.exists():
                index = faiss.read_index(str(index_path))
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                logger.info(f"Loaded existing index for user {user_id}")
                return index, metadata
            else:
                index = self.create_index(user_id)
                metadata = {"chunks": [], "document_ids": []}
                logger.info(f"Created new index for user {user_id}")
                return index, metadata
        except Exception as e:
            logger.error(f"Error loading/creating index: {e}")
            return None, {}
    
    def save_index(self, user_id: int, index: faiss.IndexFlatL2, metadata: dict) -> bool:
        """Save FAISS index and metadata."""
        try:
            if index is None:
                return False
            
            index_path = self.get_index_path(user_id)
            metadata_path = self.get_metadata_path(user_id)
            
            faiss.write_index(index, str(index_path))
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)
            
            logger.info(f"Saved index for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            return False
    
    def add_chunks_to_index(
        self,
        user_id: int,
        chunks: List[str],
        document_id: int,
        document_name: str,
    ) -> bool:
        """Add document chunks to vector index."""
        try:
            if not self.enabled or not self.embeddings_model:
                return False
            
            index, metadata = self.load_or_create_index(user_id)
            if index is None:
                return False
            
            embeddings = self.embeddings_model.encode(chunks, convert_to_numpy=True)
            embeddings = np.array(embeddings, dtype=np.float32)
            
            index.add(embeddings)
            
            # Update metadata
            for i, chunk in enumerate(chunks):
                metadata["chunks"].append({
                    "index": index.ntotal - len(chunks) + i,
                    "text": chunk[:200],  # Store preview
                    "document_id": document_id,
                    "document_name": document_name,
                    "chunk_position": i,
                })
            
            if document_id not in metadata["document_ids"]:
                metadata["document_ids"].append(document_id)
            
            self.save_index(user_id, index, metadata)
            logger.info(f"Added {len(chunks)} chunks for document {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding chunks to index: {e}")
            return False
    
    def retrieve_relevant_chunks(
        self,
        user_id: int,
        query: str,
        k: int = 5,
    ) -> List[dict]:
        """Retrieve top-k relevant chunks for query."""
        try:
            if not self.enabled or not self.embeddings_model:
                return []
            
            index, metadata = self.load_or_create_index(user_id)
            if index is None or index.ntotal == 0:
                return []
            
            # Encode query
            query_embedding = self.embeddings_model.encode([query], convert_to_numpy=True)
            query_embedding = np.array(query_embedding, dtype=np.float32)
            
            # Search
            distances, indices = index.search(query_embedding, min(k, index.ntotal))
            
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx < len(metadata["chunks"]):
                    chunk_metadata = metadata["chunks"][idx]
                    results.append({
                        "text": chunk_metadata["text"],
                        "document_id": chunk_metadata["document_id"],
                        "document_name": chunk_metadata["document_name"],
                        "similarity": float(distance),
                        "chunk_position": chunk_metadata["chunk_position"],
                    })
            
            logger.info(f"Retrieved {len(results)} relevant chunks for user {user_id}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return []
    
    def delete_document_chunks(self, user_id: int, document_id: int) -> bool:
        """Delete all chunks for a document."""
        try:
            if not self.enabled:
                return False
            
            index, metadata = self.load_or_create_index(user_id)
            if index is None:
                return False
            
            # Remove chunks for this document
            remaining_chunks = [
                chunk for chunk in metadata["chunks"]
                if chunk["document_id"] != document_id
            ]
            
            if len(remaining_chunks) == len(metadata["chunks"]):
                logger.info(f"No chunks found for document {document_id}")
                return True
            
            # Rebuild index with remaining chunks
            if remaining_chunks:
                chunk_texts = [chunk["text"] for chunk in remaining_chunks]
                embeddings = self.embeddings_model.encode(chunk_texts, convert_to_numpy=True)
                embeddings = np.array(embeddings, dtype=np.float32)
                
                new_index = self.create_index(user_id, embeddings.shape[1])
                new_index.add(embeddings)
                
                # Update indices in metadata
                for i, chunk in enumerate(remaining_chunks):
                    chunk["index"] = i
                
                metadata["chunks"] = remaining_chunks
            else:
                # Create empty index
                new_index = self.create_index(user_id)
                metadata["chunks"] = []
            
            # Remove document ID
            if document_id in metadata["document_ids"]:
                metadata["document_ids"].remove(document_id)
            
            self.save_index(user_id, new_index, metadata)
            logger.info(f"Deleted chunks for document {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document chunks: {e}")
            return False
    
    def augment_context_with_rag(
        self,
        user_id: int,
        question: str,
        max_context_length: int = None,
    ) -> Tuple[Optional[str], List[dict]]:
        """Augment question context using RAG."""
        try:
            if not self.enabled:
                return None, []
            
            max_context_length = max_context_length or Config.MAX_CONTEXT_LENGTH
            
            # Retrieve relevant chunks
            relevant_chunks = self.retrieve_relevant_chunks(user_id, question, k=5)
            
            if not relevant_chunks:
                return None, []
            
            # Build context from chunks
            context_parts = []
            total_length = 0
            
            for chunk in relevant_chunks:
                chunk_text = f"From {chunk['document_name']}: {chunk['text']}"
                if total_length + len(chunk_text) <= max_context_length:
                    context_parts.append(chunk_text)
                    total_length += len(chunk_text)
            
            if not context_parts:
                return None, relevant_chunks
            
            context = "\n\n".join(context_parts)
            return context, relevant_chunks
        except Exception as e:
            logger.error(f"Error augmenting context with RAG: {e}")
            return None, []
    
    def get_user_statistics(self, user_id: int) -> dict:
        """Get RAG statistics for user."""
        try:
            if not self.enabled:
                return {}
            
            index, metadata = self.load_or_create_index(user_id)
            
            if index is None:
                return {}
            
            return {
                "total_vectors": index.ntotal,
                "total_chunks": len(metadata["chunks"]),
                "total_documents": len(metadata["document_ids"]),
                "documents": metadata["document_ids"],
            }
        except Exception as e:
            logger.error(f"Error getting RAG statistics: {e}")
            return {}


# Global RAG service instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
