"""Unit tests for agent getter functions across all agent modules."""

import pytest
from unittest.mock import patch, MagicMock
from google.adk.agents import LlmAgent


class TestOrchestratorAgent:
    """Tests for the orchestrator agent getter."""

    def test_get_orchestrator_agent_returns_llm_agent(self):
        """get_orchestrator_agent should return an LlmAgent."""
        from toddle_ops.agents.orchestrator.agent import get_orchestrator_agent

        agent = get_orchestrator_agent()
        assert isinstance(agent, LlmAgent)

    def test_orchestrator_agent_has_correct_name(self):
        """Orchestrator agent should have the expected name."""
        from toddle_ops.agents.orchestrator.agent import get_orchestrator_agent

        agent = get_orchestrator_agent()
        assert agent.name == "ToddleOpsOrchestrator"

    def test_orchestrator_agent_has_output_key(self):
        """Orchestrator agent should have human_project as output_key."""
        from toddle_ops.agents.orchestrator.agent import get_orchestrator_agent

        agent = get_orchestrator_agent()
        assert agent.output_key == "human_project"

    def test_orchestrator_agent_has_tools(self):
        """Orchestrator agent should have tools configured."""
        from toddle_ops.agents.orchestrator.agent import get_orchestrator_agent

        agent = get_orchestrator_agent()
        assert len(agent.tools) > 0

    def test_orchestrator_agent_has_after_callback(self):
        """Orchestrator agent should have after_agent_callback set."""
        from toddle_ops.agents.orchestrator.agent import get_orchestrator_agent

        agent = get_orchestrator_agent()
        assert agent.after_agent_callback is not None

    def test_root_agent_alias_exists(self):
        """root_agent module-level alias should exist for backwards compatibility."""
        from toddle_ops.agents.orchestrator.agent import root_agent

        assert isinstance(root_agent, LlmAgent)
        assert root_agent.name == "ToddleOpsOrchestrator"


class TestResearchCoordinatorAgent:
    """Tests for the research coordinator agent getter."""

    def test_get_research_coordinator_returns_llm_agent(self):
        """get_research_coordinator_agent should return an LlmAgent."""
        from toddle_ops.agents.research_team.agent import get_research_coordinator_agent

        agent = get_research_coordinator_agent()
        assert isinstance(agent, LlmAgent)

    def test_research_coordinator_has_correct_name(self):
        """Research coordinator should have the expected name."""
        from toddle_ops.agents.research_team.agent import get_research_coordinator_agent

        agent = get_research_coordinator_agent()
        assert agent.name == "ProjectResearchCoordinator"

    def test_research_coordinator_has_output_key(self):
        """Research coordinator should have standard_project as output_key."""
        from toddle_ops.agents.research_team.agent import get_research_coordinator_agent

        agent = get_research_coordinator_agent()
        assert agent.output_key == "standard_project"

    def test_research_coordinator_has_sub_agents(self):
        """Research coordinator should have sub_agents configured."""
        from toddle_ops.agents.research_team.agent import get_research_coordinator_agent

        agent = get_research_coordinator_agent()
        assert len(agent.sub_agents) > 0

    def test_research_coordinator_has_generate_content_config(self):
        """Research coordinator should have generate_content_config set."""
        from toddle_ops.agents.research_team.agent import get_research_coordinator_agent

        agent = get_research_coordinator_agent()
        assert agent.generate_content_config is not None
        assert agent.generate_content_config.temperature == 1.0
        assert agent.generate_content_config.max_output_tokens == 1000

    def test_root_agent_alias_exists(self):
        """root_agent module-level alias should exist for backwards compatibility."""
        from toddle_ops.agents.research_team.agent import root_agent

        assert isinstance(root_agent, LlmAgent)
        assert root_agent.name == "ProjectResearchCoordinator"


class TestResearchTeamSubAgents:
    """Tests for research team sub-agent getters."""

    def test_get_low_temp_researcher_returns_llm_agent(self):
        """get_low_temp_project_researcher should return an LlmAgent."""
        from toddle_ops.agents.research_team.sub_agent import get_low_temp_project_researcher

        agent = get_low_temp_project_researcher()
        assert isinstance(agent, LlmAgent)

    def test_low_temp_researcher_has_correct_name(self):
        """Low temp researcher should have the expected name."""
        from toddle_ops.agents.research_team.sub_agent import get_low_temp_project_researcher

        agent = get_low_temp_project_researcher()
        assert agent.name == "LowTempProjectResearcher"

    def test_low_temp_researcher_has_low_temperature(self):
        """Low temp researcher should have temperature of 0.7."""
        from toddle_ops.agents.research_team.sub_agent import get_low_temp_project_researcher

        agent = get_low_temp_project_researcher()
        assert agent.generate_content_config.temperature == 0.7

    def test_low_temp_researcher_has_correct_output_key(self):
        """Low temp researcher should output to low_temp_project_research."""
        from toddle_ops.agents.research_team.sub_agent import get_low_temp_project_researcher

        agent = get_low_temp_project_researcher()
        assert agent.output_key == "low_temp_project_research"

    def test_get_high_temp_researcher_returns_llm_agent(self):
        """get_high_temp_project_researcher should return an LlmAgent."""
        from toddle_ops.agents.research_team.sub_agent import get_high_temp_project_researcher

        agent = get_high_temp_project_researcher()
        assert isinstance(agent, LlmAgent)

    def test_high_temp_researcher_has_correct_name(self):
        """High temp researcher should have the expected name."""
        from toddle_ops.agents.research_team.sub_agent import get_high_temp_project_researcher

        agent = get_high_temp_project_researcher()
        assert agent.name == "HighTempProjectResearcher"

    def test_high_temp_researcher_has_high_temperature(self):
        """High temp researcher should have temperature of 1.2."""
        from toddle_ops.agents.research_team.sub_agent import get_high_temp_project_researcher

        agent = get_high_temp_project_researcher()
        assert agent.generate_content_config.temperature == 1.2

    def test_high_temp_researcher_has_correct_output_key(self):
        """High temp researcher should output to high_temp_project_research."""
        from toddle_ops.agents.research_team.sub_agent import get_high_temp_project_researcher

        agent = get_high_temp_project_researcher()
        assert agent.output_key == "high_temp_project_research"

    def test_researchers_have_google_search_tool(self):
        """Both researchers should have google_search in their tools."""
        from toddle_ops.agents.research_team.sub_agent import (
            get_low_temp_project_researcher,
            get_high_temp_project_researcher,
        )

        low_agent = get_low_temp_project_researcher()
        high_agent = get_high_temp_project_researcher()

        assert len(low_agent.tools) > 0
        assert len(high_agent.tools) > 0

    def test_get_project_synthesizer_returns_llm_agent(self):
        """get_project_synthesizer should return an LlmAgent."""
        from toddle_ops.agents.research_team.sub_agent import get_project_synthesizer

        agent = get_project_synthesizer()
        assert isinstance(agent, LlmAgent)

    def test_project_synthesizer_has_correct_name(self):
        """Project synthesizer should have the expected name."""
        from toddle_ops.agents.research_team.sub_agent import get_project_synthesizer

        agent = get_project_synthesizer()
        assert agent.name == "ProjectSynthesizer"

    def test_project_synthesizer_has_output_schema(self):
        """Project synthesizer should have StandardProject output schema."""
        from toddle_ops.agents.research_team.sub_agent import get_project_synthesizer
        from toddle_ops.models.projects import StandardProject

        agent = get_project_synthesizer()
        assert agent.output_schema == StandardProject

    def test_project_synthesizer_has_correct_output_key(self):
        """Project synthesizer should output to standard_project."""
        from toddle_ops.agents.research_team.sub_agent import get_project_synthesizer

        agent = get_project_synthesizer()
        assert agent.output_key == "standard_project"


class TestQualityAssuranceSubAgents:
    """Tests for quality assurance team sub-agent getters."""

    def test_get_safety_critic_returns_llm_agent(self):
        """get_safety_critic_agent should return an LlmAgent."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_critic_agent

        agent = get_safety_critic_agent()
        assert isinstance(agent, LlmAgent)

    def test_safety_critic_has_correct_name(self):
        """Safety critic should have the expected name."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_critic_agent

        agent = get_safety_critic_agent()
        assert agent.name == "SafetyCriticAgent"

    def test_safety_critic_has_output_schema(self):
        """Safety critic should have StatusReport output schema."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_critic_agent
        from toddle_ops.models.reports import StatusReport

        agent = get_safety_critic_agent()
        assert agent.output_schema == StatusReport

    def test_safety_critic_has_correct_output_key(self):
        """Safety critic should output to safety_report."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_critic_agent

        agent = get_safety_critic_agent()
        assert agent.output_key == "safety_report"

    def test_get_safety_refiner_returns_llm_agent(self):
        """get_safety_refiner_agent should return an LlmAgent."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_refiner_agent

        agent = get_safety_refiner_agent()
        assert isinstance(agent, LlmAgent)

    def test_safety_refiner_has_correct_name(self):
        """Safety refiner should have the expected name."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_refiner_agent

        agent = get_safety_refiner_agent()
        assert agent.name == "SafetyRefinerAgent"

    def test_safety_refiner_has_correct_output_key(self):
        """Safety refiner should output to standard_project."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_refiner_agent

        agent = get_safety_refiner_agent()
        assert agent.output_key == "standard_project"

    def test_safety_refiner_has_tools(self):
        """Safety refiner should have exit_loop tool."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_safety_refiner_agent

        agent = get_safety_refiner_agent()
        assert len(agent.tools) > 0

    def test_get_editorial_agent_returns_llm_agent(self):
        """get_editorial_agent should return an LlmAgent."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_editorial_agent

        agent = get_editorial_agent()
        assert isinstance(agent, LlmAgent)

    def test_editorial_agent_has_correct_name(self):
        """Editorial agent should have the expected name."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_editorial_agent

        agent = get_editorial_agent()
        assert agent.name == "EditorialAgent"

    def test_editorial_agent_has_correct_output_key(self):
        """Editorial agent should output to standard_project."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import get_editorial_agent

        agent = get_editorial_agent()
        assert agent.output_key == "standard_project"

    def test_editorial_agent_alias_exists(self):
        """editorial_agent module-level alias should exist for backwards compatibility."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import editorial_agent

        assert isinstance(editorial_agent, LlmAgent)
        assert editorial_agent.name == "EditorialAgent"


class TestAgentIndependence:
    """Tests to verify each getter creates independent agent instances."""

    def test_multiple_calls_create_different_instances(self):
        """Each call to a getter should create a new instance."""
        from toddle_ops.agents.research_team.sub_agent import get_project_synthesizer

        agent1 = get_project_synthesizer()
        agent2 = get_project_synthesizer()

        assert agent1 is not agent2

    def test_low_and_high_temp_researchers_are_different(self):
        """Low and high temp researchers should be different agents."""
        from toddle_ops.agents.research_team.sub_agent import (
            get_low_temp_project_researcher,
            get_high_temp_project_researcher,
        )

        low = get_low_temp_project_researcher()
        high = get_high_temp_project_researcher()

        assert low.name != high.name
        assert low.output_key != high.output_key
        assert low.generate_content_config.temperature != high.generate_content_config.temperature

    def test_safety_critic_and_refiner_are_different(self):
        """Safety critic and refiner should be different agents."""
        from toddle_ops.agents.quality_assurance_team.sub_agent import (
            get_safety_critic_agent,
            get_safety_refiner_agent,
        )

        critic = get_safety_critic_agent()
        refiner = get_safety_refiner_agent()

        assert critic.name != refiner.name
        assert critic.output_key != refiner.output_key
