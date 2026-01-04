from google.adk.agents import LlmAgent
from google.adk.apps import App
from .sub_agents.message_generate_pipeline.agent import message_generate_pipeline_agent
from agents.config import config

from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

from agents.service import find_persona_by_id, format_persona

from dotenv import load_dotenv
load_dotenv()


def set_state(callback_context: CallbackContext) -> Optional[types.Content]:
    persona_id = callback_context.state.get("persona_id")
    if persona_id is None:
        callback_context.state["persona"] = "target persona is None"
        return None
    
    persona = find_persona_by_id(persona_id=persona_id)
    if persona is None:
        callback_context.state["persona"] = "target persona is None"
        return None
    
    formatted_persona = format_persona(persona=persona)
    callback_context.state["persona"] = formatted_persona

    return None
   
# TODO 1. Sequential Agent 로 수정
# TODO 2. 주요 메시지 성과, 예상 발송일 기반 RAG 조회 에이전트 추가
root_agent = LlmAgent(
    name="message_generator",
    model=config.worker_model,
    description="고객의 요청에 따라 마케팅 메시지를 생성한다.",
    instruction="당신은 고객의 마케팅 메시지 생성 요청에 따라 메시지를 작성하는 전문가입니다. 'message_generate_pipeline' sub agents를 통해 마케팅 메시지를 생성하세요.",
    sub_agents=[message_generate_pipeline_agent],
    before_agent_callback=set_state
)

app = App(root_agent=root_agent, name="message")

def get_app_name() -> str:
    return "message"