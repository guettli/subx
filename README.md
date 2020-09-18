[![image](https://travis-ci.org/guettli/subx.svg?branch=master)](https://travis-ci.org/guettli/subx)

subx: Data structure SubprocessResult - for the Python programming language
===========================================================================

<https://github.com/guettli/subx>

SubprocessResult
================

This library gives you a data structure called
[SubprocessResult]{.title-ref}. It combines stdout, stderr and ret (the
exit status).

This is handy if you do \"one shot\" calling of processes.

Why?
====

If subx fails, you get a meaningful exception message that helps you.
You see the first bytes of stdout and stderr. This more convinient than
the standard library
\[subprocess\](<https://docs.python.org/3/library/subprocess.html>)

Gracefull handling of timeouts. You get a meaningful error message, even
if a timeout happens: You see all stdin and stdout which was emitted
until the timeout occured.

Passing in a string as stdin of a subprocess is easy. Just use the kwarg
[input]{.title-ref}.

Examples
========

The method [call()]{.title-ref} returns an instance of
[SubprocessResult]{.title-ref}.

result = subx.call(\[\'date\'\])

Just replace [subprocess.check\_call(cmd)]{.title-ref} with
[subx.call(cmd)]{.title-ref} and you get all you want plus a helpful
exception messages.

Or replace [subprocess.check\_output(cmd)]{.title-ref} with
[subx.call(cmd).stdout]{.title-ref}.

If you want to ignore the status code like shell scripts do, and you
want to see the head of stdout/stderr you can use this:

[logging.info(subx.call(assert\_zero\_exit\_status=False))]{.title-ref}

This will use repr(result). Which looks like roughly this:

[\<SubprocessResult cmd=\'my-command\' ret=0 stdout=\'\....\'
stderr=\'\...\'\>]{.title-ref}

By default subx.call() raises [subx.SubprocessError]{.title-ref} if the
exit status is non-zero.

If you want to handle non-zero exist status yourself, then you can do it
like this:

    result = subx.call(cmd, assert_zero_exit_status=False)
    if result.ret:
        print('Failed: {}\n{}\n{}'.format(cmd, result.stderr, result.stdout))
        ...

Method subx.call()
==================

Arguments:

    call(cmd, input=None, assert_zero_exit_status=True, warn_on_non_zero_exist_status=False, **kwargs)

    input: String which gets send to stdin of the subprocess.
    assert_zero_exit_status: raise an exception if exist status is non-zero?
    warn_on_non_zero_exist_status: warn on non zero exit status?

    Returns: SubprocessResult instance

Class SubprocessResult
======================

The class [SubprocessResult]{.title-ref} has the following attributes:

> -   stdout
> -   stderr
> -   ret (exit status)
> -   cmd

Not suited for \...
===================

This library is not usefull if you want to read streamed data **from**
your subprocess. But the library is usefull, if you want to stream data
**to** your subprocess.

Install
=======

Install from [pypi](https://pypi.python.org/pypi/subx/):

    pip install subx

subprocess.check\_output() vs subx.call()
=========================================

Look, compare, think and decide what message helps your more.

subprocess.check\_output():

    CalledProcessError: Command '['cat', 'some-file']' returned non-zero exit status 1

sub.call():

    SubprocessError: Command '['cat', 'some-file']' returned non-zero exit status 1:
    stdout='' stderr='cat: some-file: No such file or directory'

\... especially if the code fails in a production environment where
reproducing the error is not easy, subx can call help you to spot the
source of the failure.

Development Install on Python3
==============================

Install subx for development on Python3:

    python3 -m venv subx-py3env
    cd subx-py3env
    . ./bin/activate
    pip install --upgrade pip
    pip install -e git+https://github.com/guettli/subx.git#egg=subx

Development Testing
===================

Testing:

    pip install -r src/subx/requirements.txt
    cd src/subx
    pytest # all test ok?
    pyCharm src/subx/...
    pytest # all test still ok?
    .... I am waiting for your pull request :-)

Python 2
========

Python 2 is not supported any more. Please use version
[2019.36.0]{.title-ref} if you need it.