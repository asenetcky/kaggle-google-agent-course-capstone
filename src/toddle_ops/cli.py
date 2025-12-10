"""
This module provides a command-line interface for the Toddle-Ops application.
"""
import asyncio

import google.adk
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from typing_extensions import Annotated

from toddle_ops.agents.root_agent.agent import root_agent

app = typer.Typer(
    name="toddle-ops",
    help="Fast and Easy Project Generation for Exhausted Caregivers.",
    add_completion=False,
)

console = Console()


@app.command()
def create(
    prompt: str = typer.Argument(
        ..., help="A prompt or context for the kind of project to generate."
    )
):
    """
    Generates a new toddler craft project by running the root agent.
    """

    async def run_agent_async():
        spinner = Spinner("dots", text="[bold cyan]Generating a new project...[/bold cyan]")
        console.print(spinner)
        final_output = {}
        try:
            async for event in google.adk.run_agent(root_agent, prompt=prompt):
                console.print(f"EVENT TYPE: {type(event)}")
                console.print(f"EVENT CONTENT: {event}")
                if "StepStart" in str(type(event)):
                    spinner.text = f"[bold cyan]Running: {event.agent_name}...[/bold cyan]"
                if "AgentFinish" in str(type(event)):
                    final_output = event.outputs

            # Clear the spinner before printing the result
            console.print("\r", end="")

            project_markdown = final_output.get(
                "human_project", "Could not generate project."
            )
            console.print(Markdown(project_markdown))

        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

    asyncio.run(run_agent_async())


if __name__ == "__main__":
    app()
