### Example Project: `customer-service-agent`

This example illustrates a project for a customer service AI agent.

#### File Tree

```
customer-service-agent/
├── .github/                      # CI/CD workflows (e.g., for testing, linting)
│   └── workflows/
│       └── main.yml
├── .gitignore                    # Files to ignore in git
├── .env.example                  # Example environment variables
├── .python-version               # Specifies Python version (e.g., for pyenv)
├── data/                         # For data files, like evaluation datasets
│   └── faqs.csv
├── docs/                         # Project documentation
│   ├── index.md
│   └── usage.md
├── notebooks/                    # Jupyter notebooks for exploration and analysis
│   └── agent_evaluation.ipynb
├── pyproject.toml                # Project metadata and dependencies (PEP 621)
├── README.md                     # Project overview and setup instructions
├── scripts/                      # Utility scripts (e.g., data processing, deployment)
│   └── load_faqs.py
├── src/                          # Main source code directory
│   └── customer_service_agent/
│       ├── __init__.py           # Makes the directory a Python package
│       ├── agent.py              # The core agent definition
│       ├── config.py             # Configuration loading
│       └── tools/                # A package for custom agent tools
│           ├── __init__.py
│           ├── order_lookup.py
│           └── shipping_status.py
└── tests/                        # Tests for your agent and tools
    ├── __init__.py
    ├── test_agent.py
    └── tools/
        ├── __init__.py
        └── test_order_lookup.py
```

---

### Explanation of Key Files and Directories

*   **`src/customer_service_agent/`**: This is the main Python package for your agent.
    *   **`__init__.py`**: This file is necessary to make the directory a Python package. It can be empty, or it can expose the agent, like so:
        ```python
        # src/customer_service_agent/__init__.py
        from .agent import customer_service_agent
        ```
    *   **`agent.py`**: This is where you define your agent's core logic using the ADK.
        ```python
        # src/customer_service_agent/agent.py
        from adk.agent import Agent
        from adk.llm import GenerativeModel
        from .tools.order_lookup import get_order_details

        customer_service_agent = Agent(
            name="customer_service_agent",
            llm=GenerativeModel(
                model_name="gemini-1.5-pro-latest",
                project="your-gcp-project-id",
                location="us-central1",
            ),
            instructions=[
                "You are a helpful customer service agent.",
                "Use your tools to look up order information.",
            ],
            tools=[get_order_details],
        )
        ```
    *   **`tools/`**: A sub-package to organize your custom tools. This keeps your agent's capabilities modular and easy to test.

*   **`pyproject.toml`**: This file is the modern standard for configuring Python projects. It defines dependencies, project metadata, and tool configurations (like linters and test runners).
    ```toml
    [project]
    name = "customer-service-agent"
    version = "0.1.0"
    description = "A customer service agent built with the Google ADK."
    requires-python = ">=3.10"
    dependencies = [
        "google-cloud-aiplatform",
        # Add other dependencies here
    ]

    [project.optional-dependencies]
    dev = [
        "pytest",
        "ruff",
    ]
    ```

*   **`tests/`**: Contains all your tests. Mirroring your `src` directory structure here is a good practice.

*   **`.env.example`**: A template for the environment variables your project needs. You would create a `.env` file (which is git-ignored) based on this for your local development.
    ```
    # .env.example
    GOOGLE_API_KEY="your-api-key-here"
    GCP_PROJECT_ID="your-gcp-project-id"
    ```

*   **`data/`**: For storing data files. This directory is often added to `.gitignore` if the data is large or sensitive.

*   **`docs/`**: For user and developer documentation.

*   **`notebooks/`**: For experiments, data analysis, and agent evaluation.

*   **`.github/workflows/`**: For Continuous Integration/Continuous Deployment (CI/CD). You can automate testing, linting, and even deployment to Google Cloud.

This structure provides a solid foundation for building, testing, and maintaining a high-quality AI agent with the Google ADK.