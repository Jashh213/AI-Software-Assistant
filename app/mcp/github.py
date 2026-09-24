from app.config.settings import GITHUB_TOKEN
from app.mcp.client import MCPClient


class GitHubClient:
    """
    Wrapper around the Official GitHub MCP Server.

    Responsibilities
    ----------------
    - Configure the GitHub MCP Server
    - Expose GitHub-specific methods
    - Hide MCP protocol details
    """

    def __init__(self):

        self.client = MCPClient(
            command="npx",
            args=[
                "@modelcontextprotocol/server-github"
            ],
            env={
                "GITHUB_TOKEN": GITHUB_TOKEN
            }
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
    # Repository
    # =====================================================

    async def search_repositories(
        self,
        query: str,
        page: int = 1
    ):
        return await self.client.call_tool(
            "search_repositories",
            {
                "query": query,
                "page": page
            }
        )

    async def create_repository(
        self,
        name: str,
        description: str = "",
        private: bool = False
    ):
        return await self.client.call_tool(
            "create_repository",
            {
                "name": name,
                "description": description,
                "private": private
            }
        )

    async def fork_repository(
        self,
        owner: str,
        repo: str
    ):
        return await self.client.call_tool(
            "fork_repository",
            {
                "owner": owner,
                "repo": repo
            }
        )

    # =====================================================
    # Files
    # =====================================================

    async def get_file_contents(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str = "main"
    ):
        return await self.client.call_tool(
            "get_file_contents",
            {
                "owner": owner,
                "repo": repo,
                "path": path,
                "branch": branch
            }
        )

    async def create_or_update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str = "main"
    ):
        return await self.client.call_tool(
            "create_or_update_file",
            {
                "owner": owner,
                "repo": repo,
                "path": path,
                "content": content,
                "message": message,
                "branch": branch
            }
        )

    async def push_files(
        self,
        owner: str,
        repo: str,
        branch: str,
        files: list,
        message: str
    ):
        return await self.client.call_tool(
            "push_files",
            {
                "owner": owner,
                "repo": repo,
                "branch": branch,
                "files": files,
                "message": message
            }
        )

    # =====================================================
    # Branch
    # =====================================================

    async def create_branch(
        self,
        owner: str,
        repo: str,
        branch: str,
        from_branch: str = "main"
    ):
        return await self.client.call_tool(
            "create_branch",
            {
                "owner": owner,
                "repo": repo,
                "branch": branch,
                "from_branch": from_branch
            }
        )

    async def list_commits(
        self,
        owner: str,
        repo: str,
        branch: str = "main"
    ):
        return await self.client.call_tool(
            "list_commits",
            {
                "owner": owner,
                "repo": repo,
                "branch": branch
            }
        )

    # =====================================================
    # Issues
    # =====================================================

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str
    ):
        return await self.client.call_tool(
            "create_issue",
            {
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body
            }
        )

    async def list_issues(
        self,
        owner: str,
        repo: str
    ):
        return await self.client.call_tool(
            "list_issues",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def update_issue(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        body: str
    ):
        return await self.client.call_tool(
            "update_issue",
            {
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
                "body": body
            }
        )

    async def add_issue_comment(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        body: str
    ):
        return await self.client.call_tool(
            "add_issue_comment",
            {
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
                "body": body
            }
        )

    # =====================================================
    # Pull Requests
    # =====================================================

    async def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str
    ):
        return await self.client.call_tool(
            "create_pull_request",
            {
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body,
                "head": head,
                "base": base
            }
        )

    async def list_pull_requests(
        self,
        owner: str,
        repo: str
    ):
        return await self.client.call_tool(
            "list_pull_requests",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def merge_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int
    ):
        return await self.client.call_tool(
            "merge_pull_request",
            {
                "owner": owner,
                "repo": repo,
                "pull_number": pull_number
            }
        )

    # =====================================================
    # Search
    # =====================================================

    async def search_code(
        self,
        query: str
    ):
        return await self.client.call_tool(
            "search_code",
            {
                "query": query
            }
        )

    async def search_users(
        self,
        query: str
    ):
        return await self.client.call_tool(
            "search_users",
            {
                "query": query
            }
        )

    async def search_issues(
        self,
        query: str
    ):
        return await self.client.call_tool(
            "search_issues",
            {
                "query": query
            }
        )