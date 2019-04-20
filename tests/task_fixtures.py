VALID_TASK_BASIC = {
    "task_name": "my_task",
    "image": "python3:alpine",
    "pwd": "/opt",
    "cmd_list": [
        "python"
    ],
    "resource_list": [
        {
            "data": 'print("hello world")',
            "dest": "hello.py"
        },
    ],
    "is_daemon": False,
    "ttl": 60,
    "env": {
       "FOO": "bar"
    }
}

INVALID_TASK_BASIC = {
    "foo": "bar"
}

INVALID_TASK_NAME_TOO_LONG = {
    "task_name": "C" * 130,
    "image": "python3:alpine",
    "pwd": "/opt",
    "cmd_list": [
        "python"
    ],
    "resource_list": [
        {
            "data": 'print("hello world")',
            "dest": "hello.py"
        },
    ],
    "is_daemon": False,
    "ttl": 60,
    "env": {
       "FOO": "bar"
    }
}
