.. image:: https://travis-ci.org/guettli/subx.svg?branch=master
    :target: https://travis-ci.org/guettli/subx
    
subx: Data structure SubprocessResult - for the Python programming language
===========================================================================


https://github.com/guettli/subx

SubprocessResult
================

This library gives you a data structure called `SubprocessResult`. It combines stdout, stderr and ret (the exit status).

This is handy if you do "one shot" calling of processes.

Why?
====

If subx fails, you get a meaningful exception message that helps you. You see the first bytes of stdout and stderr. This is the main reason
why I wrote this library.

Gracefull handling of timeouts. You get a meaningful error message, even if a timeout happens: You see all stdin and stdout which was emitted
until the timeout occured.

Passing in a string as stdin of a subprocess is easy. Just use the kwarg `input`.


Examples
========

The method `call()` returns an instance of `SubprocessResult`.

result = subx.call(['date'])

Just replace `subprocess.check_call(cmd)` with `subx.call(cmd)` and you get all you want plus a helpful exception messages.

Or replace `subprocess.check_output(cmd)` with `subx.call(cmd).stdout`.

If you want to ignore the status code like shell scripts do, and you want to see the head of stdout/stderr you can use this:

`logging.info(subx.call(assert_zero_exit_status=False))`

This will use repr(result). Which looks like roughly this:

`<SubprocessResult cmd='my-command' ret=0 stdout='....' stderr='...'>`

Method subx.call()
==================

Arguments::

    call(cmd, input=None, assert_zero_exit_status=True, warn_on_non_zero_exist_status=False, **kwargs)

    input: String which gets send to stdin of the subprocess.
    assert_zero_exit_status: raise an exception if exist status is non-zero?
    warn_on_non_zero_exist_status: warn on non zero exit status?

    Returns: SubprocessResult instance

Class SubprocessResult
======================

The class `SubprocessResult` has the following attributes:

 * stdout
 * stderr
 * ret (exit status)
 * cmd

Additional Features
===================

If available the subprocess32 library gets used. This provides the timeout parameter for Python 2.7.


Not suited for ...
==================

This library is not usefull if you want to read streamed data **from** your subprocess. But the library is usefull, if
you want to stream data **to** your subprocess.

Install
=======

Install from `pypi <https://pypi.python.org/pypi/subx/>`_::

    pip install subx



subprocess.check_output() vs subx.call()
========================================

Look, compare, think and decide what message helps your more.

subprocess.check_output()::

    CalledProcessError: Command '['cat', 'some-file']' returned non-zero exit status 1

sub.call()::

    SubprocessError: Command '['cat', 'some-file']' returned non-zero exit status 1:
    stdout='' stderr='cat: some-file: No such file or directory'


... especially if the code fails in a production environment where reproducing the error is not easy,
subx can call help you to spot the source of the failure.

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
