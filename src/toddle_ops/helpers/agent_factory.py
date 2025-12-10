"""Helpers to turn agent archetypes into runnable agents or test doubles."""

from __future__ import annotations

import importlib
from typing import Any, Callable, Iterable, Sequence

from toddle_ops.models import StandardProject
from toddle_ops.models.agents import AgentArchetype, AgentToolSpec, AgentType

ModelResolver = Callable[[str], Any]
ToolResolver = Callable[[str], Any]
AgentResolver = Callable[[str], Any]


def resolve_dotted_path(path: str) -> Any:
    """Import and return an object by dotted path."""

    module_path, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)


def prepare_standard_project(payload: StandardProject | dict[str, Any]) -> StandardProject:
    """Normalize either a dict payload or StandardProject into StandardProject.

    Useful for unit tests that want to inject simple dictionaries without
    constructing the full model ahead of time.
    """

    if isinstance(payload, StandardProject):
        return payload
    if isinstance(payload, dict):
        return StandardProject(**payload)
    msg = "payload must be a StandardProject or dict"
    raise TypeError(msg)


def _resolve_tools(paths: Iterable[str], tool_resolver: ToolResolver) -> list[Any]:
    return [tool_resolver(path) for path in paths]


def _build_managed_agent_tools(
    specs: Sequence[AgentToolSpec],
    agent_tool_cls: type,
    agent_resolver: AgentResolver,
) -> list[Any]:
    tools: list[Any] = []
    for spec in specs:
        managed_agent = agent_resolver(spec.agent_path)
        tool = agent_tool_cls(managed_agent, name=spec.handle)
        tool.input_keys = list(spec.input_keys)
        tool.output_keys = list(spec.output_keys)
        tool.summary = spec.summary
        tools.append(tool)
    return tools


def build_agent_from_archetype(
    archetype: AgentArchetype,
    *,
    llm_agent_cls: type | None = None,
    agent_tool_cls: type | None = None,
    model_resolver: ModelResolver | None = None,
    tool_resolver: ToolResolver | None = None,
    agent_resolver: AgentResolver | None = None,
) -> Any:
    """Instantiate an agent instance from an archetype.

    Defaults use google-adk classes, but tests can inject lightweight fakes
    to avoid network calls and heavy imports.
    """

    # Deferred imports so unit tests can stub everything out.
    if llm_agent_cls is None:
        from google.adk.agents import LlmAgent as llm_agent_cls  # type: ignore
    if agent_tool_cls is None:
        from google.adk.tools import AgentTool as agent_tool_cls  # type: ignore
    if model_resolver is None:
        from google.adk.models.google_llm import Gemini
        from google.adk.models.lite_llm import LiteLlm

        def model_resolver(name: str):  # type: ignore
            # Prefer Gemini when string starts with gemini-, else fall back to LiteLlm.
            if name.startswith("gemini"):
                return Gemini(model=name)
            return LiteLlm(model=name)

    if tool_resolver is None:
        tool_resolver = resolve_dotted_path
    if agent_resolver is None:
        agent_resolver = resolve_dotted_path

    model = model_resolver(archetype.model)

    tools: list[Any] = _resolve_tools(archetype.default_tools, tool_resolver)

    managed_specs = getattr(archetype, "managed_agents", [])

    if archetype.type == AgentType.ORCHESTRATOR and managed_specs:
        # Build AgentTools for managed agents and attach them to an LLM agent or
        # directly return a SequentialAgent when no tools are needed.
        managed_tools = _build_managed_agent_tools(
            managed_specs, agent_tool_cls, agent_resolver  # type: ignore[arg-type]
        )
        tools.extend(managed_tools)

        agent = llm_agent_cls(
            name=archetype.name,
            model=model,
            instruction=archetype.instruction,
            tools=tools,
            output_key=archetype.output_key,
        )
    else:
        agent = llm_agent_cls(
            name=archetype.name,
            model=model,
            instruction=archetype.instruction,
            tools=tools,
            output_key=archetype.output_key,
        )

    # Attach archetype metadata for debugging and tests.
    setattr(agent, "archetype", archetype)
    return agent


__all__ = [
    "build_agent_from_archetype",
    "prepare_standard_project",
    "resolve_dotted_path",
]
