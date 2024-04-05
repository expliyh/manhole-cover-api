import json
import os
from abc import abstractmethod
from typing import Tuple

from fastapi import HTTPException


class FileGetter:
    @abstractmethod
    def get_path(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_path_and_name(self, filename: str) -> Tuple[str, str]:
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

    def get_path_and_name(self, filename: str) -> Tuple[str, str]:
        real_path = self.get_path(filename)
        if os.path.splitext(filename)[1] != '.json':
            return real_path, filename
        file = json.load(fp=open(real_path, encoding='utf-8'))
        return real_path, file['real_name']


getter: FileGetter = LocalFileGetter('./covers/')
