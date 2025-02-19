from abc import abstractmethod, ABC
from io import IOBase
from typing import Callable

from .types import FileInfo


class FsAccessor(ABC):
    @abstractmethod
    def normalize_base_path(self, base_path: str) -> str:
        pass

    @abstractmethod
    def head(self, path: str) -> FileInfo | None:
        pass

    def exists(self, path: str) -> bool:
        if self.head(path) is not None:
            return True
        return False

    @abstractmethod
    def mkdir(self, dir_path: str):
        pass

    @abstractmethod
    def rmdir(self, dir_path: str):
        pass

    @abstractmethod
    def get_list(self, dir_path: str) -> list[FileInfo]:
        pass

    @abstractmethod
    def read(self, path: str) -> IOBase:
        pass

    @abstractmethod
    def write(self, path: str, data: bytes | IOBase):
        pass

    @abstractmethod
    def delete(self, path: str):
        pass

    def walk(self, file: FileInfo, cb: Callable[[FileInfo], None]):
        path = file.path
        if file.is_dir is False:
            cb(file)
        children = self.get_list(path)
        for c in children:
            if c.is_dir is False:
                cb(c)
            else:
                self.walk(c, cb)
