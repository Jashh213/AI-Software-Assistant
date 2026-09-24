from urllib.parse import urlparse

from app.llm.base import BaseLLM

from app.planner.planner import Planner
from app.planner.routes import Route

from app.repository.repository_manager import RepositoryManager

from app.rag.retriever import Retriever
from app.rag.rag_pipeline import RAGPipeline

from app.tools.registry import ToolRegistry
from app.tools.executor import ToolExecutor
from app.tools.validator import ToolValidator


class SoftwareEngineeringAgent:

    def __init__(
        self,
        planner: Planner,
        repository_manager: RepositoryManager,
        llm: BaseLLM,
        registry: ToolRegistry,
        executor: ToolExecutor,
    ):

        self.planner = planner
        self.repository_manager = repository_manager
        self.llm = llm
        self.registry = registry
        self.executor = executor

        self.validator = ToolValidator()

    # =====================================================
    # Helpers
    # =====================================================

    def _github_owner_repo(self, repository_url: str):

        path = urlparse(repository_url).path.strip("/")

        parts = path.split("/")

        owner = parts[0]
        repo = parts[1]

        return owner, repo

    # =====================================================
    # Public API
    # =====================================================

    def run(
        self,
        query: str,
        repository_url: str | None = None,
    ):

        # ----------------------------------------
        # Open Repository
        # ----------------------------------------

        if repository_url:

            self.repository_manager.open_repository(
                repository_url
            )

        # ----------------------------------------
        # Planner
        # ----------------------------------------

        decision = self.planner.plan(query)

        # ----------------------------------------
        # GENERAL
        # ----------------------------------------

        if decision.route == Route.GENERAL:

            return self.llm.generate(query)

        # ----------------------------------------
        # RAG
        # ----------------------------------------

        if decision.route == Route.RAG:

            project = self.repository_manager.get_current_project()

            if project is None:

                return (
                    "Please provide a GitHub repository URL "
                    "before asking repository questions."
                )

            retriever = Retriever(
                project.vector_store
            )

            rag = RAGPipeline(
                retriever=retriever,
                llm=self.llm,
            )

            return rag.answer(query)

        # ----------------------------------------
        # TOOL
        # ----------------------------------------

        if decision.route == Route.TOOL:

            tool = self.registry.get_tool(
                decision.tool
            )

            if tool is None:

                return (
                    f"Tool '{decision.tool}' was not found."
                )

            project = self.repository_manager.get_current_project()

            if project is None:

                return (
                    "Please open a repository first."
                )

            # ----------------------------------------
            # Inject Repository Context
            # ----------------------------------------

            args = decision.arguments.copy()

            # ======================================
            # Filesystem MCP
            # ======================================

            if tool.server == "filesystem":

                properties = tool.input_schema.get(
                    "properties",
                    {}
                )

                if "path" in properties:

                    repo_root = project.project_id

                    current_path = args.get("path")

                    if current_path in (
                        None,
                        "",
                        ".",
                    ):

                        args["path"] = repo_root

                    else:

                        current_path = current_path.lstrip("/\\")

                        args["path"] = (
                            f"{repo_root}/{current_path}"
                        )

            # ======================================
            # GitHub MCP
            # ======================================

            elif tool.server == "github":

                owner, repo = self._github_owner_repo(
                    project.repository_url
                )

                properties = tool.input_schema.get(
                    "properties",
                    {}
                )

                if "owner" in properties:

                    args.setdefault(
                        "owner",
                        owner
                    )

                if "repo" in properties:

                    args.setdefault(
                        "repo",
                        repo
                    )

            decision.arguments = args

            # ----------------------------------------
            # Validate Arguments
            # ----------------------------------------

            missing = self.validator.validate(
                tool,
                decision.arguments
            )

            if missing:

                fields = "\n".join(
                    f"• {field}"
                    for field in missing
                )

                return (
                    "I need some more information before I can "
                    "execute that tool.\n\n"
                    f"Please provide:\n{fields}"
                )

            # ----------------------------------------
            # Execute Tool
            # ----------------------------------------

            result = self.executor.execute(
                tool,
                decision.arguments,
            )

            # ----------------------------------------
            # Convert MCP Result
            # ----------------------------------------

            if hasattr(result, "content"):

                texts = []

                for item in result.content:

                    if hasattr(item, "text"):

                        texts.append(item.text)

                    else:

                        texts.append(str(item))

                return "\n".join(texts)

            return str(result)

        # ----------------------------------------

        return "Unknown planner route."