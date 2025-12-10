from __future__ import annotations

from dataclasses import dataclass

import pytest

from toddle_ops.helpers.agent_factory import (
    build_agent_from_archetype,
    prepare_standard_project,
)
from toddle_ops.models.agents import (
    AgentToolSpec,
    OrchestratorAgentArchetype,
    OrchestrationStyle,
    WorkerAgentArchetype,
)
from toddle_ops.models import StandardProject


@dataclass
class FakeAgent:
    name: str
    model: str
    instruction: str
    tools: list
    output_key: str | None = None


@dataclass
class FakeAgentTool:
    agent: object
    name: str
    input_keys: list | None = None
    output_keys: list | None = None
    summary: str | None = None


def test_build_worker_agent_with_injected_classes():
    archetype = WorkerAgentArchetype(
        name="Worker",
        summary="Does work",
        instruction="Do it",
        model="stub-model",
        output_key="result",
        capability="testing",
        default_tools=["path.to.tool"],
    )

    registry = {"path.to.tool": object()}

    agent = build_agent_from_archetype(
        archetype,
        llm_agent_cls=FakeAgent,
        agent_tool_cls=FakeAgentTool,
        model_resolver=lambda name: f"model:{name}",
        tool_resolver=lambda path: registry[path],
        agent_resolver=lambda path: registry[path],
    )

    assert isinstance(agent, FakeAgent)
    assert agent.model == "model:stub-model"
    assert agent.tools == [registry["path.to.tool"]]
    assert agent.output_key == "result"
    assert agent.archetype is archetype


def test_build_orchestrator_adds_managed_agent_tools():
    archetype = OrchestratorAgentArchetype(
        name="Orchestrator",
        summary="Coordinates",
        instruction="Coordinate",
        model="stub-model",
        orchestration_style=OrchestrationStyle.SEQUENTIAL,
        managed_agents=[
            AgentToolSpec(
                handle="child",
                agent_path="child.path",
                summary="child agent",
                input_keys=["in"],
                output_keys=["out"],
            )
        ],
    )

    child_agent = object()

    agent = build_agent_from_archetype(
        archetype,
        llm_agent_cls=FakeAgent,
        agent_tool_cls=FakeAgentTool,
        model_resolver=lambda name: f"model:{name}",
        tool_resolver=lambda path: object(),
        agent_resolver=lambda path: child_agent,
    )

    assert isinstance(agent.tools[0], FakeAgentTool)
    tool = agent.tools[0]
    assert tool.agent is child_agent
    assert tool.name == "child"
    assert tool.input_keys == ["in"]
    assert tool.output_keys == ["out"]
    assert tool.summary == "child agent"


def test_prepare_standard_project_accepts_dict():
    payload = {
        "name": "Test",
        "description": "Desc",
        "duration_minutes": 5,
        "instructions": "1. step",
        "materials": "Paper",
    }

    project = prepare_standard_project(payload)

    assert isinstance(project, StandardProject)
    assert project.name == "Test"
    assert project.duration_minutes == 5


def test_prepare_standard_project_rejects_invalid_type():
    with pytest.raises(TypeError):
        prepare_standard_project("invalid")
