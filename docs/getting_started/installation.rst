Installation
=============

This document assumes that you are familiar with python, django, pip and 
virtualenv.

Requirements
------------

See :download:`requirements.txt <../../requirements.txt>` which is a pip 
compatible requirements list.

Installation (unix)
--------------------

This is the long way to install snippify. It is installed as a lot of other 
django apps. This is an example based on ``virtualenv``.

::

    virtualenv . --no-site-packages 
    source bin/activate 
    pip install -r requirements.txt
    cp local_settings.py.sample local_settings.py # Configure this file for your needs
    ./manage.py syncdb
    ./manage runserver

At this point you should be able to see a working snippify instance at 
http://localhost:8000/

.. note:: Remember to configure your ``MEDIA_URL`` correctly.
