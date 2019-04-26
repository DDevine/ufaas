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
# WARNING: annotations can break dataclasses in 3.7, might be fixed 3.8.
# from __future__ import annotations

from asyncio import PriorityQueue, create_task, get_event_loop
from typing import Optional, Tuple

from async_timeout import timeout

from quart import Quart, request
from quart.json import jsonify
from quart.typing import ResponseValue
from quart.views import MethodView

from ufaas.tasks import (
                            PriorityQueueType, QueuesDictType,
                            create_container_coro, task_cleanup_coro,
                            task_runner_coro
                        )

BODY_TIMEOUT = 2  # Time limit for the body to be recieved.


class FnAPI(MethodView):
    """
    Function REST API.
    """

    async def get(self, id: Optional[str] = None) -> Tuple[ResponseValue, int]:
        """
        Retrieve status of job given id.
        If no `id` status of the service as JSON.
        """
        return "test", 200

    async def post(self) -> Tuple[ResponseValue, int]:
        """
        Create job, return ID.
        If `container_id` is supplied as URI parameter attempt to run job in
        that container. If container is not running, create one. This is to
        minimise container creation overhead and maximise caching.

        Returns OK, pending, success (with output?).
        """
        # Consume JSON object that specifies a fn task.
        # Temporary code for research/testing.
        async with timeout(BODY_TIMEOUT):
            complete_body = await request.get_json()
            return jsonify(complete_body), 200
        return "Not yet implemented", 501

    async def delete(self, id: Optional[str]) -> Tuple[ResponseValue, int]:
        """
        Cancel the job if `id` given.
        Clean up the container if `container_id` URI parameter given,
        when container stops.

        Returns OK, pending, success.
        """
        return "Not yet implemented", 501


async def setup_queues(app: Quart) -> QueuesDictType:
    """
    Set up the queues for handing FnTask processing.
    App context has to be copied into the handler methods so that the tasks
    can transfer tasks into the next context.
    """
    queues: QueuesDictType = dict({})

    # The create_queue holds jobs waiting to have their containers created.
    create_queue: PriorityQueueType = PriorityQueue()
    app.logger.info("Creating container creation consumer.")
    create_queue_consumer = create_task(create_container_coro(create_queue))
    queues["create"] = (create_queue_consumer, create_queue)

    # The run_queue holds jobs waiting to be run as a container exists.
    run_queue: PriorityQueueType = PriorityQueue()
    app.logger.info("Creating task runner consumer.")
    run_queue_consumer = create_task(task_runner_coro(run_queue))
    queues["run"] = (run_queue_consumer, run_queue)

    # The cleanup_queue holds jobs waiting to be cleaned up.
    cleanup_queue: PriorityQueueType = PriorityQueue()
    app.logger.info("Creating task cleanup consumer.")
    cleanup_queue_consumer = create_task(task_cleanup_coro(cleanup_queue))
    queues["cleanup"] = (cleanup_queue_consumer, cleanup_queue)

    return queues


def create_app() -> Tuple[Quart, QueuesDictType]:
    """
    Create app and setup queues.
    """
    app = Quart(__name__)

    # Register the URIs
    # NOTE: there is some strange behavior with optional parameters that needs
    # to be clarified.
    fn_view = FnAPI.as_view("fn_api")
    app.add_url_rule("/fn", methods=["POST", "GET"], view_func=fn_view)
    app.add_url_rule(
        "/fn/<id>", methods=["GET", "POST", "PUT", "DELETE"],
        view_func=fn_view
    )

    loop = get_event_loop()
    queues: QueuesDictType = loop.run_until_complete(setup_queues(app))
    return app, queues


app, queues = create_app()


@app.route('/', methods=["GET"])
async def info_page() -> Tuple[ResponseValue, int]:
    """
    Show basic status and API information, via HTML.
    """
    return "Hello", 200

if __name__ == "__main__":
    app.run()
