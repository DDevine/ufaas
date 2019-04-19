Lessl - Less Server-Less
==========================
A service that accepts and runs scripts/microservices in Docker containers on demand, but with much less overhead than OpenFAAS, Fission, AWS Lambda etc.

Lessl is intended for small scale use with the intended purpose of running arbitary code in a semi-trusted environment. This means "best effort" security, but with the main goal of just mitigating accidents. It is intended to be used via a REST API primarily.

A task definition can point to the resources needed and download them, or it can embed the resources directly as text or base64, because on a small scale that's likely all you want. It's expected that the docker image already has the majority of dependencies for the task.

The goal is for Lessl to be as small as possible, trivial to install/integrate and have few dependencies, because beyond that other solutions are better (eg. OpenFAAS).


Installing and Running `lessl`
-------------------------------
::

    $ cd lessl/
    $ pip install .
    $ lessl