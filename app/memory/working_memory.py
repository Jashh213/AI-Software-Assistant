from typing import Dict, Any, Optional

from app.memory.base_memory import BaseMemory


class WorkingMemory(BaseMemory):
    """
    Temporary in-memory state used during the
    current agent execution.

    This memory is NOT persisted to disk.
    """

    def __init__(self):

        # Dummy path because BaseMemory requires one.
        super().__init__("storage/memory/working.json")

        self.clear()

    # =====================================================
    # Working State
    # =====================================================

    def set_current_repository(
        self,
        repository: str
    ) -> None:

        self.current_repository = repository

    def set_current_branch(
        self,
        branch: str
    ) -> None:

        self.current_branch = branch

    def set_current_file(
        self,
        file_path: str
    ) -> None:

        self.current_file = file_path

    def set_current_function(
        self,
        function_name: str
    ) -> None:

        self.current_function = function_name

    def set_current_task(
        self,
        task: str
    ) -> None:

        self.current_task = task

    def set_current_plan(
        self,
        plan: Dict[str, Any]
    ) -> None:

        self.current_plan = plan

    def set_last_tool(
        self,
        tool_name: str
    ) -> None:

        self.last_tool = tool_name

    # =====================================================
    # Getters
    # =====================================================

    def get_current_repository(self) -> Optional[str]:
        return self.current_repository

    def get_current_branch(self) -> Optional[str]:
        return self.current_branch

    def get_current_file(self) -> Optional[str]:
        return self.current_file

    def get_current_function(self) -> Optional[str]:
        return self.current_function

    def get_current_task(self) -> Optional[str]:
        return self.current_task

    def get_current_plan(self):
        return self.current_plan

    def get_last_tool(self) -> Optional[str]:
        return self.last_tool

    # =====================================================
    # BaseMemory Overrides
    # =====================================================

    def save(self) -> None:
        """
        Working memory is temporary.

        Nothing is written to disk.
        """
        pass

    def load(self) -> None:
        """
        Working memory always starts empty.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:

        return {
            "current_repository": self.current_repository,
            "current_branch": self.current_branch,
            "current_file": self.current_file,
            "current_function": self.current_function,
            "current_task": self.current_task,
            "current_plan": self.current_plan,
            "last_tool": self.last_tool,
        }

    def from_dict(
        self,
        data: Dict[str, Any]
    ) -> None:

        self.current_repository = data.get("current_repository")
        self.current_branch = data.get("current_branch")
        self.current_file = data.get("current_file")
        self.current_function = data.get("current_function")
        self.current_task = data.get("current_task")
        self.current_plan = data.get("current_plan")
        self.last_tool = data.get("last_tool")

    def clear(self) -> None:

        self.current_repository = None
        self.current_branch = None
        self.current_file = None
        self.current_function = None
        self.current_task = None
        self.current_plan = None
        self.last_tool = None