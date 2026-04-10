from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            # Temporarily disabling ChromaDB due to system access violation
            # import chromadb
            # client = chromadb.Client()
            # self._collection = client.get_or_create_collection(name=collection_name)
            # self._use_chroma = True
            self._use_chroma = False
            self._collection = None
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        """Build a normalized stored record for one document."""
        return {
            "id": doc.id,
            "content": doc.content,
            "embedding": self._embedding_fn(doc.content),
            "metadata": doc.metadata,
        }

    def _search_records(self, query_embedding: list[float], records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        """Run in-memory similarity search over provided records."""
        results = []
        for rec in records:
            score = _dot(query_embedding, rec["embedding"])
            results.append({
                "id": rec["id"],
                "content": rec["content"],
                "metadata": rec["metadata"],
                "score": score
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """Embed each document's content and store it."""
        for doc in docs:
            record = self._make_record(doc)
            if self._use_chroma and self._collection is not None:
                # ChromaDB requires metadata to be non-empty or None
                metadata = record["metadata"] if record["metadata"] and len(record["metadata"]) > 0 else None
                
                # Use upsert instead of add to handle potential duplicate IDs gracefully
                self._collection.upsert(
                    ids=[record["id"]],
                    documents=[record["content"]],
                    embeddings=[record["embedding"]],
                    metadatas=[metadata] if metadata is not None else None
                )
            else:
                self._store.append(record)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Find the top_k most similar documents to query."""
        query_embedding = self._embedding_fn(query)

        if self._use_chroma and self._collection is not None:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            # Flatten ChromaDB results format
            formatted = []
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    formatted.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                    })
            return formatted
        
        return self._search_records(query_embedding, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            return self._collection.count()
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """Search with optional metadata pre-filtering."""
        query_embedding = self._embedding_fn(query)

        if self._use_chroma and self._collection is not None:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=metadata_filter
            )
            # Flatten results
            formatted = []
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    formatted.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                    })
            return formatted

        # In-memory filtering
        filtered_records = []
        for rec in self._store:
            match = True
            if metadata_filter:
                for k, v in metadata_filter.items():
                    if rec["metadata"].get(k) != v:
                        match = False
                        break
            if match:
                filtered_records.append(rec)
        
        return self._search_records(query_embedding, filtered_records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """Remove all chunks belonging to a document."""
        if self._use_chroma and self._collection is not None:
            # ChromaDB delete supports 'ids' or 'where'
            # We try both: exact ID match OR doc_id in metadata
            count_before = self._collection.count()
            self._collection.delete(ids=[doc_id])
            self._collection.delete(where={"doc_id": doc_id})
            return self._collection.count() < count_before

        # In-memory
        initial_count = len(self._store)
        self._store = [
            rec for rec in self._store 
            if rec["id"] != doc_id and rec["metadata"].get("doc_id") != doc_id
        ]
        return len(self._store) < initial_count
