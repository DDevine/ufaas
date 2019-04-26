MicroFaaS - FaaS without the faff.
======================================================
MicroFaaS is a service that accepts and runs code in Docker containers on demand, but with much less overhead than OpenFAAS, Fission, AWS Lambda etc.

MicroFaaS (or ufaas) is intended for small scale use with the intended purpose of running arbitary code in a semi-trusted environment. This means "best effort" security, but with the main goal of just mitigating accidents. It is intended to be used via a REST API primarily.

A task definition can point to the resources needed and download them, or it can embed the resources directly as text or base64, because on a small scale that's likely all you want. It's expected that the docker image already has the majority of dependencies for the task.

The goal is for MicroFAAS to be as small as possible, trivial to install/integrate and have few dependencies, because beyond that other solutions are better (eg. OpenFAAS). Some basic scaling approaches should also emerge in time (eg. Swarm compatibility).


Installing and Running MicroFaaS
---------------------------------
::

    $ pip install ufaas/
    $ ufaas

Running Tests
---------------
Testing can be automatically set up and run using Tox.
::

    $ cd ufaas/
    $ tox

API - Under Development
===========================

========  ========================  ===========================================
Method     URI                      Description
========  ========================  ===========================================
GET       /fn                       Lists running function containers.
GET       /fn/{uuid: id}            Shows information for running function
                                    given `id`.
POST      /fn                       Create a function given a definition.
POST      /fn/{uuid: id}            Create a function in the same container as
                                    recently used for function identified by 
                                    `id`. Used for locality/caching reasons.
PUT       /fn/{uuid: id}            Update a pending function given `id`.
DELETE    /fn/{uuid: id}            Stop/cancel a function given `id`.
                                    URI parameters can be used to indicate
                                    any clean-up options.
OPEN      /fn/ws                    Open WebSockets API. This is expected to 
                                    provide asynchronous notifications and
                                    further functionality.
========  ========================  ===========================================

* JSON Task spec is under heavy development as there are many unknowns. Current examples are in `tests/` and more implementation details in `ufaas/tasks.py`.