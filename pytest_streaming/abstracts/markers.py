from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from typing import Generator
from typing import cast

from _pytest.nodes import Node
from pytest import Config
from pytest import FixtureRequest
from pytest import Mark


class BaseMarker(ABC):
    config: Config
    request: FixtureRequest
    marker_name: str
    marker_description: str
    marker_params: list[str]

    def __init__(self, config: Config, request: FixtureRequest) -> None:
        self.config = config
        self.request = request

    @classmethod
    def definition(cls) -> str:
        params = ", ".join(cls.marker_params)
        return f"{cls.marker_name}({params})"

    @property
    def node(self) -> Node:
        return cast(Node, self.request.node)

    @property
    def marker(self) -> Mark | None:
        return self.node.get_closest_marker(self.marker_name)

    @abstractmethod
    @contextmanager
    def impl(self) -> Generator[None, None, None]: ...

    """This is the entry point for all markers. When a marker
    is added to the context of the plugin, these are ran by default
    for each valid implementation built.
    
    See `_markers` in the `plugin` entrypoint.
    """
