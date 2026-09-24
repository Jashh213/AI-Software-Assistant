from pathlib import Path
from typing import List, Dict
import hashlib
from datetime import datetime


class DocumentLoader:
    """
    Production-ready document loader.

    Responsibilities
    ----------------
    - Traverse repository
    - Ignore unnecessary files/directories
    - Read supported source files
    - Skip empty or huge files
    - Collect metadata
    """

    # =====================================================
    # Configuration
    # =====================================================

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".html",
        ".css",
        ".java",
        ".sql",
        ".xml",
    }

    IGNORE_FILES = {
        ".env",
        ".gitignore",
        "package-lock.json",
        "yarn.lock",
    }

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
        ".idea",
        ".vscode",
        ".next",
        ".pytest_cache",
        ".mypy_cache",
        "coverage",
        "target",
        "bin",
        "obj",
        "out",
    }

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "react",
        ".ts": "typescript",
        ".tsx": "react-typescript",
        ".java": "java",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".sql": "sql",
        ".xml": "xml",
        ".txt": "text",
    }

    # Skip extremely large files
    MAX_FILE_SIZE = 1_000_000  # 1 MB

    # Skip huge markdown documentation
    MAX_MARKDOWN_SIZE = 100_000

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self, project_path: str):

        self.project_path = Path(project_path).resolve()

    # =====================================================
    # Public API
    # =====================================================

    def load_documents(self) -> List[Dict]:

        documents: List[Dict] = []

        for file_path in self.project_path.rglob("*"):

            if not file_path.is_file():
                continue

            if self._should_ignore(file_path):
                continue

            try:

                stat = file_path.stat()

                # Skip huge files
                if stat.st_size > self.MAX_FILE_SIZE:
                    continue

                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                # Skip empty files
                if not content.strip():
                    continue

                # Skip massive markdown files
                if (
                    file_path.suffix.lower() == ".md"
                    and len(content) > self.MAX_MARKDOWN_SIZE
                ):
                    continue

                document = {
                    "path": str(file_path),
                    "relative_path": str(
                        file_path.relative_to(
                            self.project_path
                        )
                    ),
                    "filename": file_path.name,
                    "extension": file_path.suffix.lower(),
                    "language": self._detect_language(file_path),
                    "content": content,
                    "size": len(content),
                    "hash": self._calculate_hash(content),
                    "last_modified": datetime.fromtimestamp(
                        stat.st_mtime
                    ).isoformat(),
                }

                documents.append(document)

            except Exception as e:

                print(
                    f"[Loader] Could not read {file_path}: {e}"
                )

        print(f"Loaded {len(documents)} documents")

        return documents

    # =====================================================
    # Helpers
    # =====================================================

    def _should_ignore(
        self,
        file_path: Path
    ) -> bool:

        if file_path.name in self.IGNORE_FILES:
            return True

        if (
            file_path.suffix.lower()
            not in self.SUPPORTED_EXTENSIONS
        ):
            return True

        for part in file_path.parts:

            if part in self.IGNORE_DIRS:
                return True

        return False

    def _calculate_hash(
        self,
        content: str
    ) -> str:

        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

    def _detect_language(
        self,
        file_path: Path
    ) -> str:

        return self.LANGUAGE_MAP.get(
            file_path.suffix.lower(),
            "unknown"
        )