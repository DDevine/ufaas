Lessl - Less Server-Less
==========================
A service that accepts and runs scripts/microservices in Docker containers on demand, but with much less overhead than OpenFAAS, Fission, AWS Lambda etc.

Lessl is intended for small scale use with the intended purpose of running arbitary code in a semi-trusted environment. This means "best effort" security, but with the main goal of just mitigating accidents. It is intended to be used via a REST API primarily.

A task definition can point to the resources needed and download them, or it can embed the resources directly as text or base64, because on this scale that's likely all you want - and it's expected that the base image in docker already has the majority of requirements (eg. libraries).

The goal is for Lessl to be written in a single file and have few dependencies, because beyond that other solutions are better.


Installing and Running `lessl`
-------------------------------
::

    $ cd lessl/
    $ pip install .
    $ lessl

Design Planning / TODO
=======================

Task Specification
--------------------
TODO: JSON Schema after basic spec has been sketched out. https://app.quicktype.io/#l=schema

::

    [
        {
            "version": 1.0,
            "daemon": true,
            "image": "my_python_image",
            "ttl": 3600,
            "resources": [
                {
                    "content_type": "text/python",
                    "data": "print('Hello World')",
                    "src": "http://example.com/hello.py",
                    "dest": "/opt",
                    "mnt": "...some mount point specification for a volume."
                },
            ]
            "task_name": "hello_world",
            "pwd": "/opt",
            "env" : {"KEY": "value"}
            "cmd": ["python hello.py",],
        },
    ]

HTTP Methods
-------------
* POST - create container. (docker run...)
* PUT -  submit task to already running container. Optionally create if not running. (docker exec...)
* GET - retrieve status of container. 
* DELETE - kill/remove container.


Field Definitions
------------------
- version: The version of the task specification to use. This is 1.0.
- daemon: keep the container running. Useful if running multiple things in the same container is desired.
- image: the name of the docker image to create the container from.
- ttl: Time to Live. How many seconds until the container should be removed.
- resources: a set of resource specification objects.
    - content_type: the mimetype of the resource.
    - src: the source of the data, a uri.
    - data: the data relative to the mimetype. Binary data will be base64 encoded.
    - dest: the destination for the resource.
- task_name: A human readable name for the task.
- pwd: the working directory that the command is to be executed in.
- env: environment variables.
- cmd: a list of commands to give.


Task Response Specification
------------------------------
* Uses HTTP codes.
* Gives errors.
* Returns container ID.

Implementation Notes
-------------------------
* Quart would be good because AsyncIO can be used and it immediately gives a HTTP server.
    - No need for a REST framework. Our API should be just 4 or 5 endpoints.
* docker-python used to hook into Docker.
    - If deployed in a docker container then it will have to expose the host's docker sock.
* Apparently there is a smaller/faster Python image than the official Alpine images - https://www.revsys.com/tidbits/optimized-python/