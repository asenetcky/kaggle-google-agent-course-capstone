"""Unit tests for the agent factory module."""

import pytest
from unittest.mock import patch, MagicMock
from google.adk.agents import LlmAgent
from google.genai import types

from toddle_ops.agents.factory import (
    create_agent,
    DEFAULT_MODEL,
    DEFAULT_SAFETY_SETTINGS,
)


class TestCreateAgentBasics:
    """Test basic agent creation functionality."""

    def test_create_agent_returns_llm_agent(self):
        """Factory should return an LlmAgent instance."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="You are a test agent.",
        )
        assert isinstance(agent, LlmAgent)

    def test_create_agent_sets_name(self):
        """Factory should set the agent name correctly."""
        agent = create_agent(
            name="MyTestAgent",
            description="A test agent",
            instruction="You are a test agent.",
        )
        assert agent.name == "MyTestAgent"

    def test_create_agent_sets_description(self):
        """Factory should set the agent description correctly."""
        agent = create_agent(
            name="TestAgent",
            description="A very descriptive description",
            instruction="You are a test agent.",
        )
        assert agent.description == "A very descriptive description"

    def test_create_agent_sets_instruction(self):
        """Factory should set the agent instruction correctly."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="You are a helpful test agent.",
        )
        assert agent.instruction == "You are a helpful test agent."


class TestCreateAgentModel:
    """Test model configuration in agent creation."""

    def test_create_agent_uses_default_model(self):
        """Factory should use the default model when none specified."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
        )
        # The model is a Gemini instance, check its model name
        assert agent.model.model == DEFAULT_MODEL

    def test_create_agent_accepts_custom_model(self):
        """Factory should accept a custom model name."""
        custom_model = "gemini-2.0-flash"
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            model=custom_model,
        )
        assert agent.model.model == custom_model


class TestCreateAgentOptionalParams:
    """Test optional parameter handling."""

    def test_create_agent_with_output_key(self):
        """Factory should set output_key when provided."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            output_key="my_output",
        )
        assert agent.output_key == "my_output"

    def test_create_agent_with_output_schema(self):
        """Factory should set output_schema when provided."""
        from pydantic import BaseModel

        class TestSchema(BaseModel):
            result: str

        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            output_schema=TestSchema,
        )
        assert agent.output_schema == TestSchema

    def test_create_agent_with_tools(self):
        """Factory should set tools when provided."""
        mock_tool = MagicMock()
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            tools=[mock_tool],
        )
        assert mock_tool in agent.tools

    def test_create_agent_with_sub_agents(self):
        """Factory should set sub_agents when provided."""
        sub_agent = create_agent(
            name="SubAgent",
            description="A sub agent",
            instruction="Sub agent instruction",
        )
        parent_agent = create_agent(
            name="ParentAgent",
            description="A parent agent",
            instruction="Parent instruction",
            sub_agents=[sub_agent],
        )
        assert sub_agent in parent_agent.sub_agents

    def test_create_agent_with_callbacks(self):
        """Factory should set before and after callbacks when provided."""
        before_cb = MagicMock()
        after_cb = MagicMock()

        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            before_agent_callback=before_cb,
            after_agent_callback=after_cb,
        )
        assert agent.before_agent_callback == before_cb
        assert agent.after_agent_callback == after_cb


class TestCreateAgentGenerateContentConfig:
    """Test generate_content_config building."""

    def test_create_agent_with_temperature(self):
        """Factory should build config when temperature is provided."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            temperature=0.5,
        )
        assert agent.generate_content_config is not None
        assert agent.generate_content_config.temperature == 0.5

    def test_create_agent_with_max_output_tokens(self):
        """Factory should build config when max_output_tokens is provided."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            max_output_tokens=2000,
        )
        assert agent.generate_content_config is not None
        assert agent.generate_content_config.max_output_tokens == 2000

    def test_create_agent_with_temperature_and_max_tokens(self):
        """Factory should combine temperature and max_output_tokens."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            temperature=0.8,
            max_output_tokens=1500,
        )
        assert agent.generate_content_config.temperature == 0.8
        assert agent.generate_content_config.max_output_tokens == 1500

    def test_create_agent_with_custom_safety_settings(self):
        """Factory should use custom safety settings when provided."""
        custom_safety = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            )
        ]
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            temperature=0.5,  # Need at least one param to trigger config build
            safety_settings=custom_safety,
        )
        assert agent.generate_content_config.safety_settings == custom_safety

    def test_create_agent_uses_default_safety_when_building_config(self):
        """Factory should use default safety settings when building config."""
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            temperature=0.5,
        )
        assert agent.generate_content_config.safety_settings == DEFAULT_SAFETY_SETTINGS

    def test_create_agent_with_full_generate_content_config(self):
        """Factory should accept a full GenerateContentConfig object."""
        custom_config = types.GenerateContentConfig(
            temperature=0.9,
            max_output_tokens=3000,
            top_p=0.95,
        )
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            generate_content_config=custom_config,
        )
        assert agent.generate_content_config == custom_config

    def test_full_config_overrides_individual_params(self):
        """Full GenerateContentConfig should take precedence over individual params."""
        custom_config = types.GenerateContentConfig(
            temperature=0.9,
            max_output_tokens=3000,
        )
        agent = create_agent(
            name="TestAgent",
            description="A test agent",
            instruction="Test instruction",
            temperature=0.1,  # Should be ignored
            max_output_tokens=100,  # Should be ignored
            generate_content_config=custom_config,
        )
        assert agent.generate_content_config.temperature == 0.9
        assert agent.generate_content_config.max_output_tokens == 3000


class TestDefaultConstants:
    """Test default constant values."""

    def test_default_model_value(self):
        """DEFAULT_MODEL should be set to expected value."""
        assert DEFAULT_MODEL == "gemini-2.5-flash-lite"

    def test_default_safety_settings_blocks_dangerous_content(self):
        """DEFAULT_SAFETY_SETTINGS should block dangerous content."""
        assert len(DEFAULT_SAFETY_SETTINGS) == 1
        setting = DEFAULT_SAFETY_SETTINGS[0]
        assert setting.category == types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
        assert setting.threshold == types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
