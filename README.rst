.. image:: https://travis-ci.org/leinz/imagesort.svg?branch=master
    :target: https://travis-ci.org/leinz/imagesort

imagesort
=========

Organize images according to exif date metadata.

Installation
============

Install with one of the following commands::

    $ easy_install imagesort

or alternatively if you have pip installed::

    $ pip install imagesort

Usage
=====

Type ``imagesort -h`` for usage help.

Examples
--------

Processing a directory::

    $ imagesort <sourcedir> <destdir>

Use the ``dry-run`` flag to see which actions will be performed without actually doing anything::

    $ imagesort --dry-run <sourcedir> <destdir>

Development
===========

Testing
-------

Running the tests during development requires pytest. Install
dependencies with

::

    $ pip install -r requirements.txt

and then run tests with

::

    $ py.test

Alternatively, if you have tox installed, just run tests by running::

    $ tox
