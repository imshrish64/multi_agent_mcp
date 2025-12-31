import logging
import os
import json
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
logger = logging.getLogger(__name__)


class AnalysisAgent:
    """
    Analysis Agent:
    - Extracts key developments
    - Identifies main themes
    - Uses Groq + Qwen QwQ-32B
    """

    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
            temperature=0.2,
            max_tokens=1024,
        )

    def run(self, research_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
        snippets = research_data.get("snippets", [])

        if not snippets:
            logger.warning("AnalysisAgent received no snippets")
            return {
                "key_developments": [],
                "themes": []
            }

        logger.info("AnalysisAgent started")

        prompt = f"""
You are a senior research analyst.

Analyze the following research snippets and do the following:
1. Extract 3–5 key developments.
2. Identify 3–5 main themes or patterns.

Snippets:
{snippets}

IMPORTANT:
- Return ONLY valid JSON
- No markdown
- No explanations

JSON format:
{{
  "key_developments": ["..."],
  "themes": ["..."]
}}
"""

        response = self.llm.invoke(
            [
                SystemMessage(content="You extract structured insights from research data."),
                HumanMessage(content=prompt)
            ]
        )

        try:
            parsed = json.loads(response.content)
            logger.info("AnalysisAgent completed successfully")
            return parsed

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Raw response: {response.content}")
            return {
                "key_developments": [],
                "themes": []
            }
