from typing import Literal
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from config import config
from ...types import MessageType
from .prompt import marketing_message_evaluator_instruction


class Feedback(BaseModel):
    """Model for providing evaluation feedback on marketing message quality."""

    grade: Literal["pass", "fail"] = Field(
        description="Evaluation result. 'pass' if the message meets all criteria, 'fail' if it needs revision."
    )
    comment: str = Field(
        description="Detailed explanation of the evaluation, highlighting which criteria were met or failed, and specific suggestions for improvement."
    )
    improvement_suggestions: list[str] | None = Field(
        default=None,
        description="Specific actionable suggestions for improving the message (only provided when grade is 'fail')."
    )


def get_message_evaluator(message_type: MessageType) -> LlmAgent:
    return LlmAgent(
        model=config.critic_model,
        name="marketing_message_evaluator",
        description="Evaluates marketing messages against brand guidelines and quality criteria.",
        instruction=marketing_message_evaluator_instruction,
        output_schema=Feedback,
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        output_key=f"{message_type.value}_evaluation",
    )

