from dotenv import load_dotenv
import os
from pathlib import Path
from app.llm.factory import LLMFactory
from app.planner.planner import Planner

from app.tools.registry import ToolRegistry
from app.tools.executor import ToolExecutor

from app.mcp.client import MCPClient
from app.mcp.runtime import MCPRuntime

from app.repository.git_manager import GitManager
from app.repository.repository_manager import RepositoryManager

from app.agent.software_engineering_agent import (
    SoftwareEngineeringAgent,
)


def bootstrap() -> SoftwareEngineeringAgent:
    """
    Bootstraps the AI Software Engineering Assistant.

    Responsibilities
    ----------------
    - Load environment variables
    - Create LLM
    - Create repository manager
    - Start MCP runtime
    - Register MCP clients
    - Discover tools
    - Create executor
    - Create planner
    - Create agent
    """

    print("=" * 60)
    print("Bootstrapping AI Software Engineering Assistant")
    print("=" * 60)

    # =====================================================
    # Environment
    # =====================================================

    load_dotenv()

    # =====================================================
    # LLM
    # =====================================================

    print("Creating LLM...")
    llm = LLMFactory.create()

    # =====================================================
    # Repository Manager
    # =====================================================

    print("Creating Repository Manager...")

    git_manager = GitManager()

    repository_manager = RepositoryManager(
        git_manager=git_manager
    )

    # =====================================================
    # MCP Runtime
    # =====================================================

    print("Starting MCP Runtime...")

    runtime = MCPRuntime()
    runtime.start()

    # =====================================================
    # MCP Clients
    # =====================================================

    print("Creating MCP Clients...")

    filesystem_client = MCPClient(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            str(Path("repositories").resolve())
        ]
    )

    github_client = MCPClient(
        command="npx",
        args=[
            "@modelcontextprotocol/server-github"
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")
        }
    )

    runtime.register_client(
        "filesystem",
        filesystem_client
    )

    runtime.register_client(
        "github",
        github_client
    )

    print("Connecting Filesystem MCP Server...")
    runtime.connect_client("filesystem")

    print("Connecting GitHub MCP Server...")
    runtime.connect_client("github")

    # =====================================================
    # Tool Registry
    # =====================================================

    print("Discovering MCP Tools...")

    registry = ToolRegistry(runtime)

    registry.register_server("filesystem")
    registry.register_server("github")

    print(f"Discovered {len(registry)} tools.")
    print("\n================ AVAILABLE TOOLS ================\n")
    for tool in registry.list_tools():
        print(f"{tool.server:<12} {tool.name}")
    print("\n=================================================\n")

    # =====================================================
    # Tool Executor
    # =====================================================

    print("Creating Tool Executor...")

    executor = ToolExecutor(runtime)

    # =====================================================
    # Planner
    # =====================================================

    print("Creating Planner...")

    planner = Planner(
    registry=registry,
    llm=llm,
    )
    # =====================================================
    # Agent
    # =====================================================

    print("Creating Software Engineering Agent...")

    agent = SoftwareEngineeringAgent(
        planner=planner,
        repository_manager=repository_manager,
        llm=llm,
        registry=registry,
        executor=executor,
    )

    print()
    print("=" * 60)
    print("Application Bootstrapped Successfully!")
    print("=" * 60)

    return agent