# Multi-Agent Research Assistant (MCP-Based)

## Overview

This project implements a **multi-agent research assistant system** that autonomously researches a given topic, analyzes the collected information, and generates a structured summary.

The system demonstrates:
- **Multi-agent orchestration**
- **Model Context Protocol (MCP)** for tool-based external access
- **LLM-based reasoning using Groq**
- **Clear separation of responsibilities**
- **Production-grade engineering practices**

This project was built as part of an **AI/ML Developer interview assignment**.

---

## High-Level Architecture

User Query

│

▼

┌────────────────────────────┐

│ Orchestrator │

│ (ResearchWorkflow) │


└──────────────┬─────────────┘

│

▼

┌────────────────────────────┐


│ Research Agent (MCP) │

│ FastMCP Server (STDIO) │

│ Tool: web_search │

└──────────────┬─────────────┘

│

▼

┌────────────────────────────┐

│ Analysis Agent │

│ Groq + GPT-OSS-120B │

│ Insight Extraction │

└──────────────┬─────────────┘

│

▼

┌────────────────────────────┐

│ Summary Agent │

│ Deterministic Formatter │

└──────────────┬─────────────┘

▼

Final Structured Summary
---

## Agents and Responsibilities

### 1. Research Agent (MCP Server)

- Implemented as a **FastMCP server**

- Uses external web search APIs

- Exposes a tool: `web_search`

- Returns structured data:

  - `snippets`

  - `sources`

-Isolated via MCP for safety and extensibility

### 2. Analysis Agent

- Uses **Groq LLM (`openai/gpt-oss-120b`)**

- Extracts:

  - Key developments

  - Main themes and patterns

- Performs reasoning only (no external tools)

### 3. Summary Agent

- Deterministic (non-LLM)

- Formats results into a clean, readable report

- Reduces hallucination risk and inference cost

### 4. Orchestrator

- Coordinates agent execution

- Normalizes MCP protocol responses

- Manages agent-to-agent communication via structured data contracts

---

## MCP Usage

- **Transport:** STDIO

- **Server:** FastMCP

- **Client:** Official MCP Python client (`stdio_client`, `ClientSession`)

- MCP is used strictly at the **tool boundary**, keeping orchestration logic clean and deterministic.

---

## Project Structure

multi_agent_mcp/

├── agents/

│ ├── analysis_agent.py

│ └── summary_agent.py

│

├── mcp_server/

│ └── research_server.py

│

├── orchestrator/

│ ├── mcp_research_client.py

│ └── workflow.py

├── screenshotlog

├── tests/ # optional (local testing)

│ ├── test_analysis_agent.py

│ ├── test_research_tool.py

│ └── test_summary_agent.py

│

├── main.py # entry point

├── README.md

├── requirements.txt

├── .gitignore


---

## Setup Instructions

### 1. Create a Virtual Environment

```bash

python -m venv .venv

source .venv/bin/activate

2. Install Dependencies

pip install -r requirements.txt

3. Set Environment Variables

export GROQ_API_KEY="your_groq_api_key"

export GROQ_MODEL="openai/gpt-oss-120b"


API keys are injected via environment variables and are not committed.

Running the System

python main.py

Example Output

Topic: Recent developments in quantum computing

=== RESEARCH SUMMARY ===

Key Developments:

1. Hybrid quantum hardware combining multiple qubit technologies

2. Advances in quantum communication and security

3. Improved scalability through new system architectures

4. Miniaturization of quantum control hardware

5. Industry-wide monitoring of quantum progress

Main Themes:

- Scalability and network architecture improvements

- Hardware innovation and hybrid platforms

- Secure quantum communication

- Commercial readiness of quantum technologies

Sources:

- https://www.mckinsey.com/...

- https://www.sciencedaily.com/...

Generated at: 2025-12-31 15:32:56 UTC


Error Handling & Logging

MCP tool failures handled gracefully

Empty research results propagate safely

Logging enabled across:

MCP server

Orchestrator

Analysis agent

Design Decisions

MCP used to isolate external tools

LLM usage restricted to reasoning-heavy agent

Deterministic formatting for reliability

Structured data contracts between agents

Scalability Considerations

Add new agents without modifying existing ones

Parallelize research tools

Replace shared state with message queues or Redis

Add observability (metrics, tracing)

Security Considerations

No secrets committed

API keys via environment variables

Clear trust boundary at MCP tool layer
---------------------------------------------

Author

Shrish Dubey
AI / ML Engineer
