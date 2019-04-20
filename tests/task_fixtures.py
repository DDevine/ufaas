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
