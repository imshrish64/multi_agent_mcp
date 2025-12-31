import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.summary_agent import SummaryAgent
analysis_output = {
    "key_developments": [
        "IBM, Google, and Microsoft announced major quantum hardware breakthroughs in 2025",
        "Significant improvements in quantum error correction techniques",
        "Enhanced fault tolerance in quantum processors",
        "Accelerated path toward commercialization of quantum technologies",
    ],
    "themes": [
        "Leadership of major tech firms in quantum hardware innovation",
        "Advances in error correction and fault tolerance",
        "Rapid progression from research to commercial applications",
        "Increasing viability of quantum computing in the market",
    ],
}

sources = [
    "https://www.ibm.com/quantum",
    "https://www.networkworld.com/article/4088709/top-quantum-breakthroughs-of-2025.html",
]

agent = SummaryAgent()
result = agent.run(
    topic="Quantum Computing",
    analysis_data=analysis_output,
    sources=sources,
)

print(result)
