import asyncio
import logging
from orchestrator.workflow import ResearchWorkflow
logging.basicConfig(level=logging.INFO)


def main():
    topic = "Recent development in AI-driven drug discovery"

    workflow = ResearchWorkflow(
        mcp_server_path="mcp_server/research_server.py"
    )
    result = asyncio.run(workflow.run(topic))
    print(result)

if __name__ == "__main__":
    main()
