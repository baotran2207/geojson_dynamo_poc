from pydantic import BaseSettings, SecretStr
import os


class AppSettings(BaseSettings):
    # Security
    default_username =  os.getenv("SecretStr", "baotran")
    default_password =  os.getenv("SecretStr", "123")
    secret_key: str = os.getenv("SecretStr", "randomsecret")
    jwt_token_prefix: str = "Bearer"  # token? Bearer ?

    # Dynamo
    DYNAMO_USER_TABLE_NAME:str = os.environ.get('DYNAMO_USER_TABLE_NAME', 'geo_poc_user')
    DYNAMO_FEATURES_TABLE_NAME:str = os.environ.get('DYNAMO_FEATURES_TABLE_NAME', 'geo_poc_feature')
    DYNAMODB_STREAM_ARN:str = os.environ.get('DYNAMODB_STREAM_ARN', '')


settings = AppSettings()