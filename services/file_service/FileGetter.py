import os
from abc import abstractmethod

from fastapi import HTTPException


class FileGetter:
    @abstractmethod
    def get_path(self, filename: str):
        pass


class LocalFileGetter(FileGetter):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_path(self, filename: str) -> str:
        path = os.path.join(self.base_path, filename)
        real_path = os.path.realpath(path)
        if not real_path.startswith(os.path.realpath(self.base_path)):
            raise HTTPException(status_code=403, detail="Path Traversal Detected")
        return real_path


getter: FileGetter = LocalFileGetter('./covers/')
