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