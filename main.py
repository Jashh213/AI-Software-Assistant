import asyncio

from app.bootstrap import bootstrap


async def main():

    agent = await bootstrap()

    while True:

        query = input("\nYou: ")

        if query.lower() in {"exit", "quit"}:
            break

        repository_url = input(
            "Repository URL (leave empty for GENERAL questions): "
        ).strip()

        if repository_url == "":
            repository_url = None

        answer = await agent.run(

            query=query,

            repository_url=repository_url

        )

        print("\nAssistant:\n")

        print(answer)


if __name__ == "__main__":

    asyncio.run(main())