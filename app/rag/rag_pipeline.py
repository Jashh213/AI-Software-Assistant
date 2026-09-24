from typing import List, Dict

from app.llm.base import BaseLLM
from app.rag.retriever import Retriever


class RAGPipeline:
    """
    Production RAG Pipeline.

    Responsibilities
    ----------------
    - Retrieve relevant chunks
    - Build repository context
    - Build augmented prompt
    - Ask the configured LLM
    """

    def __init__(
        self,
        retriever: Retriever,
        llm: BaseLLM,
    ):

        self.retriever = retriever
        self.llm = llm

    # =====================================================

    def answer(
        self,
        question: str,
        top_k: int = 10,
    ) -> str:

        chunks = self.retriever.retrieve(
            question=question,
            top_k=top_k,
        )

        print("\n========== RETRIEVED CHUNKS ==========")

        for chunk in chunks:
            print(chunk["relative_path"])

        print("======================================\n")

        if not chunks:

            return (
                "I couldn't find that information "
                "in the repository."
            )

        context = self._build_context(chunks)

        prompt = self._build_prompt(
            question,
            context,
        )

        return self.llm.generate(prompt)

    # =====================================================

    def _build_context(
        self,
        chunks: List[Dict],
    ) -> str:

        sections = []

        for chunk in chunks:

            sections.append(
                f"""
File:
{chunk['relative_path']}

Content:
{chunk['text']}
"""
            )

        return "\n\n--------------------------\n\n".join(
            sections
        )

    # =====================================================

    def _build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""
You are an expert Software Engineering Assistant.

Answer ONLY using the repository context below.

Rules

- Use ONLY the provided repository context.
- If the answer is not available, reply:
  "I couldn't find that information in the repository."

- Mention filenames whenever possible.
- Explain code clearly.

==============================
Repository Context
==============================

{context}

==============================
Question
==============================

{question}

==============================
Answer
==============================
"""