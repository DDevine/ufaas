from dataclasses import field
from typing import Dict, List, Optional, Union

from pydantic import ConstrainedStr, PositiveInt, Required, validator
from pydantic.dataclasses import dataclass


class NameStr(ConstrainedStr):
    min_length = 1
    max_length = 127


@dataclass
class TextResource:
    """
    Resource that is provided as raw text. (eg. a raw Python script).
    """
    data: str
    dest: str
    content_type: str = "text/plain"


@dataclass
class URIResource:
    """
    Resource that is fetched from a URI.
    """
    uri: str
    dest: str


@dataclass
class BindResource:
    """
    Resource that is a Docker bind mount
    """
    src: str
    target: str
    readonly: bool = True
    propagation: Optional[str] = None


@dataclass
class GenericMountResource:
    """
    Resource for specifying a generic Docker mount, takes a string so that
    complicated mounts such as Volumes with specific drivers can be specified.
    """
    mount_csv: str


@dataclass
class TmpfsResource:
    """
    Create a tmpfs mount.
    """
    dest: str
    size: Optional[int] = None
    mode: str = "1777"


# Type alias used to accept all the resources for a Task.
ResourceType = Union[
    TextResource,
    URIResource,
    GenericMountResource,
    TmpfsResource
]


@dataclass()
class Task:
    pwd: str = "."
    task_name: NameStr = Required
    image: NameStr = Required
    cmd_list: List[str] = field(default_factory=list)
    # Members of resource_list are mapped to their types automatically. Magic.
    resource_list: List[ResourceType] = field(default_factory=list)
    is_daemon: bool = False
    ttl: Optional[PositiveInt] = None
    env: Dict[str, Union[str, int, float]] = field(default_factory=dict)

    @validator("image")
    def check_image_name(cls, v: str) -> str:  # noqa: N805
        if "!" in v:
            raise ValueError("Name cannot contain '!'")
        return v

    @validator("task_name")
    def check_task_name(cls, v: str) -> str:  # noqa: N805
        v = v.replace(' ', '_')
        return v
