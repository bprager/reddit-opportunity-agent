from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "reddit-opportunity-radar/0.1"

    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    database_url: str = "sqlite:///./reddit_radar.db"

    def missing_reddit_credentials(self) -> list[str]:
        missing = []
        if not self.reddit_client_id:
            missing.append("REDDIT_CLIENT_ID")
        if not self.reddit_client_secret:
            missing.append("REDDIT_CLIENT_SECRET")
        if not self.reddit_user_agent:
            missing.append("REDDIT_USER_AGENT")
        return missing


settings = Settings()
