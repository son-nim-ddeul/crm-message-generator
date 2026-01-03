from google.adk.agents import ParallelAgent
from .pipelines import (
    aspirational_dreamer_message,
    empathetic_supporter_message,
    playful_entertainer_message,
    rational_advisor_message
)

message_generate_pipeline_agent = ParallelAgent(
    name="message_generate_pipeline",
    description="마케팅 메시지 생성 파이프라인. 여러 가지 톤의 메시지를 동시에 생성합니다.",
    sub_agents=[
        aspirational_dreamer_message,
        empathetic_supporter_message,
        playful_entertainer_message,
        rational_advisor_message
    ]
)
