from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: int
    mtime: datetime


class FsType(Enum):
    LOCAL = "local"
    S3 = "s3"
