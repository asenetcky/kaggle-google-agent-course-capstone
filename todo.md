I need to rework some of the flows


generally:

- keep the root_agent as an LlmAgent() that just calls the
typical loop for project generation

- build the database agent/s as a team (the summarization should probs be separate AgentTool())
- Have the db agent called in a very specific context as the end of the typical loop
- have the same/similar db agents available to the LlmAgent root_agent as a tool
if users want to forgo project generation and pull from some old favorites
- add favorites
- get the database to actually get setup correctly.
- add logging/callbacks/plugins etc... logging is the priority
- re-add session/memory (can't remember where we left off with that...)


