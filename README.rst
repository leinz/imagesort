.. image:: https://travis-ci.org/leinz/imagesort.svg?branch=master
    :target: https://travis-ci.org/leinz/imagesort

Organize image files by date taken
==================================

All images under the given source directory are copied to the destination
directory under subdirectories with names corresponding to when they are taken.
Files with no or invalid exif metadata are put in the ``unknown`` directory.

The destination directory have the following structure after processing::

    2013/
        2013_12_20/
            1.jpg
    2014/
        2014_03_06/
            2.jpg
            3.jpg
        2014_07_01/
            4.jpg
    unknown/
        5.jpg

The original filenames are preserved. If a destination filepath already exist,
there are two possible outcomes:

- If the old filepath's content is identical to the new one, the program does
  nothing and continues to the next image.
- If the contents of the old and new files are different, it will append an
  integer until the content of an existing file matches or the path does not
  already exist. This means that if there are three source files named
  ``1.jpg`` with identical date metadata but different contents, the final
  names will be ``1.jpg``, ``1-1.jpg`` and ``1-2.jpg``.

Installation
============

Install with one of the following commands::

    $ easy_install imagesort

or alternatively if you have pip installed::

    $ pip install imagesort

Usage
=====

Type ``imagesort -h`` for a list of available options.

Examples
--------

Copying images from ``inputdir`` to ``outputdir``::

    $ imagesort inputdir outputdir

Use the ``dry-run`` flag to see which actions will be performed without
actually doing anything::

    $ imagesort --dry-run inputdir outputdir

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
