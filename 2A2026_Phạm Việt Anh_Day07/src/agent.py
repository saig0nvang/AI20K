from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        # 1. Retrieve top-k relevant chunks from the store
        results = self.store.search(question, top_k=top_k)
        
        # 2. Build a prompt with the chunks as context
        context_parts = [r["content"] for r in results]
        context = "\n---\n".join(context_parts)
        
        prompt = (
            "Bạn là một trợ lý ảo hữu ích. Hãy sử dụng ngữ cảnh dưới đây để trả lời câu hỏi.\n"
            "Nếu thông tin không có trong ngữ cảnh, hãy nói rằng bạn không biết, đừng tự ý bịa thêm.\n\n"
            f"Ngữ cảnh:\n{context}\n\n"
            f"Câu hỏi: {question}\n\n"
            "Trả lời:"
        )

        # 3. Call the LLM to generate an answer
        return self.llm_fn(prompt)
