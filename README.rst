.. image:: https://travis-ci.org/guettli/subx.svg?branch=master
    :target: https://travis-ci.org/guettli/subx
    
subx: Data structure SubprocessResult - for the Python programming language
==================================================================


https://github.com/guettli/subx

SubprocessResult
================

This library gives you a data structure called `SubprocessResult`. It combines stdout, stderr and ret (the exit status).

This is handy if you do "one shut" calling of processes.


Examples
========

The method `call()` returns an instance of `SubprocessResult`.

result = subx.call(['date'])

Class SubprocessResult
======================

The class `SubprocessResult` has the following attributes:

 * stdout
 * stderr
 * ret
 * cmd

Additional Features
===================

If available the subprocess32 library gets used. This provides the timeout parameter for Python 2.7.


Not suited for ...
==================

This library is not usefull if you want to stream data to or from your subprocess.

Install
=======

Install for usage from `pypi <https://pypi.python.org/pypi/subx/>`_::

    pip install subx


Development Install on Python2
==============================

Install subx for development on Python2::

    virtualenv subx-env
    cd subx-env
    . ./bin/activate
    pip install -e git+https://github.com/guettli/subx.git#egg=subx

Development Install on Python3
==============================

Install subx for development on Python3::

    python3 -m venv subx-py3env
    cd subx-py3env
    . ./bin/activate
    pip install --upgrade pip
    pip install -e git+https://github.com/guettli/subx.git#egg=subx

Development Testing
===================

Testing::

    pip install -r src/subx/requirements.txt
    cd src/subx
    pytest # all test ok?
    pyCharm src/subx/...
    pytest # all test still ok?
    .... I am waiting for your pull request :-)
