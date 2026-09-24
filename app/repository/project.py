from dataclasses import dataclass
from pathlib import Path

from app.rag.vector_store import VectorStore


@dataclass
class Project:
    """
    Represents a repository that is ready to be used
    by the AI assistant.
    """

    project_id: str

    repository_url: str

    local_path: Path

    vector_store: VectorStore

    indexed: bool