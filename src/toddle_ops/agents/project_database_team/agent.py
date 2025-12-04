from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool

from toddle_ops.config import retry_config
from toddle_ops.mcp.sqlite import mcp_sqlite_server

root_agent = LlmAgent(
    name="ProjectDatabaseAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a database administrator for toddler projects.
        You receive a toddler project: {final_project}

        Your goal is to save this project to the database.

        1. Formulate a plan to save the project.
        2. Check to see if the database is initialized - if not - initialize
        the database. The database MUST be called 'toddle-ops-data.db'
        3. Projects will be saved to a table called 'toddle_ops_projects' - initialize
        this table if it does not exist using this example:
            - id: SQL integer identity
            - project_name: varchar derived from Project.name
            - description: string derived from Project.description
            - difficulty: string derived from Project.difficulty
            - materials: string derived from Project.materials
            - duration_minutes: int derived from Project.duration_minutes
            - instructions: string derived from Project.materials
            - date_created: date derived from the date you perform this action
            - date_modified: date derived from the date you modify this row
        3. You MUST call `ask_user_permission` with a summary of your intended actions.
            Example summary: 
            1. Initialize database (if missing).
            2. Creating the toddle_ops_projects table (if missing).
            3. Save project 'Glue Art' to projects table.
        3. IF the user says 'yes':
            - Perform the actions (e.g. using the mcp server).
            - Output the saved project.
        4. IF the user says 'no':
            - Do nothing.
            - Output "Action Cancelled by user."
        """,
    tools=[
        # FunctionTool(tools.ask_user_permission),
        mcp_sqlite_server,
    ],
    output_key="database_queue",
)
