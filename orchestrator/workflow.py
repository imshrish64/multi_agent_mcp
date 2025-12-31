import logging
from agents.analysis_agent import AnalysisAgent
from agents.summary_agent import SummaryAgent
from orchestrator.mcp_research_client import MCPResearchClient
logger = logging.getLogger(__name__)


class ResearchWorkflow:
    """
    Orchestrates MCP Research → Analysis → Summary
    """

    def __init__(self, mcp_server_path: str):
        self.mcp_client = MCPResearchClient(mcp_server_path)
        self.analysis_agent = AnalysisAgent()
        self.summary_agent = SummaryAgent()

    async def run(self, topic: str) -> str:
        logger.info(f"Workflow started | topic='{topic}'")

        # Connect to MCP server
        await self.mcp_client.connect()

        try:
            # Research via MCP
            research_data = await self.mcp_client.research(topic)

            # Analysis
            analysis = self.analysis_agent.run(research_data)

            # Summary
            summary = self.summary_agent.run(
                topic=topic,
                analysis_data=analysis,
                sources=research_data.get("sources", []),
            )

            return summary

        finally:
            await self.mcp_client.close()
            logger.info("Workflow completed")   