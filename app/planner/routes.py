from enum import Enum


class Route(str, Enum):
    """
    All execution routes supported by the assistant.
    """

    GENERAL = "GENERAL"

    RAG = "RAG"

    TOOL = "TOOL"