from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from app.memory.base_memory import BaseMemory


class ConversationMemory(BaseMemory):
    """
    Stores the conversation for a single session.

    Each chat/session has its own JSON file.

    Example

    storage/
        memory/
            sessions/
                abcd123.json
    """

    def __init__(self, session_id: str):

        self.session_id = session_id

        memory_path = (
            f"storage/memory/sessions/{session_id}.json"
        )

        super().__init__(memory_path)

        self.messages: List[Dict[str, Any]] = []

        self.load()

    # =====================================================
    # Add Messages
    # =====================================================

    def add_user_message(
        self,
        content: str
    ) -> None:

        self.messages.append({

            "role": "user",

            "content": content,

            "timestamp": datetime.utcnow().isoformat()

        })

        self.save()

    def add_assistant_message(
        self,
        content: str,
        route: str | None = None,
        tool_used: str | None = None
    ) -> None:

        self.messages.append({

            "role": "assistant",

            "content": content,

            "timestamp": datetime.utcnow().isoformat(),

            "route": route,

            "tool_used": tool_used

        })

        self.save()

    # =====================================================
    # Read Messages
    # =====================================================

    def get_messages(self):

        return self.messages

    def get_recent_messages(
        self,
        limit: int = 10
    ):

        return self.messages[-limit:]

    # =====================================================
    # BaseMemory Methods
    # =====================================================

    def to_dict(self):

        return {

            "session_id": self.session_id,

            "messages": self.messages

        }

    def from_dict(self, data):

        self.session_id = data.get(
            "session_id",
            self.session_id
        )

        self.messages = data.get(
            "messages",
            []
        )

    def clear(self):

        self.messages = []

        self.save()