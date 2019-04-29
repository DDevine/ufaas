Notes
======

TODO
-----
* aiodocker doesn't work because it has no concept of exec.
    * docker python API doesn't suit us because it is a blocking API.
    * Will have to use AIOhttp or Requests-async to wait on IO.
    * The problem with threading is that it will blow out the server resources as 
    the resources are cloned.
* Make Task.image types so that a hub spec string, tarball, git, http, path
* Add image pre-load, because these may take a while to load. Cold starts and warm starts.
    * Track last used etc. so that old ones can be purged.
    * Provide way to trigger update, etc.
* Create separte management library - provide/register scripts, provide easy way
    to sync whole library in one go to bring up services etc.
* Use Pydantic to output OpenAPI schema.
* Docker deployment image
* Docs

Minimal clustering support? 
-----------------------------
* Is there and easy/simple upgrade path into Docker swarm?
    - People are going to have their own scaling solution, just make sure it is ready to work within a swarm?
* Can we just design around this and use Nginx load balancing/sticky redirects?



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
