from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    elasticsearch_url: str
    elasticsearch_index: str = "documents"
    elasticsearch_user: str = "elastic"
    elasticsearch_password: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
