from dataclasses import dataclass, field
from typing import Any
print("planner_response loaded")

from app.planner.routes import Route


@dataclass
class PlannerResponse:
    """
    Output returned by the Planner.
    """

    route: Route
    confidence: float
    reason: str

    tool: str | None = None

    arguments: dict[str, Any] = field(default_factory=dict)