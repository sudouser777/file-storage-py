from abc import ABCMeta
from pathlib import Path
from typing import Any


class BaseFileSystem(metaclass=ABCMeta):

    def upload_file(self, file: str | Path, **kwargs: Any) -> None:
        raise NotImplementedError()

    def download_file(self, file: str | Path, destination: str | Path, **kwargs: Any) -> None:
        raise NotImplementedError()

    def delete_file(self, file: str | Path, **kwargs: Any) -> None:
        raise NotImplementedError()
