from asyncio import PriorityQueue, Queue, Task
from dataclasses import field
from enum import Flag, auto
from typing import Dict, List, Optional, TYPE_CHECKING, Tuple, Union

from pydantic import ConstrainedStr, PositiveInt, Required, validator
from pydantic.dataclasses import dataclass


class TaskState(Flag):
    """
    The state of a FnTask. It is a Flag type enum, so states can be compound
    eg. FAILED | CLEANED

    """
    RECEIVED = auto()  # Task is new, just received, nothing done yet.
    FAILED = auto()  # Task failed. Error occured.
    EXPIRED = auto()  # Task was cancelled due to a timeout of some type.
    CANCELLED = auto()  # Task cancelled, not neccessarily due to error.
    PENDING = auto()  # Task waiting to be run.
    STARTING = auto()  # Task environment being allocated.
    RUNNING = auto()  # Task Executing.
    FINISHED = auto()  # Task finished executing.

    BUILDING = auto()  # Container is being created.
    CLEANED = auto()  # Resources from task have been cleaned up.
    INITIIALISED = auto()  # Container has been created.


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
class FnTask:
    pwd: str = "."
    task_name: NameStr = Required
    image: NameStr = Required
    cmd_list: List[str] = field(default_factory=list)
    # Members of resource_list are mapped to their types automatically. Magic.
    resource_list: List[ResourceType] = field(default_factory=list)
    is_daemon: bool = False
    ttl: Optional[PositiveInt] = None
    rm: bool = False
    env: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    state: TaskState = field(default=TaskState.RECEIVED, repr=False)

    @validator("image")
    def check_image_name(cls, v: str) -> str:  # noqa: N805
        if "!" in v:
            raise ValueError("Name cannot contain '!'")
        return v

    @validator("task_name")
    def check_task_name(cls, v: str) -> str:  # noqa: N805
        v = v.replace(' ', '_')
        return v


# Note that Some classes are declared as generic in stubs, but not at runtime.
# The solution is to have a version for type checkers and a separate runtime
# compatible version. Else you will see an error like:
#    TypeError: 'type' object is not subscriptable
# https://mypy.readthedocs.io/en/latest/common_issues.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime

if TYPE_CHECKING:
    PriorityQueueType = PriorityQueue[Tuple[int, FnTask]]
    QueueTypes = Union[Queue[FnTask], PriorityQueueType]

    # A dictionary like:
    # {"consumer_name", (consumer_task: asyncio.Task, queue: Queue)}
    # Task is considered a container type and it has a Queue as an argument.
    QueuesDictType = Dict[
                str, Tuple[
                        Task[QueueTypes],
                        QueueTypes
                    ]
                ]
else:
    PriorityQueueType = PriorityQueue
    QueueTypes = Queue
    QueuesDictType = Dict


async def create_container_coro(queue: PriorityQueueType) -> None:
    """
    Wait for Tasks to enter the queue, create the containers and
    queue them up for running.
    """
    while True:
        await queue.get()


async def task_runner_coro(queue: PriorityQueueType) -> None:
    """
    Wait for Tasks to enter the queue, run the tasks.
    """
    while True:
        await queue.get()


async def task_cleanup_coro(queue: PriorityQueueType) -> None:
    """
    Wait for Tasks to enter the queue, cleanup the container/image.
    """
    while True:
        await queue.get()
