"""
ASTRAXIS-AI Core Configuration.

Uses Pydantic BaseSettings to define all engine parameters.
Settings are loaded from environment variables or .env files.
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class AstraxisSettings(BaseSettings):
    """
    Global configuration for the ASTRAXIS-AI red-teaming engine.

    Attributes:
        engine_name: Identifier tag embedded in every audit report.
        environment: Deployment mode (development, staging, production).
        max_attack_depth: Max number of recursive exploit hops per red-team run.
        sandbox_timeout_seconds: Max seconds a container sandbox can run before kill.
        risk_score_threshold: Minimum score (0.0 - 1.0) to flag as CRITICAL.
        enable_docker_sandbox: Whether to use Docker isolation or lightweight mock.
        log_level: Verbosity of structured Rich logs.
    """

    engine_name: str = Field(default="ASTRAXIS-AI v1.0", description="Engine identifier")
    environment: str = Field(default="production", description="deployment environment")
    max_attack_depth: int = Field(default=5, description="Max recursive exploit hops")
    sandbox_timeout_seconds: int = Field(default=30, description="Container kill timeout")
    risk_score_threshold: float = Field(default=0.7, description="CRITICAL risk threshold")
    enable_docker_sandbox: bool = Field(default=False, description="Enable live Docker sandbox")
    log_level: str = Field(default="INFO", description="Logging verbosity")

    class Config:
        env_prefix = "ASTRAXIS_"
        env_file = ".env"
        env_file_encoding = "utf-8"


# Module-level singleton — import this from anywhere in the project
settings = AstraxisSettings()
