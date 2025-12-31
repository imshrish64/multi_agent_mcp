from datetime import datetime
from typing import Dict, List


class SummaryAgent:
    """
    Summary Agent:
    - Formats analyzed data into a structured, user-friendly summary
    """

    def run(
        self,
        topic: str,
        analysis_data: Dict[str, List[str]],
        sources: List[str],
    ) -> str:
        key_devs = analysis_data.get("key_developments", [])
        themes = analysis_data.get("themes", [])

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

        return "\n".join(lines)
