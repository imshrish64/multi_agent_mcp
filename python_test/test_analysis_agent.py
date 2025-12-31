import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.analysis_agent import AnalysisAgent

sample_input = {
    "snippets": [
        "IBM, Google, and Microsoft announced major quantum hardware breakthroughs in 2025.",
        "Error correction and fault tolerance improved significantly, accelerating commercialization."
    ],
    "sources": []
}

agent = AnalysisAgent()
result = agent.run(sample_input)
print(result)
