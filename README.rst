snippify.me
===========

A web-app for storing code snippets.

Installation
------------

    virtualenv .
    pip install -r requirements.txt
    ./manage.py syncdb
    ./manage.py runserver

App structure
-------------

 * accounts - User profile views and models
 * api - REST api for the website
 * snippets - Snippet bussines
 * globaltags - used in different apps
 * tags - a simple tag app (maybe django-taggit is better *have a look*)
