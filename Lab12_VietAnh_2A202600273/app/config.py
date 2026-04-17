from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Cấu hình Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Cấu hình Security
    AGENT_API_KEY: str = "demo-key-change-me"
    
    # Cấu hình Redis (Stateless state)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Cấu hình Logging & Monitoring
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_PER_MINUTE: int = 10
    MONTHLY_BUDGET_USD: float = 10.0
    
    # Cho phép đọc từ file .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

