import asyncio
import threading
from typing import Any, Dict

from app.mcp.client import MCPClient


class MCPRuntime:
    """
    Production MCP Runtime.

    Responsibilities
    ----------------
    - Own one asyncio event loop
    - Run that loop forever in a background thread
    - Manage all MCP clients
    - Execute async MCP operations from synchronous code
    """

    def __init__(self):

        self.loop = asyncio.new_event_loop()

        self.thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )

        self.clients: Dict[str, MCPClient] = {}

        self.started = False

    # =====================================================
    # Background Loop
    # =====================================================

    def _run_loop(self):

        asyncio.set_event_loop(self.loop)

        self.loop.run_forever()

    # =====================================================
    # Start Runtime
    # =====================================================

    def start(self):
        if self.started:
            return
        self.thread.start()
        while not self.loop.is_running():
            pass
        self.started = True

    # =====================================================
    # Stop Runtime
    # =====================================================

    def stop(self):

        if not self.started:
            return

        # Disconnect every client
        for client in self.clients.values():

            asyncio.run_coroutine_threadsafe(
                client.disconnect(),
                self.loop
            ).result()

        self.loop.call_soon_threadsafe(
            self.loop.stop
            )
        self.thread.join()
        self.loop.close()
        self.started = False

    # =====================================================
    # Register Client
    # =====================================================

    def register_client(
        self,
        name: str,
        client: MCPClient
    ):

        self.clients[name] = client

    # =====================================================
    # Connect Client
    # =====================================================

    def connect_client(
        self,
        name: str
    ):

        client = self.clients[name]

        asyncio.run_coroutine_threadsafe(
            client.connect(),
            self.loop
        ).result()

    # =====================================================
    # List Tools
    # =====================================================

    def list_tools(
        self,
        name: str
    ):

        client = self.clients[name]

        future = asyncio.run_coroutine_threadsafe(
            client.list_tools(),
            self.loop
        )

        return future.result()

    # =====================================================
    # Call Tool
    # =====================================================

    def call_tool(
        self,
        client_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ):

        client = self.clients[client_name]

        future = asyncio.run_coroutine_threadsafe(
            client.call_tool(
                tool_name,
                arguments
            ),
            self.loop
        )

        return future.result()