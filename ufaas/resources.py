from typing import Optional

from pydantic.dataclasses import dataclass


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
