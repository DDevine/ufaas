"""
MicroFaaS - FaaS without the faff.
Provides functions as a service on a small scale using Docker.

Copyright 2019 Daniel Devine

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from dataclasses import InitVar, field
from typing import Any, Dict, List, Optional, Tuple, Union

from async_timeout import timeout

from pydantic import ValidationError, validator
from pydantic.dataclasses import dataclass

from quart import Quart
from quart.typing import ResponseValue
from quart.views import MethodView

app = Quart(__name__)
BODY_TIMEOUT = 2  # Time limit for the body to be recieved.


def main() -> None:
    app.run()


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


class TaskConfig:
    """
    The InitVar type in `Task` is not supported by Pydantic.
    `arbitrary_types_allowed` is the workaround.
    """
    arbitrary_types_allowed = True


@dataclass(config=TaskConfig)  # type: ignore
class Task:
    """
    `resource_init` is used to populate resource_list after validation.
    """
    task_name: str
    image: str
    pwd: str
    cmd_list: List[str] = field(default_factory=list)
    resource_init: InitVar[List[Any]] = field(init=False, default=[])
    resource_list: List[ResourceType] = field(default_factory=list)
    is_daemon: bool = False
    ttl: Optional[int] = None
    env: Dict[str, Union[str, int, float]] = field(default_factory=dict)

    def __post_init__(self, resource_init: List[Any]) -> None:
        """Init is needed because resource_list has to be processed."""
        for res in resource_init:
            try:
                self.resource_list.append(TextResource(**res))
            except ValidationError:
                try:
                    self.resource_list.append(URIResource(**res))
                except ValidationError:
                    try:
                        self.resource_list.append(
                            GenericMountResource(**res)
                        )
                    except ValidationError:
                        try:
                            self.resource_list.append(
                                TmpfsResource(**res)
                            )
                        except ValidationError:
                            # TODO: Probably not the right way to handle this.
                            continue

    @validator('task_name')
    def _task_name(cls, v: str) -> None:  # noqa: N805
        if len(v) > 127:
            raise ValidationError("`task_name` must not be longer than 127 \
                chars.")


@app.route('/', methods=["GET"])
async def info_page() -> Tuple[ResponseValue, int]:
    """
    Show basic status and API information, via HTML.
    """
    return "Hello", 200


class FnAPI(MethodView):
    """
    Function REST API.
    """

    async def get(self, id: Optional[str]) -> Tuple[ResponseValue, int]:
        """
        Retrieve status of job given id.
        If no `id` status of the service as JSON.
        """
        return "test", 200

    async def post(self, id: Optional[str]) -> Tuple[ResponseValue, int]:
        """
        Create job, return ID.
        If `id` is supplied attempt to run job in the same container. If
        container is not running, create one. This is to minimise container
        creation overhead and maximise caching.

        Returns OK, pending, success (with output).
        """
        # Consume JSON object that specifies a fn task.
        async with timeout(BODY_TIMEOUT):
            async for data in request.body:  # type: ignore # noqa: F821
                return "data recieved: %s" % data, 200
        return "Not yet implemented", 501

    async def delete(self, id: Optional[str]) -> Tuple[ResponseValue, int]:
        """
        Cancel the job.
        Accept URL params to clean up the container.

        Returns OK, pending, success.
        """
        return "Not yet implemented", 501


# Register the URIs
fn_view = FnAPI.as_view("fn_api")
app.add_url_rule(
    "/fn/", defaults={"id": None}, view_func=fn_view, methods=["GET"],
)
app.add_url_rule(
    "/fn/<id>", defaults={"id": None},
    view_func=fn_view, methods=["GET", "POST", "DELETE"],
)

if __name__ == "__main__":
    main()
