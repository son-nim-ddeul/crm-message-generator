from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from ..types import MessageType
from config import config
from .prompt import get_report_config
from google.adk.agents.callback_context import CallbackContext


class ReportOutput(BaseModel):
    """Output schema for messages report."""

    estimation: str = Field(
        description="메시지 평가결과를 마크다운 형식의 보고서를 작성한 결과."
    )

    conclusion: str = Field(
        description="생성된 메시지와 메시지 평과 결과를 바탕으로 마크다운 형식의 보고서를 작성한 결과."
    )
    

def after_agent_callback(callback_context: CallbackContext):
    state = callback_context.state
    # global dict에 임시 캐싱
    session_id = callback_context.session.id
    # session_id를 key값으로
    # message_type, title, content, estimation, conclusion 캐싱
    return None

def create_report_pipeline(message_type: MessageType, description: str) -> LlmAgent:
    return LlmAgent(
        name="report_agent",
        model=config.writer_model,
        description=description,
        instruction=get_report_config(message_type=message_type),
        output_schema=ReportOutput,
        output_key=f"{message_type.value}_report",
        after_agent_callback=after_agent_callback
    )
    
aspirational_dreamer_report = create_report_pipeline(
    message_type=MessageType.ASPIRATIONAL_DREAMER,
    description="generate marketing report of aspirational dreamer message"
)

empathetic_supporter_report = create_report_pipeline(
    message_type=MessageType.EMPATHETIC_SUPPORTER,
    description="generate marketing report of empathetic supporter message"
)

playful_entertainer_report = create_report_pipeline(
    message_type=MessageType.PLAYFUL_ENTERTAINER,
    description="generate marketing report of playful entertainer message"
)

rational_advisor_report = create_report_pipeline(
    message_type=MessageType.RATIONAL_ADVISOR,
    description="generate marketing report of rational advisor message"
)