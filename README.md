
# Toddle Ops 👶

## Project Overview

![gemini ai generated picture of toddlers sitting around a conference table working on a software project.](images/toddle-ops.png "Toddle Ops")

This is the continuation of my capstone project for the 
[Agents Intensive - Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project).

[5-Day AI Agents Intensive Course with Google Course Page](https://www.kaggle.com/learn-guide/5-day-agents)

Toddle Ops is an Agentic Concierge service to help exhausted parents and
caregivers create, manage and ✨deploy✨ toddler projects they can do with
their little ones.

## The Pitch

Keeping a toddler happily occupied is a fulltime job, and the odds are, you 
already have a fulltime job. Sprinkle in some sleep depravation, and your
little one is likely to miss out on enriching activities.

> Enter ToddleOps Project Generation Agent

Lower the barrier of entry to safe, fun toddler activities to the absolute
floor with the ToddleOps Agent. It will provide projects, in a standard,
easy to follow format so *all* you have to do is conjure up every last drop
of willpower in your tired, aching body to actually *do* the project!

## Installation

### Standard Installation

```bash
# Clone repository from GitHub
git clone https://github.com/asenetcky/toddle-ops

# Enter Repository
cd toddle-ops

# Create .venv and install dependencies with uv
uv sync
```
### Requirements

- uv
    - Please refer to 
    [astral's website for up-to-date installation instructions.](https://docs.astral.sh/uv/getting-started/installation/)


## Usage

**uv**

This will run the agent wrapped in an app with logging, and local session and 
memory services.

```bash
uv run ./src/toddle_ops/local_app/main.py
```

**adk cli**

This will run the agent.

```bash
adk run src/toddle_ops/agents/root_agent
```

### Example Project Output

![image of terminal output describing a project for toddlers.](images/example-project.png "Toddle Ops Output")


### MCP Servers in Use

Implementation is not quite finished - but local project storage is planned
for the future.
- [sqlite mcp server](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)

### Vertex App

## Setup

Install [gcloud](https://docs.cloud.google.com/sdk/docs/install-sdk#rpm)

**Deployment**

```bash
cd ./src/toddle_ops/agents/
adk deploy agent_engine --project=$GOOGLE_PROJECT_ID --region=$DEPLOYED_REGION vertex_agent --agent_engine_config_file=vertex_agent/.agent_engine_config.json
```

