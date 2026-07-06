from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str 
    cors_allowed_origin: list[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL="_",
        cors_allowed_origin= ['http://localhost:3000'],
    )