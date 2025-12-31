import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from mcp_server.research_server import web_search

async def test():
    result = await web_search("quantum Physics advancements in 2025")
    print(result)  # OK here, NOT MCP server

if __name__ == "__main__":
    asyncio.run(test())