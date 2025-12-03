from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

mcp_sqlite_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",  # Run MCP server via npx
            args=["mcp-server-sqlite", "--db-path", "projects-data.db"],
        ),
        timeout=30,
    )
)
