import ast
import re
from typing import List, Dict


class TextChunker:
    """
    Production-ready document chunker.

    Strategies:
    - Python -> AST (functions/classes)
    - Markdown -> Heading based
    - Others -> Recursive character chunking
    """

    def __init__(self, chunk_size: int = 1200, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    # ==========================================================
    # Public API
    # ==========================================================

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:

        all_chunks = []

        for document in documents:

            language = document.get("language", "text")

            if language == "python":
                chunks = self._chunk_python(document)

            elif language == "markdown":
                chunks = self._chunk_markdown(document)

            else:
                chunks = self._chunk_text(document)

            all_chunks.extend(chunks)

        return all_chunks

    # ==========================================================
    # Python Chunking
    # ==========================================================

    def _chunk_python(self, document: Dict) -> List[Dict]:

        text = document["content"]

        lines = text.splitlines()

        chunks = []

        chunk_id = 0

        try:

            tree = ast.parse(text)

            for node in tree.body:

                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef,
                    ),
                ):

                    start = node.lineno - 1
                    end = node.end_lineno

                    code = "\n".join(lines[start:end])

                    # If too large -> split further
                    if len(code) > self.chunk_size:

                        pieces = self._split_large_text(code)

                        for piece in pieces:

                            chunks.append(
                                self._build_chunk(
                                    document=document,
                                    text=piece,
                                    chunk_id=chunk_id,
                                    chunk_type="python"
                                )
                            )

                            chunk_id += 1

                    else:

                        chunks.append(
                            self._build_chunk(
                                document=document,
                                text=code,
                                chunk_id=chunk_id,
                                chunk_type="python"
                            )
                        )

                        chunk_id += 1

            # Empty file / script without functions
            if not chunks:
                return self._chunk_text(document)

            return chunks

        except SyntaxError:
            # Invalid Python -> fallback
            return self._chunk_text(document)

    # ==========================================================
    # Markdown Chunking
    # ==========================================================

    def _chunk_markdown(self, document: Dict) -> List[Dict]:

        text = document["content"]

        chunks = []

        chunk_id = 0

        # Split before every heading
        sections = re.split(
            r"(?=^#{1,6}\s)",
            text,
            flags=re.MULTILINE
        )

        for section in sections:

            section = section.strip()

            if not section:
                continue

            if len(section) <= self.chunk_size:

                chunks.append(
                    self._build_chunk(
                        document=document,
                        text=section,
                        chunk_id=chunk_id,
                        chunk_type="markdown"
                    )
                )

                chunk_id += 1

            else:

                pieces = self._split_large_text(section)

                for piece in pieces:

                    chunks.append(
                        self._build_chunk(
                            document=document,
                            text=piece,
                            chunk_id=chunk_id,
                            chunk_type="markdown"
                        )
                    )

                    chunk_id += 1

        return chunks

    # ==========================================================
    # Generic Character Chunking
    # ==========================================================

    def _chunk_text(self, document: Dict) -> List[Dict]:

        text = document["content"]

        pieces = self._split_large_text(text)

        chunks = []

        for i, piece in enumerate(pieces):

            chunks.append(
                self._build_chunk(
                    document=document,
                    text=piece,
                    chunk_id=i,
                    chunk_type="text"
                )
            )

        return chunks

    # ==========================================================
    # Recursive Character Splitter
    # ==========================================================

    def _split_large_text(self, text: str) -> List[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks

    # ==========================================================
    # Shared Chunk Builder
    # ==========================================================

    def _build_chunk(
        self,
        document: Dict,
        text: str,
        chunk_id: int,
        chunk_type: str
    ) -> Dict:

        return {

            "text": text,

            "chunk_id": chunk_id,

            "chunk_type": chunk_type,

            "path": document["path"],

            "relative_path": document["relative_path"],

            "filename": document["filename"],

            "extension": document["extension"],

            "language": document["language"],

            "hash": document["hash"],

            "size": len(text)
        }