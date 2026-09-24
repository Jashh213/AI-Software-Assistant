import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseMemory(ABC):
    """
    Base class for all memory implementations.

    Responsibilities
    ----------------
    - Save memory to disk
    - Load memory from disk
    - Define a common interface
    - Allow child classes to define
      their own memory structure
    """

    def __init__(self, memory_path: str):

        self.memory_path = Path(memory_path)

        # Create parent folder if it doesn't exist
        self.memory_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # Save
    # =====================================================

    def save(self) -> None:
        """
        Saves the memory object to disk.
        """

        data = self.to_dict()

        with open(
            self.memory_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # Load
    # =====================================================

    def load(self) -> None:
        """
        Loads memory from disk.
        """

        if not self.memory_path.exists():
            return

        with open(
            self.memory_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        self.from_dict(data)

    # =====================================================
    # Abstract Methods
    # =====================================================

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memory into a dictionary.

        Child classes decide
        what data should be saved.
        """
        pass

    @abstractmethod
    def from_dict(
        self,
        data: Dict[str, Any]
    ) -> None:
        """
        Restore memory from a dictionary.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the memory.
        """
        pass