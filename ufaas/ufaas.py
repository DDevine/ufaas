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
from dataclasses import field
from typing import Dict, List, Optional, Tuple, Union

from async_timeout import timeout

from pydantic import PositiveInt, Required, validator
from pydantic.dataclasses import dataclass

from quart import Quart
from quart.typing import ResponseValue
from quart.views import MethodView

from ufaas.types import NameStr, ResourceType

app = Quart(__name__)
BODY_TIMEOUT = 2  # Time limit for the body to be recieved.


def main() -> None:
    app.run()


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

    @validator('image')
    def check_task_name(cls, v: str) -> None:  # noqa: N805
        if "!" in v:
            raise ValueError("Should not contain!")


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
