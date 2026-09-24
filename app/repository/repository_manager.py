from pathlib import Path
import hashlib
from datetime import datetime

from app.repository.project import Project
from app.repository.git_manager import GitManager

from app.memory.project_memory import ProjectMemory

from app.rag.indexer import Indexer
from app.rag.vector_store import VectorStore
from app.rag.loader import DocumentLoader


class RepositoryManager:
    """
    Manages repositories for the AI Software Engineering Assistant.

    Responsibilities
    ----------------
    - Validate repository URLs
    - Clone repositories
    - Build or load FAISS indexes
    - Cache opened repositories
    - Return ready-to-use Project objects
    """

    def __init__(
        self,
        git_manager: GitManager,
        repositories_dir: str = "repositories",
        storage_dir: str = "storage"
    ):

        self.git_manager = git_manager

        self.repositories_dir = Path(repositories_dir)
        self.storage_dir = Path(storage_dir)

        self.repositories_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------
        # Cache
        # ----------------------------------------

        self._projects: dict[str, Project] = {}

        self.current_project: Project | None = None

    # ====================================================
    # Public API
    # ====================================================

    def open_repository(
        self,
        repository_url: str
    ) -> Project:

        # ----------------------------------------
        # Already Open?
        # ----------------------------------------

        if repository_url in self._projects:

            self.current_project = self._projects[
                repository_url
            ]

            return self.current_project

        # ----------------------------------------
        # Validate URL
        # ----------------------------------------

        if not self.git_manager.validate_url(repository_url):
            raise ValueError(
                "Invalid GitHub repository URL."
            )

        # ----------------------------------------
        # Generate Project ID
        # ----------------------------------------

        project_id = self._generate_project_id(
            repository_url
        )

        repository_path = (
            self.repositories_dir / project_id
        )

        storage_path = (
            self.storage_dir / project_id
        )

        storage_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------
        # Clone Repository
        # ----------------------------------------

        if not self.git_manager.repository_exists(
            repository_path
        ):

            print("Cloning repository...")

            self.git_manager.clone_repository(
                repository_url,
                repository_path
            )

        # ----------------------------------------
        # Index Files
        # ----------------------------------------

        index_file = storage_path / "index.faiss"
        metadata_file = storage_path / "metadata.pkl"

        if index_file.exists() and metadata_file.exists():

            print("Loading existing FAISS index...")

            vector_store = VectorStore.load(
                index_path=str(index_file),
                metadata_path=str(metadata_file)
            )

        else:

            print("Building new FAISS index...")

            indexer = Indexer(
                str(repository_path)
            )

            vector_store = indexer.build_index(
                index_path=str(index_file),
                metadata_path=str(metadata_file)
            )

        # ----------------------------------------
        # Repository Metadata
        # ----------------------------------------

        loader = DocumentLoader(
            str(repository_path)
        )

        documents = loader.load_documents()

        languages = sorted(
            {
                doc["language"]
                for doc in documents
                if doc["language"] != "unknown"
            }
        )

        repository_hash = self._calculate_repository_hash(
            documents
        )

        # ----------------------------------------
        # Project Memory
        # ----------------------------------------

        project_memory = ProjectMemory(
            project_id=project_id,
            repository_path=str(repository_path)
        )

        project_memory.set_languages(
            languages
        )

        project_memory.set_total_files(
            len(documents)
        )

        project_memory.set_repository_hash(
            repository_hash
        )

        project_memory.set_last_indexed(
            datetime.now().isoformat()
        )

        project_memory.save()

        # ----------------------------------------
        # Create Project
        # ----------------------------------------

        project = Project(
            project_id=project_id,
            repository_url=repository_url,
            local_path=repository_path,
            vector_store=vector_store,
            indexed=True
        )

        # ----------------------------------------
        # Cache Project
        # ----------------------------------------

        self._projects[
            repository_url
        ] = project

        self.current_project = project

        return project

    # ====================================================
    # Current Project
    # ====================================================

    def get_current_project(self) -> Project | None:

        return self.current_project

    # ====================================================
    # Helpers
    # ====================================================

    def _generate_project_id(
        self,
        repository_url: str
    ) -> str:

        return hashlib.sha256(
            repository_url.encode("utf-8")
        ).hexdigest()[:12]

    def _calculate_repository_hash(
        self,
        documents: list[dict]
    ) -> str:

        sha = hashlib.sha256()

        for document in sorted(
            documents,
            key=lambda x: x["relative_path"]
        ):
            sha.update(
                document["hash"].encode("utf-8")
            )

        return sha.hexdigest()