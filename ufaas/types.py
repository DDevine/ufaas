from typing import Union

from pydantic import ConstrainedStr

from ufaas.resources import (GenericMountResource, TextResource,
                             TmpfsResource, URIResource)

# Type alias used to accept all the resources for a Task.
ResourceType = Union[
    TextResource,
    URIResource,
    GenericMountResource,
    TmpfsResource
]


class NameStr(ConstrainedStr):
    min_length = 1
    max_length = 127
