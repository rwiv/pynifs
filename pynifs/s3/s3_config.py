from pydantic import BaseModel, Field, constr


class S3Config(BaseModel):
    name: constr(min_length=1)
    endpoint_url: constr(min_length=1) = Field(alias="endpointUrl")
    access_key: constr(min_length=1) = Field(alias="accessKey")
    secret_key: constr(min_length=1) = Field(alias="secretKey")
    verify: bool
    bucket_name: constr(min_length=1) = Field(alias="bucketName")
