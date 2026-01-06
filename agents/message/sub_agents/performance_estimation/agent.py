from google.adk.agents import ParallelAgent
from .pipeline import (
    aspirational_dreamer_estimation,
    empathetic_supporter_estimation,
    playful_entertainer_estimation,
    rational_advisor_estimation
)

performance_estimation_agent = ParallelAgent(
    name="performance_estimation_agent",
    description="각 전략별 마케팅 예상 성과를 추측합니다.",
    sub_agents=[
        aspirational_dreamer_estimation,
        empathetic_supporter_estimation,
        playful_entertainer_estimation,
        rational_advisor_estimation
    ]
)
