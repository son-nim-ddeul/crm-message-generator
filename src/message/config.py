from pydantic_settings import BaseSettings, SettingsConfigDict


class MessageSettings(BaseSettings):
    # Message 도메인 전용 설정 예시
    max_message_length: int = 450

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


message_settings = MessageSettings()
