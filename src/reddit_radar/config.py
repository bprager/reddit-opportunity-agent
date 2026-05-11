from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "reddit-opportunity-radar/0.1"

    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    database_url: str = "sqlite:///./reddit_radar.db"

    class Config:
        env_file = ".env"


settings = Settings()
