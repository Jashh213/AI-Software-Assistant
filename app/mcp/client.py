from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)


class MCPClient:
    """
    Represents a single MCP server connection.

    Responsibilities
    ----------------
    - Connect to one MCP server
    - List available tools
    - Execute tools
    - Disconnect cleanly

    NOTE:
    This class is async-only.
    It does NOT create event loops.
    The MCPRuntime owns the event loop.
    """

    def __init__(
        self,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None
    ):

        self.command = command
        self.args = args
        self.env = env or {}

        self.session: Optional[ClientSession] = None
        self.exit_stack: Optional[AsyncExitStack] = None

    # -----------------------------------------------------
    # Connect
    # -----------------------------------------------------

    async def connect(self):

        if self.session is not None:
            return

        self.exit_stack = AsyncExitStack()

        server = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env
        )

        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(server)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(
                read_stream,
                write_stream
            )
        )

        await self.session.initialize()

    # -----------------------------------------------------
    # Disconnect
    # -----------------------------------------------------

    async def disconnect(self):

        if self.exit_stack is not None:
            await self.exit_stack.aclose()

        self.exit_stack = None
        self.session = None

    # -----------------------------------------------------
    # List Tools
    # -----------------------------------------------------

    async def list_tools(self):

        if self.session is None:
            raise RuntimeError("MCP client is not connected.")

        response = await self.session.list_tools()

        return response.tools

    # -----------------------------------------------------
    # Execute Tool
    # -----------------------------------------------------

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ):

        if self.session is None:
            raise RuntimeError("MCP client is not connected.")

        response = await self.session.call_tool(
            tool_name,
            arguments
        )

        return response