VALID_BASIC_INLINE_TASK_SPEC = [
        {
            "version": 1.0,
            "image": "python:3.7-alpine",
            "resources": [
                {
                    "content_type": "text/python",
                    "data": "print('Hello World')",
                },
            ],
            "task_name": "hello_world",
            "cmd": ["python hello.py"],
        },
    ]
