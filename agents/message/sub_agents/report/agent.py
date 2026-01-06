from google.adk.agents import ParallelAgent
from .pipeline import (
    aspirational_dreamer_report,
    empathetic_supporter_report,
    playful_entertainer_report,
    rational_advisor_report
)

report_agent = ParallelAgent(
    name="report_agent",
    description="각 전략별 메시지 생성 및 성과 예측 결과 보고서를 작성합니다.",
    sub_agents=[
        aspirational_dreamer_report,
        empathetic_supporter_report,
        playful_entertainer_report,
        rational_advisor_report
    ]
)
