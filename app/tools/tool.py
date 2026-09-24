from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(slots=True)
class Tool:
    """
    Represents a tool exposed by an MCP server.
    """

    name: str

    description: str

    server: str

    input_schema: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        return {

            "name": self.name,

            "description": self.description,

            "server": self.server,

            "input_schema": self.input_schema,

            "metadata": self.metadata

        }

    @classmethod
    def from_mcp(
        cls,
        tool,
        server: str
    ):

        return cls(

            name=tool.name,

            description=tool.description,

            server=server,

            input_schema=getattr(
                tool,
                "inputSchema",
                {}
            ),

            metadata={}

        )