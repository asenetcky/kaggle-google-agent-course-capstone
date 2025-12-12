from pydantic import BaseModel

class AgentInstructions(BaseModel):
    """
    A model representing the instructions for an AI agent.
    """
    persona: str = "helpful assistant"
    primary_objective: list[str]
    guiding_principles: list[str] | None = []
    constraints: list[str] | None = []
    incoming_keys: list[str] | None = []

    def format_instructions(self) -> str:
        """
        Format the agent instructions into a structured string.
        """

        objectives = "".join(f"\t- {obj}\n" for obj in self.primary_objective)    
        guiding_principles = "".join(f"\t- {principle}\n" for principle in self.guiding_principles)
        constraints = "".join(f"\t- {constraint}\n" for constraint in self.constraints)
        incoming_keys = "".join(f"\t- {{{key}}}\n" for key in self.incoming_keys)
        
        instructions = (
            f"Persona: You are a {self.persona}\n\n"
            f"Your primary objectives are:\n"
            f"{objectives}\n"
            f"Please adhere to the following guiding principles:\n"
            f"{guiding_principles}\n"
            f"You must NEVER do the following:\n"
            f"{constraints}\n"
            f"You will receive the following incoming keys:\n"
            f"{incoming_keys}"
        )

        return instructions
