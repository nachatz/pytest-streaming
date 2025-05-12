from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class PulsarTestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PULSAR_")

    service_url: str = ""
    admin_url: str = ""


class PubsubTestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PUBSUB_")

    emulator_host: str = ""
    project_id: str = ""
