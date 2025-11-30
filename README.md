
# Toddle Ops Kaggle x Google Capstone Project 👶

![gemini ai generated picture of toddlers sitting around a conference table working on a software project.](images/toddle-ops.png "Toddle Ops")

This is my capstone project for the 
[Agents Intensive - Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project).

[5-Day AI Agents Intensive Course with Google Course Page](https://www.kaggle.com/learn-guide/5-day-agents)


Toddle Ops is an Agentic Concierge service to help exhausted parents and
caregivers create, manage and ✨deploy✨ toddler projects they can do with
their little ones.

## The Pitch

- TODO - just spitballing
- problem/solution/value
    - hard to come up with projects on a whim
    - static content: 
        - doesn't know what materials we have on hand
        - doesn't know what projects we've done already
        - has alot of fluff 
- quick projects
- clear consistant formatting everytime
- memory and database

## Usage

```bash
adk run src/toddle_ops/app/
```

### Vertex App

**Deployment**

```bash
cd ./src/toddle_ops/agents/
adk deploy agent_engine --project=$GOOGLE_PROJECT_ID --region=$DEPLOYED_REGION vertex_agent --agent_engine_config_file=vertex_agent/.agent_engine_config.json
```

### MCP

- [sqlite mcp server](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)

## Setup

Install [gcloud](https://docs.cloud.google.com/sdk/docs/install-sdk#rpm)