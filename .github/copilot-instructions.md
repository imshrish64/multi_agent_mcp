# AI Coding Agent Instructions for Multi-Agent MCP Project

## Project Overview
This project implements a multi-agent system for research, analysis, and orchestration workflows. The architecture is modular, with distinct components for agents, servers, and tools. The system is designed to facilitate asynchronous operations and integrates external APIs for research tasks.

### Key Components
- **Agents** (`agents/`):
  - `analysis_agent.py`: Handles data analysis tasks.
  - `research_agent.py`: Performs web-based research.
  - `summary_agent.py`: Summarizes findings from research and analysis.
- **MCP Server** (`mcp_server/`):
  - `research_server.py`: Provides the `web_search` function for querying external APIs.
  - `tools.py`: Contains utility functions shared across the server.
- **Orchestrator** (`orchestrator/`):
  - `workflow.py`: Manages the workflow between agents and servers.
- **Tests** (`python_test/`):
  - `test_research_tool.py`: Example test for the `web_search` function.

## Developer Workflows

### Running Tests
- Navigate to the `python_test/` directory.
- Run tests using:
  ```bash
  python ./test_research_tool.py
  ```

### Debugging
- Use `asyncio.run()` to execute asynchronous functions in isolation.
- Example:
  ```python
  asyncio.run(test())
  ```

### Environment Setup
- The project uses a virtual environment located in `multimcp/`.
- Activate the environment:
  ```bash
  source multimcp/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Project-Specific Conventions
- **Asynchronous Programming**: Most functions, especially in `mcp_server/`, are asynchronous. Always use `await` when calling these functions.
- **Modular Design**: Each agent and server module has a single responsibility. Follow this pattern when adding new components.
- **Logging**: Logs are stored in the `logs/` directory. Use structured logging for debugging and monitoring.

## Integration Points
- **External APIs**: The `web_search` function in `research_server.py` integrates with external web services for research tasks.
- **Cross-Component Communication**: Agents interact with the MCP server via function calls. Ensure compatibility when modifying interfaces.

## Examples
### Adding a New Agent
1. Create a new file in `agents/` (e.g., `new_agent.py`).
2. Implement the agent's logic as an asynchronous function.
3. Register the agent in `orchestrator/workflow.py`.

### Modifying `web_search`
- Update the `web_search` function in `mcp_server/research_server.py`.
- Add or update tests in `python_test/test_research_tool.py`.

---

For questions or further clarification, refer to the `README.md` or contact the project maintainers.