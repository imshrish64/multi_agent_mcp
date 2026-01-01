from datetime import datetime
from typing import Dict, List
import logging
import traceback

logger = logging.getLogger(__name__)


class SummaryAgent:
    """
    Summary Agent:
    - Formats analyzed data into a structured, user-friendly summary
    - Fails gracefully with proper MCP-safe logging
    """

    def run(
        self,
        topic: str,
        analysis_data: Dict[str, List[str]] | None,
        sources: List[str] | None,
    ) -> str:

        logger.info("SummaryAgent started")

        try:
            # Defensive defaults
            analysis_data = analysis_data or {}
            sources = sources or []

            key_devs = analysis_data.get("key_developments", [])
            themes = analysis_data.get("themes", [])

            if not isinstance(key_devs, list):
                logger.warning("key_developments is not a list; coercing to empty list")
                key_devs = []

            if not isinstance(themes, list):
                logger.warning("themes is not a list; coercing to empty list")
                themes = []

            if not isinstance(sources, list):
                logger.warning("sources is not a list; coercing to empty list")
                sources = []

            logger.info(
                "Input validated | topic='%s' key_devs=%d themes=%d sources=%d",
                topic,
                len(key_devs),
                len(themes),
                len(sources),
            )

            lines = []
            lines.append(f"Topic: {topic}")
            lines.append("")
            lines.append("=== RESEARCH SUMMARY ===")
            lines.append("")
            lines.append("Key Developments:")

            if key_devs:
                for idx, item in enumerate(key_devs, start=1):
                    lines.append(f"{idx}. {item}")
            else:
                lines.append("No key developments identified.")

            lines.append("")
            lines.append("Main Themes:")

            if themes:
                for theme in themes:
                    lines.append(f"- {theme}")
            else:
                lines.append("No themes identified.")

            lines.append("")
            lines.append("Sources:")

            if sources:
                for src in sources:
                    lines.append(f"- {src}")
            else:
                lines.append("No sources available.")

            lines.append("")
            lines.append(
                f"Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

            logger.info("SummaryAgent completed successfully")
            return "\n".join(lines)

        except Exception as exc:
            # MCP-safe: log full traceback to STDERR
            logger.error("SummaryAgent failed with exception: %s", exc)
            logger.error(traceback.format_exc())

            # Graceful fallback response
            return (
                "Topic: "
                + (topic or "Unknown")
                + "\n\n"
                "=== RESEARCH SUMMARY ===\n\n"
                "An error occurred while generating the summary.\n"
                "The issue has been logged for investigation.\n\n"
                f"Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
