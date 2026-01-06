from enum import Enum

class MessageType(str, Enum):
    ASPIRATIONAL_DREAMER = "aspirational_dreamer"
    EMPATHETIC_SUPPORTER = "empathetic_supporter"
    PLAYFUL_ENTERTAINER = "playful_entertainer"
    RATIONAL_ADVISOR = "rational_advisor"

    @classmethod
    def get_message_type(cls, agent_name: str) -> "MessageType":
        if cls.ASPIRATIONAL_DREAMER.value in agent_name:
            return cls.ASPIRATIONAL_DREAMER
        if cls.EMPATHETIC_SUPPORTER.value in agent_name:
            return cls.EMPATHETIC_SUPPORTER
        if cls.PLAYFUL_ENTERTAINER.value in agent_name:
            return cls.PLAYFUL_ENTERTAINER
        if cls.RATIONAL_ADVISOR.value in agent_name:
            return cls.RATIONAL_ADVISOR
        raise ValueError(f"Invalid agent name: {agent_name}")
