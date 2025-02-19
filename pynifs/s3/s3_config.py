from pydantic import BaseModel, Field


class S3Config(BaseModel):
    name: str = Field(min_length=1)
    endpoint_url: str = Field(min_length=1, alias="endpointUrl")
    access_key: str = Field(min_length=1, alias="accessKey")
    secret_key: str = Field(min_length=1, alias="secretKey")
    verify: bool
    bucket_name: str = Field(min_length=1, alias="bucketName")
