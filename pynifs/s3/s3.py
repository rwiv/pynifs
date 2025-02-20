from io import IOBase
from typing import Any

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client

from .s3_config import S3Config
from .s3_responses import S3ObjectInfoResponse, S3ListResponse
from .s3_utils import to_dir_path
from ..abstract import FsAccessor
from ..types import FileInfo, FsType
from ..utils import filename


class S3FsAccessor(FsAccessor):
    def __init__(self, config: S3Config):
        super().__init__(FsType.S3)
        self.config = config
        self.bucket_name = config.bucket_name
        self.__s3 = self.__get_client()

    def normalize_base_path(self, base_path: str) -> str:
        return filename(base_path, "/")

    def head(self, path: str) -> FileInfo | None:
        file_head = self.__head(path)
        if file_head is not None:
            return file_head
        dir_head = self.__head(to_dir_path(path))
        if dir_head is not None:
            return dir_head
        return None

    def __head(self, path: str) -> FileInfo | None:
        try:
            s3_res = self.__s3.head_object(Bucket=self.bucket_name, Key=path)
            return S3ObjectInfoResponse.new(s3_res, key=path).to_file_info()
        except ClientError as e:
            res: Any = e.response
            if res["Error"]["Code"] == "404":
                return None
            else:
                raise e

    def get_list(self, dir_path: str) -> list[FileInfo]:
        keys = self.__get_keys(dir_path)
        result = []
        for k in keys:
            info = self.head(k)
            if info is not None:
                result.append(info)
        return result

    def __get_keys(self, dir_path: str) -> list[str]:
        s3_res = self.__s3.list_objects_v2(
            Bucket=self.bucket_name, Prefix=to_dir_path(dir_path), Delimiter="/"
        )
        res = S3ListResponse.new(s3_res)
        result = []
        if res.prefixes:
            for o in res.prefixes:
                if o.prefix == to_dir_path(dir_path):
                    continue
                result.append(o.prefix)
        if res.contents:
            for o in res.contents:
                if o.key == to_dir_path(dir_path):
                    continue
                result.append(o.key)
        return result

    def all(self):
        s3_res = self.__s3.list_objects_v2(Bucket=self.bucket_name, Prefix="")
        res = S3ListResponse.new(s3_res)
        result = []
        if res.contents:
            for o in res.contents:
                result.append(o.to_file_info())
        return result

    def mkdir(self, dir_path: str):
        self.__s3.put_object(Bucket=self.bucket_name, Key=to_dir_path(dir_path))

    def rmdir(self, dir_path: str):
        children = self.get_list(dir_path)
        if len(children) > 0:
            for c in children:
                if c.is_dir:
                    self.rmdir(c.path)
                else:
                    self.delete(c.path)
        if dir_path == "" or dir_path == "/":
            return
        self.delete(to_dir_path(dir_path))

    def read(self, path: str) -> IOBase:
        res = self.__s3.get_object(Bucket=self.bucket_name, Key=path)
        return res["Body"]

    def write(self, path: str, data: bytes | IOBase):
        if isinstance(data, bytes):
            self.__s3.put_object(Bucket=self.bucket_name, Key=path, Body=data)
        elif isinstance(data, IOBase):
            self.__s3.upload_fileobj(data, self.bucket_name, path)  # type: ignore

    def delete(self, path: str):
        self.__s3.delete_object(Bucket=self.bucket_name, Key=path)

    def __get_client(self) -> S3Client:
        return boto3.client(
            "s3",
            endpoint_url=self.config.endpoint_url,
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            verify=self.config.verify,
        )
