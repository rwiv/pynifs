import os
import shutil
from datetime import datetime
from io import IOBase
from pathlib import Path

from ..abstract import FsAccessor
from ..types import FileInfo, FsType
from ..utils import path_join


class LocalFsAccessor(FsAccessor):
    def __init__(self, chunk_size=4096):
        super().__init__(FsType.LOCAL)
        self.chunk_size = chunk_size

    def normalize_base_path(self, base_path: str) -> str:
        return base_path

    def head(self, path: str) -> FileInfo | None:
        p = Path(path)
        if not p.exists():
            return None
        return FileInfo(
            name=p.name,
            path=path,
            is_dir=p.is_dir(),
            size=p.stat().st_size,
            mtime=datetime.fromtimestamp(os.path.getmtime(path)),
        )

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def get_list(self, dir_path: str) -> list[FileInfo]:
        names = os.listdir(dir_path)
        result = []
        for name in names:
            file = self.head(path_join(dir_path, name))
            if file is not None:
                result.append(file)
        return result

    def mkdir(self, dir_path: str):
        os.makedirs(dir_path, exist_ok=True)

    def rmdir(self, dir_path: str):
        if dir_path == "" or dir_path == "/":
            raise ValueError("Cannot remove root directory")
        if Path(dir_path).exists() is False:
            raise FileNotFoundError("No such file or directory: '%s'" % dir_path)
        shutil.rmtree(dir_path)

    def read(self, path: str) -> IOBase:
        file_obj = open(path, "rb")
        if isinstance(file_obj, IOBase):
            return file_obj
        else:
            raise TypeError("Expected file object, got %s" % type(file_obj))

    def write(self, path: str, data: bytes | IOBase):
        with open(path, "wb") as f:
            if isinstance(data, bytes):
                f.write(data)
            elif isinstance(data, IOBase):
                while True:
                    chunk = data.read(self.chunk_size)
                    if not data:
                        break
                    f.write(chunk)

    def delete(self, path: str):
        info = self.head(path)
        if info is None:
            raise FileNotFoundError("No such file or directory: '%s'" % path)
        if info.is_dir:
            os.rmdir(path)
        else:
            os.remove(path)
