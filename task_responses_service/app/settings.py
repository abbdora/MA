from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_host: str = "responses_postgres"
    postgres_port: int = 5432
    postgres_db: str = "responses_db"
    postgres_user: str = "postgres"
    postgres_password: str = "12345"

    secret_key: str = "my-super-secret-key-for-responses"
    algorithm: str = "HS256"

    auth_service_url: str = "http://localhost:8000"

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()