from typing import Any, Dict

from app.tools.tool import Tool
from app.mcp.runtime import MCPRuntime


class ToolExecutor:
    """
    Executes MCP tools through the shared MCP runtime.

    Responsibilities
    ----------------
    - Receive a Tool object
    - Delegate execution to MCPRuntime
    """

    def __init__(
        self,
        runtime: MCPRuntime
    ):

        self.runtime = runtime

    # =====================================================
    # Execute Tool
    # =====================================================

    def execute(
        self,
        tool: Tool,
        arguments: Dict[str, Any]
    ) -> Any:

        return self.runtime.call_tool(
            client_name=tool.server,
            tool_name=tool.name,
            arguments=arguments
        )