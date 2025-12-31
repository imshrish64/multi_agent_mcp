import json
from typing import Dict, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPResearchClient:
    """
    MCP Client for Research Agent (STDIO transport)
    """

    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
            env=None,
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.stdio, self.write = stdio_transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

    async def research(self, topic: str) -> Dict:
        if not self.session:
            raise RuntimeError("MCP session not initialized")

        result = await self.session.call_tool(
            name="web_search",
            arguments={"query": topic},
        )

        # 🔑 MCP RETURNS LIST → extract first content block
        content_block = result.content[0]

        # Case 1: Already dict (FastMCP often returns JSON directly)
        if isinstance(content_block, dict):
            return content_block

        # Case 2: Text block containing JSON
        if hasattr(content_block, "text"):
            return json.loads(content_block.text)

        raise ValueError("Unexpected MCP tool response format")

    async def close(self):
        await self.exit_stack.aclose()
