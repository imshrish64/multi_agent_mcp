"""
MCP Research Server
------------------
This MCP server exposes research-related tools to LLM agents.
It follows official MCP best practices:
- STDIO transport
- No stdout logging
- Tool-only responsibilities
"""

from typing import Any, Dict, List
import logging
import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Check if the key is loaded
if not os.getenv("SEARCH_API_KEY"):
    print("SEARCH_API_KEY not found. Ensure it is set in the .env file.")

# ---------------------------------------------------------------------
# Logging Configuration (STDERR ONLY - MCP SAFE)
# ---------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# MCP Server Initialization
# ---------------------------------------------------------------------

mcp = FastMCP("research-tools")

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SEARCH_API_URL = "https://api.tavily.com/search"
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")  # optional, mock if missing

DEFAULT_TIMEOUT = 20.0

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

async def perform_web_search(query: str) -> Dict[str, Any] | None:
    """
    Performs a web search using an external API.
    Returns structured data or None on failure.
    """
    if not SEARCH_API_KEY:
        logger.warning("SEARCH_API_KEY not set. Returning mock data.")
        return {
            "snippets": [
                "Recent advancements in quantum computing include better error correction techniques.",
                "IBM and Google announced next-generation quantum processors."
            ],
            "sources": [
                "https://www.ibm.com/quantum",
                "https://www.nature.com/quantum-information"
            ]
        }

    payload = {
        "query": query,
        "max_results": 5
    }

    headers = {
        "Authorization": f"Bearer {SEARCH_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            response = await client.post(
                SEARCH_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            snippets: List[str] = []
            sources: List[str] = []

            for item in data.get("results", []):
                if item.get("content"):
                    snippets.append(item["content"])
                if item.get("url"):
                    sources.append(item["url"])

            return {
                "snippets": snippets,
                "sources": sources
            }

        except Exception as exc:
            logger.error(f"Web search failed: {exc}")
            return None

# ---------------------------------------------------------------------
# MCP Tool Definition
# ---------------------------------------------------------------------

@mcp.tool()
async def web_search(query: str) -> Dict[str, Any]:
    """
    Search the web for a given topic and return structured research data.

    Args:
        query: Topic or question to research

    Returns:
        {
            "snippets": List[str],
            "sources": List[str]
        }
    """
    logger.info(f"Executing web_search tool | query='{query}'")

    result = await perform_web_search(query)

    if not result:
        logger.warning("Web search returned no data.")
        return {
            "snippets": [],
            "sources": []
        }

    logger.info(
        f"Web search completed | snippets={len(result['snippets'])} "
        f"sources={len(result['sources'])}"
    )

    return result

# ---------------------------------------------------------------------
# Server Entrypoint
# ---------------------------------------------------------------------

def main() -> None:
    """
    Run MCP server using STDIO transport.
    """
    logger.info("Starting MCP Research Server (STDIO)")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
