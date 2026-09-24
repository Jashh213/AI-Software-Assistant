import asyncio
from pprint import pprint

from app.config.settings import GITHUB_TOKEN
from app.mcp.client import MCPClient


async def main():

    client = MCPClient(
        command="npx",
        args=[
            "@modelcontextprotocol/server-github"
        ],
        env={
            "GITHUB_TOKEN": GITHUB_TOKEN
        }
    )

    await client.connect()

    tools = await client.list_tools()

    for tool in tools:

        print("=" * 80)

        pprint(tool)

        print()

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())