import json
from app.llm.base import BaseLLM
from app.planner.routes import Route
from app.planner.planner_response import PlannerResponse
from app.tools.registry import ToolRegistry


class Planner:

    PLANNER_PROMPT = """
You are the Planning Agent of an AI Software Engineering Assistant.

Your ONLY job is to decide HOW a user request should be handled.

==================================================
AVAILABLE ROUTES
==================================================

GENERAL
--------
Choose GENERAL when the question is about:

- Programming concepts
- AI
- Data structures
- Algorithms
- Python
- Java
- Databases
- Web Development
- Anything NOT requiring the current repository.

Examples

"What is Python?"

"Explain OOP."

"What is Docker?"

--------------------------------------------------

RAG
---

Choose RAG when the question requires understanding
the CURRENT repository.

Examples

Explain this repository

Summarize this repository

Explain App.js

Explain Indexer class

How authentication works

Where is login implemented?

Which file creates the server?

--------------------------------------------------

TOOL
----

Choose TOOL ONLY when the user wants to execute an action.

Examples

List files

Search files

Read file

Create branch

Create issue

Delete file

Rename file

Write file

Commit changes

==================================================
AVAILABLE TOOLS
==================================================

<<TOOLS>>

==================================================
IMPORTANT RULES
==================================================

1. Return ONLY JSON.

2. Never use markdown.

3. Never explain your reasoning outside JSON.

4. Choose EXACTLY one route.

5. If GENERAL or RAG:

{
  "route":"GENERAL",
  "confidence":0.95,
  "reason":"...",
  "tool":null,
  "arguments":{}
}

or

{
  "route":"RAG",
  "confidence":0.95,
  "reason":"...",
  "tool":null,
  "arguments":{}
}

6. If TOOL:

- Choose ONE tool.

- ONLY generate arguments that exist in the tool schema.

- NEVER invent argument names.

- NEVER rename arguments.

- NEVER write

"Missing..."

or

"Unknown"

or

"Please provide..."

- If an argument value is unknown,
SIMPLY OMIT IT.

Example

User:
Create branch feature/login

Correct

{
  "route":"TOOL",
  "confidence":0.97,
  "reason":"Create Git branch",
  "tool":"create_branch",
  "arguments":{
      "branch":"feature/login"
  }
}

--------------------------------------------------

User:
Create issue

Correct

{
  "route":"TOOL",
  "confidence":0.96,
  "reason":"Create GitHub issue",
  "tool":"create_issue",
  "arguments":{}
}

--------------------------------------------------

The application automatically injects:

- repository path

- repository owner

- repository name

DO NOT generate them unless the user explicitly supplies different values.

==================================================
"""

    def __init__(
    self,
    registry: ToolRegistry,
    llm: BaseLLM,
    ):
        self.registry = registry
        self.llm = llm

    # =====================================================

    def plan(
        self,
        question: str,
    ) -> PlannerResponse:

        prompt = self._build_prompt(question)

        response = self.llm.generate(prompt)

        print("\n========== PLANNER OUTPUT ==========")
        print(response)
        print("====================================\n")

        return self._parse_response(response)

    # =====================================================

    def _build_prompt(
        self,
        question: str,
    ) -> str:

        tools = self._build_tool_section()

        system_prompt = self.PLANNER_PROMPT.replace(
            "<<TOOLS>>",
            tools,
        )

        return f"""
{system_prompt}

==================================================
USER REQUEST
==================================================

{question}
"""

    # =====================================================

    def _build_tool_section(self) -> str:

        tools = self.registry.list_tools()

        if not tools:

            return "No tools available."

        sections = []

        for tool in tools:

            schema = json.dumps(
                tool.input_schema,
                indent=2,
            )

            required = tool.input_schema.get(
                "required",
                [],
            )

            required_text = (
                ", ".join(required)
                if required
                else "None"
            )

            sections.append(
f"""
Tool Name
---------
{tool.name}

Description
-----------
{tool.description}

Required Arguments
------------------
{required_text}

Input Schema
------------
{schema}

=========================================
"""
            )

        return "\n".join(sections)
        # =====================================================

    def _clean_response(
    self,
    response: str,
) -> str:
        response = response.strip()
        # Remove markdown fences
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            response = response[start:end + 1]
        return response.strip()

    # =====================================================

    def _parse_response(
        self,
        response: str,
    ) -> PlannerResponse:

        response = self._clean_response(response)

        try:

            data = json.loads(response)

        except Exception as e:

            print("\nPlanner JSON Parse Error")
            print(e)
            print(response)

            return PlannerResponse(
                route=Route.GENERAL,
                confidence=0.0,
                reason="Planner returned invalid JSON.",
                tool=None,
                arguments={}
            )

        # -----------------------------------------
        # Route
        # -----------------------------------------

        route = str(
            data.get(
                "route",
                "GENERAL"
            )
        ).upper()

        try:

            route = Route(route)

        except Exception:

            route = Route.GENERAL

        # -----------------------------------------
        # Confidence
        # -----------------------------------------

        try:

            confidence = float(
                data.get(
                    "confidence",
                    1.0
                )
            )

        except Exception:

            confidence = 1.0

        # -----------------------------------------
        # Reason
        # -----------------------------------------

        reason = str(
            data.get(
                "reason",
                ""
            )
        )

        # -----------------------------------------
        # Tool
        # -----------------------------------------

        tool = data.get("tool")

        if tool is not None:

            tool = str(tool)

        # -----------------------------------------
        # Arguments
        # -----------------------------------------

        arguments = data.get(
            "arguments",
            {}
        )

        if not isinstance(arguments, dict):

            arguments = {}

        # -----------------------------------------
        # Remove null values
        # -----------------------------------------

        arguments = {
            k: v
            for k, v in arguments.items()
            if v is not None
        }

        # -----------------------------------------
        # Remove fake placeholders
        # -----------------------------------------

        cleaned = {}

        for key, value in arguments.items():

            if not isinstance(value, str):

                cleaned[key] = value
                continue

            lower = value.lower()

            if lower.startswith("missing"):
                continue

            if lower.startswith("unknown"):
                continue

            if lower.startswith("please provide"):
                continue

            cleaned[key] = value

        arguments = cleaned

        return PlannerResponse(
            route=route,
            confidence=confidence,
            reason=reason,
            tool=tool,
            arguments=arguments,
        )