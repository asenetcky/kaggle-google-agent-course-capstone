"""Pydantic archetype instances for known agents.

These archetypes capture intent, inputs/outputs, and managed agent wiring
without importing google-adk at definition time. They enable light-weight
unit tests that avoid starting full pipelines or invoking LLMs.
"""

from toddle_ops.models.agents import (
    AgentToolSpec,
    OrchestratorAgentArchetype,
    OrchestrationStyle,
    WorkerAgentArchetype,
)

# Worker archetypes
project_formatter_archetype = WorkerAgentArchetype(
    name="ProjectFormatter",
    summary="Formats a StandardProject into reader-friendly markdown.",
    instruction="""You format a StandardProject into a concise markdown handout
    with sections for name, description, duration, materials, and instructions.""",
    model="gemini-2.5-flash-lite",
    output_key="human_project",
    capability="formatting",
    accepted_inputs=["standard_project"],
    produces=["human_project"],
)

project_database_archetype = WorkerAgentArchetype(
    name="ProjectDatabaseAgent",
    summary="Stores finalized projects in SQLite via MCP.",
    instruction="""You save a finalized toddler project to SQLite using the mcp
    sqlite server. Always ask for permission before modifying the database.""",
    model="gemini-2.5-flash-lite",
    output_key="database_queue",
    capability="persistence",
    accepted_inputs=["final_project"],
    produces=["database_queue"],
    helper_tools=["toddle_ops.mcp.sqlite.mcp_sqlite_server"],
)

# Orchestrator archetypes
craft_research_pipeline_archetype = OrchestratorAgentArchetype(
    name="CraftResearchPipeline",
    summary="Researches toddler-safe crafts and synthesizes a StandardProject.",
    instruction="""Research a toddler-safe craft with google search, then
    synthesize a single StandardProject from the findings.""",
    model="gemini-2.5-flash-lite",
    orchestration_style=OrchestrationStyle.SEQUENTIAL,
    managed_agents=[
        AgentToolSpec(
            handle="project_researcher",
            agent_path="toddle_ops.agents.craft_research_team.agent.project_researcher",
            summary="Use Google search to gather candidate toddler crafts.",
            output_keys=["project_research"],
        ),
        AgentToolSpec(
            handle="project_synthesizer",
            agent_path="toddle_ops.agents.craft_research_team.agent.project_synthesizer",
            summary="Turn research notes into a structured StandardProject.",
            input_keys=["project_research"],
            output_keys=["standard_project"],
        ),
    ],
)

quality_assurance_pipeline_archetype = OrchestratorAgentArchetype(
    name="QualityAssurancePipeline",
    summary="Runs safety refinement loop then editorial polish for projects.",
    instruction="""Iteratively critique toddler project safety, refine until
    approved, then edit for clarity and correctness.""",
    model="gemini-2.5-flash-lite",
    orchestration_style=OrchestrationStyle.SEQUENTIAL,
    managed_agents=[
        AgentToolSpec(
            handle="safety_refinement_loop",
            agent_path="toddle_ops.agents.quality_assurance_team.agent.safety_refinement_loop",
            summary="Loop until the project is safety-approved.",
            input_keys=["standard_project"],
            output_keys=["standard_project", "safety_report"],
        ),
        AgentToolSpec(
            handle="editorial_agent",
            agent_path="toddle_ops.agents.quality_assurance_team.agent.editorial_agent",
            summary="Polish instructions and wording after safety approval.",
            input_keys=["standard_project"],
            output_keys=["standard_project"],
        ),
    ],
)

project_pipeline_archetype = OrchestratorAgentArchetype(
    name="ToddleOpsSequence",
    summary="Full pipeline: research, safety/QA, then formatting for humans.",
    instruction="""Generate a project via research, refine for safety, and
    format for a caregiver-readable handout.""",
    model="gemini-2.5-flash-lite",
    orchestration_style=OrchestrationStyle.SEQUENTIAL,
    managed_agents=[
        AgentToolSpec(
            handle="craft_research",
            agent_path="toddle_ops.agents.craft_research_team.agent.root_agent",
            summary="Find and synthesize a draft StandardProject.",
            output_keys=["standard_project"],
        ),
        AgentToolSpec(
            handle="quality_assurance",
            agent_path="toddle_ops.agents.quality_assurance_team.agent.root_agent",
            summary="Refine project for safety and clarity.",
            input_keys=["standard_project"],
            output_keys=["standard_project"],
        ),
        AgentToolSpec(
            handle="project_formatter",
            agent_path="toddle_ops.agents.root_agent.project_formatter",
            summary="Format the final project into markdown output.",
            input_keys=["standard_project"],
            output_keys=["human_project"],
        ),
    ],
)

root_agent_archetype = OrchestratorAgentArchetype(
    name="ToddleOpsRoot",
    summary="Entry-point orchestrator that delegates to the full pipeline.",
    instruction="""Use the ToddleOpsSequence tool to satisfy user project
    requests. Do not attempt to author the project yourself.""",
    model="ollama_chat/mistral-nemo:12b",
    orchestration_style=OrchestrationStyle.SEQUENTIAL,
    managed_agents=[
        AgentToolSpec(
            handle="project_pipeline",
            agent_path="toddle_ops.agents.root_agent.project_pipeline",
            summary="Run the end-to-end project generation pipeline.",
            output_keys=["human_project"],
        ),
    ],
    default_tools=["google.adk.tools.preload_memory"],
    output_key="human_project",
)

__all__ = [
    "project_formatter_archetype",
    "project_database_archetype",
    "craft_research_pipeline_archetype",
    "quality_assurance_pipeline_archetype",
    "project_pipeline_archetype",
    "root_agent_archetype",
]
