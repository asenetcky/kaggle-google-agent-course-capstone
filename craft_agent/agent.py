from google.adk.agents import ParallelAgent, SequentialAgent

safety_officer=""
aggregator = ""
material_researcher = ""
craft_researcher = ""
polisher=""

parallel_craft_lookup_team = ParallelAgent(
    name="LookupTeam",
    sub_agents=[""],
)

root_agent = SequentialAgent(
    name="CraftSystem",
    sub_agents=[
        parallel_craft_lookup_team,
    ],
)
