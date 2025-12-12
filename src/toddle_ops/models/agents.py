from pydantic import BaseModel

class AgentInstructions(BaseModel):
    persona: str
    primary_objective: list[str]
    guiding_principles: list[str]
    constraints: list[str]
    incoming_keys: list[str]

