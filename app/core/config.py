from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    video_source_type: str = "static"
    video_source_path: str = "data/videos/test-1.mp4"

    class Config:
        env_file = ".env"


settings = Settings()
