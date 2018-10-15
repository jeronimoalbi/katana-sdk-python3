KUSANAGI SDK for Python 3
=======================

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python 3 SDK to interface with the **KUSANAGI**™ framework (https://kusanagi.io).

Requirements
------------

* KUSANAGI Framework 0.1+
* [Python](https://www.python.org/downloads/) 3.4+
* [libzmq](http://zeromq.org/intro:get-the-software) 4.1.5+

Installation
------------

Enter the following command to install the SDK in your local environment:

```
$ pip install kusanagi-sdk-python3
```

To run all unit tests or code coverage install requirements first:

```
$ pip install -r pip-requirements.txt
```

And then run all unit test with the command:

```
$ pytest --cache-clear
```

Or, for code coverage, use the command:

```
$ pytest -q --cov=kusanagi --cov-report=term
```

Getting Started
---------------

To start using the **KUSANAGI** SDK for **Python 3** we'll create a **Middleware** that handles requests and responses, and then a simple **Service**.

First, define the configuration files for the example **Middleware** and **Service**.

**KUSANAGI** configurations can be defined as *XML*, *YAML* or *JSON*.
For these examples we'll use *YAML*.

Create a new config file for the **Middleware** as the following:

```yaml
"@context": urn:kusanagi:middleware
name: example
version: "0.1"
request: true
response: true
info:
  title: Example Middleware
engine:
  runner: urn:kusanagi:runner:python3
  path: ./middleware-example.py
```

Now, save the config as `middleware-example.yaml`.

Next, create a config file for the **Service** as the following:

```yaml
"@context": urn:kusanagi:service
name: users
version: "0.1"
http-base-path: /0.1
info:
  title: Example Users Service
engine:
  runner: urn:kusanagi:runner:python3
  path: ./service-users.py
action:
  - name: read
    http-path: /users/{id}
    param:
      - name: id
        type: integer
        http-input: path
        required: true
```

Now, save the config as `service-users.yaml`.

With the configuration files written we've now modelled our components.

Next, we'll create a python module that defines the **Middleware** component:

```python
import json

from kusanagi.logging import INFO
from kusanagi.sdk import Middleware


def request_handler(request):
    return request


def response_handler(response):
    return response


if __name__ == '__main__':
    middleware = Middleware()
    middleware.request(request_handler)
    middleware.response(response_handler)
    middleware.run()
```

Now, save the module as `middleware-example.py`.

This module defines a **Middleware** that processes requests and also responses, so it's called two times per request.

The `request_handler` is called first, before any **Service** call, so there we have to set the **Service** name, version and action to call.

To do so, change the `request_handler` function to the following:

```python
def request_handler(request):
    http_request = request.get_http_request()
    path = http_request.get_url_path()
    request.log('Pre-processing request to URL {}'.format(path), INFO)

    # These values would normally be extracted by parsing the URL
    request.set_service_name('users')
    request.set_service_version('0.1')
    request.set_action_name('read')
    return request
```

This calls the *read* action for version *0.1* of the users **Service** for every request.

The `response_handler` is called at the end of the request/response lifecycle, after the **Service** call finishes.

For the example, all responses will be formatted as JSON. To do so, change the `response_handler` function to the following:

```python
def response_handler(response):
    # Get the data returned by the called service using the transport API
    contents = None
    transport = response.get_transport()
    origin = transport.get_origin_service()
    for service in transport.get_data():
        # Check that the service is the called service
        if service.get_name() != origin[0] or service.get_version() != origin[1]:
            continue

        for action in service.get_actions():
            # Check that the action is the called service action
            if action.get_name() != origin[2]:
                continue

            # The the data returned by the service
            contents = action.get_data()

    # Serialize transport to JSON and use it as response body
    if contents:
        body = json.dumps(contents)
        http_response = response.get_http_response()
        http_response.set_header('Content-Type', 'application/json')
        http_response.set_body(body)

    return response
```

At this point there is a complete **Middleware** defined, so the next step is to define a **Service**.

Create a new python module that defines the **Service** as the following:

```python
from kusanagi.sdk import Service


def read_handler(action):
    user_id = action.get_param('id').get_value()

    # Users read action returns a single user entity
    action.set_entity({
        'id': user_id,
        'name': 'foobar',
        'first_name': 'Foo',
        'last_name': 'Bar',
    })
    return action


if __name__ == '__main__':
    service = Service()
    service.action('read', read_handler)
    service.run()
```

Now, save the module as `service-users.py`.

At this point you can add the **Middleware** to the **Gateway** config and run the example
and make a request to the URL path `/0.1/users/1` to get a response.

Happy hacking!!

Documentation
-------------

See the [API](https://kusanagi.io#kusanagi/docs/sdk) for a technical reference of the SDK.

For help using the framework see the [documentation](https://kusanagi.io#kusanagi/docs).

Support
-------

Please first read our [contribution guidelines](https://kusanagi.io#kusanagi/open-source/contributing).

* [Requesting help](https://kusanagi.io#kusanagi/open-source/help)
* [Reporting a bug](https://kusanagi.io#kusanagi/open-source/bug)
* [Submitting a patch](https://kusanagi.io#kusanagi/open-source/patch)
* [Security issues](https://kusanagi.io#kusanagi/open-source/security)

We use [milestones](https://github.com/kusanagi/kusanagi-sdk-python3/milestones) to track upcoming releases inline with our [versioning](https://kusanagi.io#kusanagi/docs/framework/versions) strategy, and as defined in our [roadmap](https://kusanagi.io#kusanagi/docs/framework/roadmap).

For commercial support see the [solutions](https://kusanagi.io/solutions) available or [contact us](https://kusanagi.io/contact) for more information.

Contributing
------------

If you'd like to know how you can help and support our Open Source efforts see the many ways to [get involved](https://kusanagi.io#kusanagi/open-source).

Please also be sure to review our [community guidelines](https://kusanagi.io#kusanagi/open-source/conduct).

License
-------

Copyright 2016-2018 KUSANAGI S.L. (https://kusanagi.io). All rights reserved.

KUSANAGI, the sword logo and the "K" logo are trademarks and/or registered trademarks of KUSANAGI S.L. All other trademarks are property of their respective owners.

Licensed under the [MIT License](https://kusanagi.io#kusanagi/open-source/license). Redistributions of the source code included in this repository must retain the copyright notice found in each file.
