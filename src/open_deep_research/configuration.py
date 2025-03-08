import os
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict, Optional

from langchain_core.runnables import RunnableConfig

DEFAULT_REPORT_STRUCTURE = """Use this structure to create a tactical implementation guide on the user-provided topic:

1. Introduction & Objective
   - Brief description of the task/challenge
   - Clear statement of goals and desired outcomes
   - Why this guide is valuable for implementation

2. Context & Background
   - Relevant information to understand the task
   - Key considerations for successful implementation
   - Foundational concepts and prerequisites

3. Implementation Approach
   - High-level strategy and methodology
   - Required resources, tools, and technologies
   - Planning considerations and preparation steps

4. Step-by-Step Implementation
   - Detailed procedural instructions with specific examples
   - Code snippets, templates, or sample assets (if applicable)
   - Practical tips and troubleshooting guidance
   - Common pitfalls to avoid during implementation

5. Resources & Examples
   - Curated list of tools, templates, and reference materials
   - Real-world implementation examples and case studies
   - Ready-to-use templates and implementation checklists

6. Evaluation & Next Steps
   - Success metrics and definition of done
   - Recommendations for iteration and improvement
   - Potential next steps to take after completing implementation"""


class SearchAPI(Enum):
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    EXA = "exa"
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    LINKUP = "linkup"


class PlannerProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"


class WriterProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"


@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the chatbot."""

    report_structure: str = (
        DEFAULT_REPORT_STRUCTURE  # Defaults to the default report structure
    )
    number_of_queries: int = 1  # Number of search queries to generate per iteration
    max_search_depth: int = 1  # Maximum number of reflection + search iterations
    planner_provider: PlannerProvider = (
        PlannerProvider.OPENAI
    )  # Defaults to Anthropic as provider
    planner_model: str = "gpt-4o-mini"  # Defaults to claude-3-7-sonnet-latest
    writer_provider: WriterProvider = (
        WriterProvider.OPENAI
    )  # Defaults to Anthropic as provider
    writer_model: str = "gpt-4o-mini"  # Defaults to claude-3-5-sonnet-latest
    search_api: SearchAPI = SearchAPI.TAVILY  # Default to TAVILY
    search_api_config: Optional[Dict[str, Any]] = None
    document_type: str = "technical report"  # Default document type
    objective: str = (
        "Provide comprehensive and detailed technical information"  # Default objective
    )
    # report_structure: str = (
    #     DEFAULT_REPORT_STRUCTURE  # Defaults to the default report structure
    # )
    # number_of_queries: int = 1  # Number of search queries to generate per iteration
    # max_search_depth: int = 1  # Maximum number of reflection + search iterations
    # planner_provider: PlannerProvider = (
    #     PlannerProvider.ANTHROPIC
    # )  # Defaults to Anthropic as provider
    # planner_model: str = (
    #     "claude-3-7-sonnet-latest"  # Defaults to claude-3-7-sonnet-latest
    # )
    # writer_provider: WriterProvider = (
    #     WriterProvider.ANTHROPIC
    # )  # Defaults to Anthropic as provider
    # writer_model: str = (
    #     "claude-3-5-sonnet-latest"  # Defaults to claude-3-5-sonnet-latest
    # )
    # search_api: SearchAPI = SearchAPI.TAVILY  # Default to TAVILY
    # search_api_config: Optional[Dict[str, Any]] = None
    # document_type: str = "technical report"  # Default document type
    # objective: str = (
    #     "Provide comprehensive and detailed technical information"  # Default objective
    # )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})
