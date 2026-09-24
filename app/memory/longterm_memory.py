from typing import Dict, Any

from app.memory.base_memory import BaseMemory


class LongTermMemory(BaseMemory):
    """
    Stores persistent user preferences and facts.

    Shared across every conversation.
    """

    def __init__(self):

        super().__init__(
            "storage/memory/long_term.json"
        )

        self.facts: Dict[str, Any] = {}

        self.load()

    # ==========================================
    # API
    # ==========================================

    def remember(
        self,
        key: str,
        value: Any
    ):

        self.facts[key] = value

        self.save()

    def recall(
        self,
        key: str,
        default=None
    ):

        return self.facts.get(
            key,
            default
        )

    def forget(
        self,
        key: str
    ):

        self.facts.pop(
            key,
            None
        )

        self.save()

    # ==========================================
    # BaseMemory
    # ==========================================

    def to_dict(self):

        return {

            "facts": self.facts

        }

    def from_dict(
        self,
        data: Dict[str, Any]
    ):

        self.facts = data.get(
            "facts",
            {}
        )

    def clear(self):

        self.facts = {}

        self.save()