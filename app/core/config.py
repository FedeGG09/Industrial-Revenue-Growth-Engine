from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Industrial Revenue & Growth Engine"
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    mssql_host: str = "sqlserver"
    mssql_port: int = 1433
    mssql_db: str = "irge"
    mssql_user: str = "sa"
    mssql_password: str = ""
    mssql_driver: str = "ODBC Driver 18 for SQL Server"

    chroma_host: str = "chroma"
    chroma_port: int = 8000
    chroma_collection_leads: str = "industrial_leads"
    chroma_collection_policies: str = "industrial_policies"

    llm_backend: str = "transformers"
    hf_model_id: str = "mistralai/Mistral-7B-Instruct-v0.3"
    hf_token: str | None = None
    use_4bit: bool = True
    use_8bit: bool = False
    max_new_tokens: int = 512

    prometheus_enabled: bool = True
    log_level: str = "INFO"


settings = Settings()
