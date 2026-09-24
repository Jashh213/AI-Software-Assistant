from typing import Dict, Any, List

from app.memory.base_memory import BaseMemory


class ProjectMemory(BaseMemory):
    """
    Stores metadata about a repository.the original code will still be in the indexer of indexing phase.

    One ProjectMemory exists per repository.
    """

    def __init__(
        self,
        project_id: str,
        repository_path: str
    ):

        self.project_id = project_id

        memory_path = (
            f"storage/memory/projects/{project_id}.json"
        )

        super().__init__(memory_path)

        self.repository_path = repository_path

        self.languages: List[str] = []

        self.frameworks: List[str] = []

        self.dependencies: List[str] = []

        self.entry_points: List[str] = []

        self.total_files = 0

        self.repository_hash = ""

        self.last_indexed = None

        self.load()

    # ==========================================
    # Setters
    # ==========================================

    def set_languages(self, languages: List[str]):

        self.languages = languages

    def set_frameworks(self, frameworks: List[str]):

        self.frameworks = frameworks

    def set_dependencies(self, dependencies: List[str]):

        self.dependencies = dependencies

    def set_entry_points(self, entry_points: List[str]):

        self.entry_points = entry_points

    def set_total_files(self, total_files: int):

        self.total_files = total_files

    def set_repository_hash(self, repository_hash: str):

        self.repository_hash = repository_hash

    def set_last_indexed(self, timestamp: str):

        self.last_indexed = timestamp

    # ==========================================
    # BaseMemory
    # ==========================================

    def to_dict(self):

        return {

            "project_id": self.project_id,

            "repository_path": self.repository_path,

            "languages": self.languages,

            "frameworks": self.frameworks,

            "dependencies": self.dependencies,

            "entry_points": self.entry_points,

            "total_files": self.total_files,

            "repository_hash": self.repository_hash,

            "last_indexed": self.last_indexed
        }

    def from_dict(
        self,
        data: Dict[str, Any]
    ):

        self.repository_path = data.get(
            "repository_path",
            self.repository_path
        )

        self.languages = data.get(
            "languages",
            []
        )

        self.frameworks = data.get(
            "frameworks",
            []
        )

        self.dependencies = data.get(
            "dependencies",
            []
        )

        self.entry_points = data.get(
            "entry_points",
            []
        )

        self.total_files = data.get(
            "total_files",
            0
        )

        self.repository_hash = data.get(
            "repository_hash",
            ""
        )

        self.last_indexed = data.get(
            "last_indexed",
            None
        )

    def clear(self):

        self.languages.clear()

        self.frameworks.clear()

        self.dependencies.clear()

        self.entry_points.clear()

        self.total_files = 0

        self.repository_hash = ""

        self.last_indexed = None

        self.save()