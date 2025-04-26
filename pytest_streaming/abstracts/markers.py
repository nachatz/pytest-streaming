from pytest import Config, Mark
from pytest import FixtureRequest
from _pytest.nodes import Node

from typing import Generator
from pydantic import BaseModel
from abc import abstractmethod
from contextlib import contextmanager

class AbstractMarker(BaseModel):

    config: Config
    request: FixtureRequest
    marker_name: str = ""
    marker_description: str = ""
    marker_params: list[str] = []

    @classmethod
    def definition(cls) -> str:
        params = ", ".join(cls.marker_params)
        return f"{cls.marker_name}({params})"

    @property
    def node(self) -> Node:
        return self.request.node

    @property
    def marker(self) -> Mark | None:
        return self.node.get_closest_marker(self.marker_name)

    @abstractmethod
    @contextmanager
    def impl(self) -> Generator[None, None, None]:
        raise NotImplementedError("Subclasses must implement this method")