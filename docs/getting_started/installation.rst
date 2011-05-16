Installation
=============

This document assumes that you are familiar with python, django, pip and 
virtualenv.

Requirements
------------

See :download:`requirements.txt <../../requirements.txt>` which is a pip 
compatible requirements list.

One line installation
-----------------------

The make command will do the same thing as manual installation example.

::

    make install
    ./manage.py runserver

Manual installation
--------------------

This is the long way to install snippify. It is installed as a lot of other 
django apps. This is an example based on virtualenv.

::

    virtualenv . --no-site-packages 
    source bin/activate 
    pip install -r requirements.txt
    cp local_settings.py.example local_settings.py # Configure this file for your needs
    ./manage.py syncdb
    ./manage runserver

At this point you should be able to see a working snippify instance at 
http://localhost:8000/
