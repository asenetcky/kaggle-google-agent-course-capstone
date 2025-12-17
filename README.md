
<div align="center">

# 👶 Toddle Ops

**AI-Powered Project Generation for Exhausted Caregivers**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google)](https://google.github.io/adk-docs/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Demo](#-demo)

![gemini ai generated picture of toddlers sitting around a conference table working on a software project.](images/toddle-ops.png)

</div>

---

## 🎯 What is Toddle Ops?

Keeping a toddler happily occupied is a full-time job—and you probably already have one. Add sleep deprivation to the mix, and those enriching activities your little one needs can feel impossible to manage.

**Toddle Ops is your AI-powered concierge for toddler activities.** Using a sophisticated multi-agent system, it researches, validates, and formats safe, engaging projects tailored for children aged 1-3 years—all in seconds.

> **The mission:** Lower the barrier to quality toddler activities to *absolute zero*. All you need to do is bring the energy (we know that's already asking a lot 💪).

### 💡 Born from the Trenches

This project grew out of the [Google 5-Day AI Agents Intensive Course](https://www.kaggle.com/learn-guide/5-day-agents) and the [Agents Intensive Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project). It's a real-world solution to a real-world problem: parenting is hard, and AI can help.

---

## ✨ Features

- 🤖 **Multi-Agent Architecture** - Specialized AI agents handle research, safety validation, and formatting
- 🔍 **Smart Research** - Automatically searches for age-appropriate activities using Google Search
- 🛡️ **Safety First** - Built-in safety critic and refiner ensure projects are toddler-safe
- ✏️ **Editorial Polish** - Grammar and clarity checks for easy-to-follow instructions
- 💾 **Session Memory** - Remembers your preferences across conversations
- 🗄️ **Supabase Integration** - PostgreSQL database backend for persistent session storage
- 🌐 **Web Interface** - Clean, modern UI powered by ADK Web Server
- 📝 **Structured Output** - Consistent format with materials, duration, and step-by-step instructions

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** - [Download here](https://www.python.org/downloads/)
- **uv** - Fast Python package installer ([Installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Google Gemini API Key** - [Get one here](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/asenetcky/toddle-ops.git
cd toddle-ops

# Install dependencies with uv
uv sync

# Set up your environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Create `.env` File

Create a `.env` file in the project root:

```bash
# Required: Gemini API Key
GOOGLE_API_KEY=your_api_key_here

# Required: Supabase Database Configuration
SUPABASE_USER=your_supabase_user
SUPABASE_PASSWORD=your_supabase_password

# Optional: For production deployments
GOOGLE_PROJECT_ID=your_project_id
DEPLOYED_REGION=us-central1
```

---

## 🎮 Usage

### Option 1: Command Line Interface

Run the agent directly from the terminal using the convenient Makefile:

```bash
make run
```

Or run directly with uv:

```bash
uv run ./src/toddle_ops/main.py
```

### Option 2: Streamlit Web UI (Recommended)

Beautiful, modern web interface with chat functionality:

```bash
# Run locally
make ui

# Or directly with uv
uv run streamlit run src/toddle_ops/ui.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

**Features:**
- 💬 Interactive chat interface
- 🎨 Quick prompt buttons for common activities
- 📊 Session info display
- 🔄 New session button to start fresh
- ⚠️ Safety notes and example prompts

See the [Streamlit UI](#-streamlit-web-ui) section for more details.

### Option 3: ADK CLI

For development and testing:

```bash
cd src/toddle_ops/agents
adk run orchestrator
```

```bash
cd src/toddle_ops/agents
adk run orchestrator
```

### Example Interaction

```
You: Hello ToddleOps! Please create a new project for me.
Agent: [Researches, validates, and formats a safe project...]

- **Name:** DIY Sensory Bottle
- **Description:** Create a mesmerizing sensory bottle filled with colorful 
  and sparkly items that slowly drift and swirl, providing a calming visual 
  experience for toddlers.
- **Duration:** 30 minutes
- **Materials:**
    * Empty, clean plastic bottle with a secure lid
    * Water
    * Clear glue or corn syrup
    * Glitter, sequins, large pom-poms
    * Food coloring (optional)
    * Strong adhesive for sealing the lid
- **Instructions:**
    1. Prepare the Bottle: Ensure the bottle is clean and dry
    2. Add Base Liquid and Fillers: Fill 2/3 full with warm water and glue
    3. Add Decorative Items: Add glitter, sequins, and large items
    4. Add Color (Optional): Add food coloring if desired
    5. Secure the Lid: Glue the lid shut and allow to dry completely
    6. Test and Play: Shake and observe the slow, captivating movement
```

---

## 🗄️ Supabase Integration

Toddle Ops uses **Supabase** (PostgreSQL) for persistent session storage, allowing conversations to be resumed across application restarts.

### Database Setup

1. **Create a Supabase Project**
   - Sign up at [supabase.com](https://supabase.com)
   - Create a new project
   - Wait for the database to be provisioned

2. **Get Database Credentials**
   - Navigate to Project Settings → Database
   - Copy your database password (you set this during project creation)
   - Note your database user (usually `postgres`)

3. **Configure Environment Variables**
   ```bash
   SUPABASE_USER=postgres
   SUPABASE_PASSWORD=your_password_here
   ```

### Session Service Architecture

The application uses ADK's `DatabaseSessionService` to:
- **Persist user sessions** across application restarts
- **Store conversation history** for context continuity
- **Manage session metadata** (user IDs, timestamps, app names)
- **Support concurrent users** with isolated session data

```python
# From src/toddle_ops/services/sessions.py
db_url = f"postgresql+asyncpg://{SUPABASE_USER}:{SUPABASE_PASSWORD}@aws-0-us-west-2.pooler.supabase.com:5432/postgres"
session_service = DatabaseSessionService(db_url=db_url)
```

### Benefits

✅ **Persistent Conversations** - Resume exactly where you left off  
✅ **Multi-User Support** - Each user has isolated session data  
✅ **Scalable Storage** - PostgreSQL handles large conversation histories  
✅ **Cloud-Native** - Supabase provides managed infrastructure  
✅ **Easy Migration** - Standard PostgreSQL compatible with other databases

### Alternative: Local Development

For local development without Supabase, you can switch to in-memory sessions:

```python
# In src/toddle_ops/services/sessions.py
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()
```

⚠️ **Note:** In-memory sessions are lost when the application restarts.

---

## 🖥️ Streamlit Web UI

Toddle Ops includes a beautiful, production-ready Streamlit web interface for easy interaction with the AI agents.

### Features

| Feature | Description |
|---------|-------------|
| 💬 **Chat Interface** | Natural conversation with the AI agent |
| 🎨 **Quick Prompts** | One-click buttons for Creative Projects, Sensory Activities, and Active Play |
| 📊 **Session Info** | Real-time display of session ID, user ID, and message count |
| 🔄 **New Session** | Start a fresh conversation anytime |
| 📝 **Example Prompts** | Helpful suggestions for getting started |
| ⚠️ **Safety Notes** | Reminders about toddler supervision |

### Running the UI

```bash
# Using Make (recommended)
make ui

# Or directly with uv
uv run streamlit run src/toddle_ops/ui.py

# Or with Docker
docker-compose up -d
```

### Quick Prompt Buttons

The sidebar includes one-click buttons for common activity types:

- 🎨 **Creative Project** - "Create a creative art project for my toddler"
- 🌈 **Sensory Activity** - "Give me a sensory activity for a 2-year-old"
- 🏃 **Active Play** - "Suggest an active indoor activity for a toddler"

### Architecture Notes

The Streamlit UI uses a special async handling pattern to work with the ADK's async database operations:

- **Separate Thread Execution** - Each request runs in its own thread with a dedicated event loop
- **Fresh Session Service** - Creates new `InMemorySessionService` per request to avoid asyncpg event loop conflicts
- **Thread-Safe Design** - All Streamlit session state values are passed as parameters to async functions

```python
# The UI creates fresh async resources in each worker thread
def _generate_project_sync(prompt: str, user_id: str, session_id: str | None):
    async def _run():
        local_session_service = InMemorySessionService()
        local_memory_service = InMemoryMemoryService()
        runner = Runner(app=app, session_service=local_session_service, ...)
        # ... run agent
    
    # Execute in separate thread with its own event loop
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_thread)
        return future.result()
```

### Configuration

The Streamlit app is configured via `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

### Environment Variables

The UI requires the same environment variables as the CLI:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional (for database persistence in CLI mode)
SUPABASE_USER=your_supabase_user
SUPABASE_PASSWORD=your_supabase_password
```

---

## 🏗️ Architecture

Toddle Ops uses [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/) to orchestrate multiple specialized agents:

```mermaid
graph TD
    User[👤 User] -->|Request| Orchestrator[🎭 Orchestrator Agent]
    Orchestrator --> Research[🔍 Research Team]
    Research --> Researcher[Research Agent]
    Research --> Synthesizer[Synthesis Agent]
    Synthesizer --> QA[✅ Quality Assurance Team]
    QA --> Safety[Safety Loop]
    Safety --> Critic[Safety Critic]
    Safety --> Refiner[Safety Refiner]
    QA --> Editorial[Editorial Agent]
    Editorial --> Formatter[📄 Formatter Agent]
    Formatter --> User
```

### Agent Roles

| Agent | Responsibility |
|-------|---------------|
| **Orchestrator** | Routes requests and manages overall workflow |
| **Research Team** | Searches for age-appropriate projects using Google Search |
| **Synthesis Agent** | Combines research into a coherent project structure |
| **Safety Critic** | Evaluates projects for toddler safety (choking hazards, supervision needs) |
| **Safety Refiner** | Revises projects based on safety feedback |
| **Editorial Agent** | Polishes grammar, clarity, and age-appropriateness |
| **Formatter** | Outputs clean, consistent markdown format |

---

## 📸 Demo

### Web Interface
![Example of the ADK Web Interface](images/example-project.png)

---

## 🛠️ Development

### Project Structure

```
toddle-ops/
├── src/toddle_ops/
│   ├── agents/                        # Agent definitions
│   │   ├── orchestrator/              # Root agent and workflows
│   │   ├── research_team/             # Research and synthesis agents
│   │   └── quality_assurance_team/    # Safety and editorial agents
│   ├── models/                        # Pydantic models
│   │   ├── agents.py                  # Agent instruction models
│   │   ├── projects.py                # Project data models
│   │   └── reports.py                 # Status report models
│   ├── services/                      # Core services
│   │   ├── callbacks.py               # Agent callbacks
│   │   ├── memory.py                  # Memory service
│   │   └── sessions.py                # Session management
│   ├── app.py                         # ADK App configuration
│   ├── config.py                      # Application configuration
│   ├── enums.py                       # Status enums
│   ├── helpers.py                     # Helper functions
│   ├── main.py                        # CLI entry point
│   ├── plugins.py                     # Custom retry plugin
│   └── ui.py                          # Streamlit web UI
├── .streamlit/                        # Streamlit configuration
│   └── config.toml                    # Theme and server settings
├── tests/                             # Test suite
├── notebooks/                         # Marimo notebooks for development
├── Makefile                           # Development commands
└── pyproject.toml                     # Project dependencies
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Format and lint
make ruff
```

### Development Makefile Commands

```bash
make install      # Install production dependencies only
make install-dev  # Install all dependencies including dev tools
make ruff         # Run code formatting and linting
make run          # Run the application (CLI)
make ui           # Run Streamlit web UI
make test-research # Run research team agent tests
```

### Key Features in Current Implementation

- **Custom Plugin System**: `CustomRetryPlugin` handles errors from both Pydantic models and dictionaries
- **Structured Models**: Pydantic models for `StatusReport`, `StandardProject`, and agent instructions
- **Memory Service**: Persistent session and conversation history using ADK memory system
- **Agent Callbacks**: Automatic memory saving after each agent turn
- **Error Handling**: Robust error detection and retry logic with reflection
- **Status Workflow**: Approval workflow with states: `APPROVED`, `PENDING`, `REVISION_NEEDED`, `REJECTED`
- **Supabase Integration**: PostgreSQL backend for session persistence
- **Streamlit UI**: Modern web interface with chat functionality and quick prompts
- **Makefile**: Simplified development workflow with common commands


---

## 🚢 Deployment

### Google Cloud (Vertex AI Agent Engine)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Configure your project
export GOOGLE_PROJECT_ID=your_project_id
export DEPLOYED_REGION=us-central1

# Deploy
cd src/toddle_ops/agents
adk deploy agent_engine \
  --project=$GOOGLE_PROJECT_ID \
  --region=$DEPLOYED_REGION \
  vertex_agent \
  --agent_engine_config_file=vertex_agent/.agent_engine_config.json
```

---

## 🗺️ Roadmap

### Completed ✅
- [x] Multi-agent architecture with ADK
- [x] Safety validation system with critic and refiner agents
- [x] Editorial agent for polished output
- [x] Session memory and conversation history
- [x] Supabase PostgreSQL integration for persistent sessions
- [x] Custom error handling with ReflectAndRetryToolPlugin
- [x] Pydantic models for structured data
- [x] Command-line interface with session management
- [x] Makefile for easy development workflow

### In Progress 🚧
- [ ] Web interface improvements
- [ ] Enhanced safety validation rules

### Future Features 🔮
- [ ] User authentication and project history
- [ ] Local project storage with MCP SQLite integration
- [ ] PDF export of projects
- [ ] Image generation for project visualization
- [ ] Mobile-responsive design improvements
- [ ] Project rating and feedback system
- [ ] Custom project templates

---

## 🔧 Recent Updates

### Version 0.3.0

**Bug Fixes:**
- Fixed `AttributeError` in `CustomRetryPlugin` when handling `StatusReport` Pydantic models
- Proper type checking for both Pydantic models and dictionary results
- Improved error detection logic to distinguish between workflow status and actual errors

**Improvements:**
- Enhanced safety refinement loop with proper status handling
- Better integration between safety critic and refiner agents
- Cleaner separation between `APPROVED`, `PENDING`, `REVISION_NEEDED`, and `REJECTED` statuses
- More robust error handling with backward compatibility
- Integrated Supabase PostgreSQL for persistent session storage
- Database-backed session service using ADK's `DatabaseSessionService`

**Development:**
- Updated plugin system to handle mixed return types (Pydantic models and dicts)
- Improved logging and debugging output
- Added comprehensive type hints throughout the codebase

---

## 🤝 Contributing

Contributions are welcome! This project is a learning experiment, so feel free to:

- 🐛 Report bugs or issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google ADK Team** - For the excellent Agent Development Kit framework
- **Kaggle & Google** - For the 5-Day AI Agents Intensive Course
- **Exhausted parents everywhere** - This one's for you ☕

---

<div align="center">

**Made with ❤️ (and way too much caffeine) by [asenetcky](https://github.com/asenetcky)**

[⬆ Back to Top](#-toddle-ops)

</div>


