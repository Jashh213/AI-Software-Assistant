from pathlib import Path
from typing import Any

from app.mcp.client import MCPClient


class FilesystemClient:
    """
    Client for the Official Filesystem MCP Server.

    Responsibilities
    ----------------
    - Configure the Filesystem MCP Server
    - Provide easy-to-use filesystem methods
    - Hide MCP protocol details
    """

    def __init__(self, project_path: str):

        self.project_path = str(Path(project_path).resolve())

        self.client = MCPClient(
            command="npx",
            args=[
                "@modelcontextprotocol/server-filesystem",
                self.project_path
            ]
        )

    # =====================================================
    # Connection
    # =====================================================

    async def connect(self):

        await self.client.connect()

    async def disconnect(self):

        await self.client.disconnect()

    # =====================================================
    # Discovery
    # =====================================================

    async def list_tools(self):

        return await self.client.list_tools()

    # =====================================================
    # File Operations
    # =====================================================

    async def read_file(self, path: str):

        return await self.client.call_tool(
            tool_name="read_file",
            arguments={
                "path": path
            }
        )

    async def write_file(
        self,
        path: str,
        content: str
    ):

        return await self.client.call_tool(
            tool_name="write_file",
            arguments={
                "path": path,
                "content": content
            }
        )

    async def list_directory(
        self,
        path: str = "."
    ):

        return await self.client.call_tool(
            tool_name="list_directory",
            arguments={
                "path": path
            }
        )

    async def create_directory(
        self,
        path: str
    ):

        return await self.client.call_tool(
            tool_name="create_directory",
            arguments={
                "path": path
            }
        )

    async def delete_file(
        self,
        path: str
    ):

        return await self.client.call_tool(
            tool_name="delete_file",
            arguments={
                "path": path
            }
        )

    async def move_file(
        self,
        source: str,
        destination: str
    ):

        return await self.client.call_tool(
            tool_name="move_file",
            arguments={
                "source": source,
                "destination": destination
            }
        )

    async def get_file_info(
        self,
        path: str
    ):

        return await self.client.call_tool(
            tool_name="get_file_info",
            arguments={
                "path": path
            }
        )