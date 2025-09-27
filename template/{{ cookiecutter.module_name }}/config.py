"""Configuration management using Pydantic and environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

####################################################################################
# Make sure to match the the naming in the env file with the settings variable name
# So DATA_DIR -> data_dir and NOT DATA_DIR -> data_dir_path
####################################################################################

DOTENV = os.path.join(os.path.dirname(Path(__file__).parent), ".env")

# Load the .env file
load_dotenv(dotenv_path=DOTENV, override=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project paths
    project_dir: Path = Field(
        default=Path(__file__).parent.parent,
        description="Root directory of the project",
    )
    data_dir: Path = Field(
        default=None, description="Directory containing data files", env="DATA_DIR"
    )
    raw_dir: Path = Field(
        default=None,
        description="Directory containing the raw data files",
        env="RAW_DIR",
    )
    processed_dir: Path = Field(
        default=None,
        description="Directory containing the processed data files",
        env="PROCESSED_DIR",
    )
    output_dir: Path = Field(
        default=None, description="Directory for output files", env="OUTPUT_DIR"
    )

    # API configurations
    api_key: str | None = Field(
        default=None, description="API key for external services", env="API_KEY"
    )

    # Database configurations
    db_url: str | None = Field(
        default=None, description="Database connection URL", env="DATABASE_URL"
    )

    db_user: str | None = Field(
        default=None, description="Database user name", env="DATABASE_USER"
    )

    db_password: str | None = Field(
        default=None, description="Database user password", env="DATABASE_PASSWORD"
    )

    db_name: str | None = Field(
        default=None, description="Database name", env="DATABASE_NAME"
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level", env="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=DOTENV, env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set default paths if not provided in environment
        if self.data_dir is None:
            self.data_dir = self.project_dir / "data"
        if self.output_dir is None:
            self.output_dir = self.project_dir / "output"

        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


# Create global settings instance
settings = Settings()
