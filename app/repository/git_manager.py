from pathlib import Path
import subprocess


class GitManager:
    """
    Handles all Git operations.

    Responsibilities
    ----------------
    - Validate GitHub URLs
    - Clone repositories
    - Check whether a repository already exists
    """

    # ==========================================
    # Validate Repository URL
    # ==========================================

    def validate_url(
        self,
        repository_url: str
    ) -> bool:
        """
        Basic validation for GitHub URLs.
        """

        return (
            repository_url.startswith("https://github.com/")
            or repository_url.startswith("git@github.com:")
        )

    # ==========================================
    # Repository Exists
    # ==========================================

    def repository_exists(
        self,
        repository_path: Path
    ) -> bool:
        """
        Check whether the repository
        already exists locally.
        """

        return repository_path.exists()

    # ==========================================
    # Clone Repository
    # ==========================================

    def clone_repository(
        self,
        repository_url: str,
        repository_path: Path
    ) -> None:
        """
        Clone a GitHub repository.
        """

        print(f"\nCloning repository...")

        subprocess.run(
            [
                "git",
                "clone",
                repository_url,
                str(repository_path)
            ],
            check=True
        )

        print("Repository cloned successfully.")