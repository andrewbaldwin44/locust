.. _analytics:

====================
Anonymous Analytics
====================

Locust gathers anonymous analytics using open-source Posthog. You will be notified the first time you run locust. Analytics are not enabled until after this notice is shown, to ensure that you can opt out without ever sending analytics data.

Why?
----

Anonymous analytics allow us to prioritise fixes and features based on how people use Locust. For example:

    If a command is widely used and is failing often, it will enable us to prioritise fixing that feature over others.
    Collecting OS information, Python, and Locust versions allows us to decide which systems to prioritise for support and identify failures that occur only on certain versions.
    Knowing which features are not used and can be deprecated

What?
-----

Locust's analytics record some information for every execution of a locustfile:

    Non-identifying or boolean locust arguments e.g. num_users, headless, otel.
    The OS you are using e.g. 'linux', 'mac', or 'windows'.
    The version of Python you are using e.g. 3.12.4.
    The version of Locust, e.g. 2.42.7.

It is impossible for the Locust maintainers to match any particular event to any particular user. We do not store or receive IP addresses. We use a completely anonymous uuid to de-duplicate events.

How?
----

The code is viewable here `here <https://github.com/locustio/locust/locust/analytics.py>`_. The events are sent in a separate thread and will not delay any execution.

Opting out
----------

Locust analytics helps us maintainers and leaving it on is appreciated. However, if you want to opt out of Locust's analytics, you have sevaral options available:

.. code-block:: console

    $ locust --disable-analytics

Alternatively, an environment variable may be set:

.. code-block:: console
    $ export LOCUST_DISABLE_ANALYTICS=1
