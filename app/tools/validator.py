from typing import Dict, Any, List

from app.tools.tool import Tool


class ToolValidator:
    """
    Validates tool arguments before execution.

    Responsibilities
    ----------------
    - Read the MCP input schema
    - Determine required fields
    - Detect missing arguments
    """

    def validate(
        self,
        tool: Tool,
        arguments: Dict[str, Any]
    ) -> List[str]:

        schema = tool.input_schema or {}

        required_fields = schema.get("required", [])

        missing = []

        for field in required_fields:

            value = arguments.get(field)

            if value is None:
                missing.append(field)
                continue

            if isinstance(value, str):

                value = value.strip()

                if not value:
                    missing.append(field)
                    continue

                # Planner sometimes generates:
                # "Missing: Please provide ..."
                if value.lower().startswith("missing"):
                    missing.append(field)

        return missing