from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageReferenceBase(BaseModel):
    title: str
    content: str
    category: str | None = None


class MessageReferenceCreate(MessageReferenceBase):
    pass


class MessageReferenceResponse(MessageReferenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime



class EventContent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str | None = None
    parts: list | None = None


class EventError(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    error_code: str | None = None
    error_message: str | None = None


class EventResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    event_status: str
    user_id: str
    session_id: str
    branch: str | None = None
    author: str | None = None
    timestamp: float
    is_final_response: bool | None = None
    ui_status: str | None = None # TODO: state_delta.ui_status
    content: EventContent | None = None
    error: EventError | None = None
    
class AgentRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: str
    session_id: str | None = None

class MessageAgentConfig(BaseModel):
    brand_tone: str
    message_purpose: str
    persona_id: str
    key_marketing_achievements: str | None = None
    message_sending_datetime: datetime | None = None
    product_info: str | None = None
    current_event_info: str | None = None
    additional_request: str | None = None

class MessageAgentRequest(AgentRequest):
    config: MessageAgentConfig