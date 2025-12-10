"""
This module provides a command-line interface for the Toddle-Ops application.
"""

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from typing_extensions import Annotated

from toddle_ops.agents.root_agent.agent import root_agent
from toddle_ops.mcp.supabase import supabase_repo

app = typer.Typer(
    name="toddle-ops",
    help="Fast and Easy Project Generation for Exhausted Caregivers.",
    add_completion=False,
)

db_app = typer.Typer(
    name="db",
    help="Interact with the Toddle-Ops project database.",
    add_completion=False,
)
app.add_typer(db_app)

console = Console()


@app.command()
def new(
    prompt: Annotated[
        str,
        typer.Argument(
            help="An optional prompt or context for the kind of project to generate."
        ),
    ] = "A fun and simple craft project for a toddler.",
):
    """
    Generates a new toddler craft project.
    """
    console.print("[bold cyan]Generating a new project...[/bold cyan]")
    try:
        response = root_agent.run(prompt=prompt)
        project_markdown = response.get("human_project", "Could not generate project.")
        console.print(Markdown(project_markdown))
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")


@db_app.command("list")
def db_list():
    """
    Lists all projects in the database.
    """
    console.print("[bold cyan]Fetching projects from the database...[/bold cyan]")
    try:
        projects = supabase_repo.list_projects()
        if not projects:
            console.print("[yellow]No projects found in the database.[/yellow]")
            return

        table = Table(
            "ID", "Name", "Description", "Duration (min)", title="Projects"
        )
        for p in projects:
            table.add_row(
                str(p.get("id")),
                p.get("name"),
                p.get("description"),
                str(p.get("duration_minutes")),
            )
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")


@db_app.command("get")
def db_get(
    name: Annotated[
        str, typer.Argument(help="The exact name of the project to retrieve.")
    ]
):
    """
    Gets a specific project from the database by name.
    """
    console.print(
        f"[bold cyan]Fetching project '{name}' from the database...[/bold cyan]"
    )
    try:
        project = supabase_repo.get_project_by_name(name)
        if not project:
            console.print(f"[yellow]Project '{name}' not found.[/yellow]")
            return

        # Create a human-readable format from the dictionary
        md_string = f"""
# {project.get('name')}

**Description:** {project.get('description')}

**Duration:** {project.get('duration_minutes')} minutes

**Materials:**
{project.get('materials')}

**Instructions:**
{project.get('instructions')}
        """
        console.print(Markdown(md_string))

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")


if __name__ == "__main__":
    app()
