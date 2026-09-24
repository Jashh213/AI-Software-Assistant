from typing import Dict, List

from app.tools.tool import Tool
from app.mcp.runtime import MCPRuntime


class ToolRegistry:
    """
    Stores and manages all tools exposed by MCP servers.

    Responsibilities
    ----------------
    - Discover tools from MCP servers
    - Register tools
    - Find tools
    - Group tools by server
    """

    def __init__(
        self,
        runtime: MCPRuntime
    ):

        self.runtime = runtime

        # tool_name -> Tool
        self._tools: Dict[str, Tool] = {}

    # =====================================================
    # Register tools from an MCP server
    # =====================================================

    def register_server(
        self,
        server_name: str
    ) -> None:

        mcp_tools = self.runtime.list_tools(
            server_name
        )

        for mcp_tool in mcp_tools:

            tool = Tool.from_mcp(
                tool=mcp_tool,
                server=server_name
            )

            self._tools[tool.name] = tool

    # =====================================================
    # Lookup
    # =====================================================

    def get_tool(
        self,
        tool_name: str
    ) -> Tool | None:

        return self._tools.get(tool_name)

    # =====================================================
    # List
    # =====================================================

    def list_tools(self) -> List[Tool]:

        return list(self._tools.values())

    # =====================================================
    # Filter
    # =====================================================

    def get_tools_by_server(
        self,
        server_name: str
    ) -> List[Tool]:

        return [

            tool

            for tool in self._tools.values()

            if tool.server == server_name

        ]

    # =====================================================
    # Exists
    # =====================================================

    def has_tool(
        self,
        tool_name: str
    ) -> bool:

        return tool_name in self._tools

    # =====================================================
    # Stats
    # =====================================================

    def __len__(self):

        return len(self._tools)