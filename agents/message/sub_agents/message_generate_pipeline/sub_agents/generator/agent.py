from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from config import config
from ....types import MessageType

from .prompt import (
    get_message_generator_config,
    get_enhanced_message_generator_config
)


class MessageOutput(BaseModel):
    """Output schema for marketing messages."""
    
    title: str = Field(description="Message title, maximum 40 characters in Korean")
    content: str = Field(description="Message content, maximum 350 characters in Korean")
    tone_rationale: str = Field(description="Brief explanation of how this message implements the specific emotional tone strategy")

class EnhancedMessageOutput(MessageOutput):
    """Model for providing evaluation feedback on marketing message quality."""

    revision_notes: str = Field(
        default=None,
        description="[Optional] 어떤 부분을 어떻게 개선했는지 간단히 설명"
    )


def get_message_generator(message_type: MessageType) -> LlmAgent:
    description, instruction = get_message_generator_config(message_type=message_type)
    return LlmAgent(
        name="message_generator",
        model=config.writer_model,
        description=description,
        instruction=instruction,
        output_schema=MessageOutput,
        output_key=f"{message_type.value}_message"
    )

def get_enhanced_message_generator(message_type: MessageType) -> LlmAgent:
    """Creates an agent that improves messages based on evaluation feedback."""
    description, instruction = get_enhanced_message_generator_config(message_type=message_type)
    return LlmAgent(
        model=config.writer_model,
        name="enhanced_message_generator",
        description=description,
        instruction=instruction,
        output_schema=EnhancedMessageOutput,
        output_key=f"{message_type.value}_message",  # 동일한 key로 덮어쓰기
    )

