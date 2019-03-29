# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import logging
import os

try:
    import subprocess32 as subprocess

    TimeoutExpired = subprocess.TimeoutExpired
    is_subprocess32 = True
except ImportError:
    import subprocess

    TimeoutExpired = IOError
    is_subprocess32 = False

try:
    from subprocess32 import CalledProcessError
except ImportError:
    from subprocess import CalledProcessError

try:
  basestring
except NameError:
  basestring = str


logger = logging.getLogger(__name__)


def repr_like_python3(something):
    result = repr(something)
    if result.startswith("u'") or result.startswith('u"'):
        return result[1:]
    return result


def call(cmd, input=None, assert_zero_exit_status=True, warn_on_non_zero_exist_status=False, **kwargs):
    """
    :rtype: SubprocessResult

    Raises OSError if command was not found

    Returns non-zero result in result.ret if subprocess terminated with non-zero exist status.
    """
    if (not kwargs.get('shell')) and isinstance(cmd, basestring):
        raise ValueError('cmd should be list or tuple, not a string: %r' % cmd)
    result = SubprocessResult.call(cmd, input=input, **kwargs)
    if assert_zero_exit_status and result.ret != 0:
        raise SubprocessError(result)

    if warn_on_non_zero_exist_status and result.ret != 0:
        logger.warn('subprocess failed %r' % result)

    return result


class SubprocessResult(object):
    def __init__(self, cmd, ret, stdout='', stderr=''):
        self.cmd = cmd
        self.ret = ret
        self.stdout = stdout
        self.stderr = stderr

    max_head_size = 4000

    def __repr__(self):
        return b'<{} cmd={} ret={} stdout={} stderr={}>'.format(self.__class__.__name__,
                                                                repr_like_python3(self.cmd_for_copy_and_paste),
                                                                self.ret,
                                                                repr_like_python3(self.head_of_string(self.stdout)),
                                                                repr_like_python3(self.head_of_string(self.stderr)))

    @property
    def cmd_for_copy_and_paste(self):
        ret = []
        for item in self.cmd:
            if b' ' in item:
                item = '"{}"'.format(item)
            ret.append(item)
        return b' '.join(ret)

    @classmethod
    def head_of_string(cls, stdout, max_head_size=None):
        if not max_head_size:
            max_head_size = cls.max_head_size
        stdout = stdout.strip()
        if len(stdout) < max_head_size:
            return stdout
        return '%s ... [cut]' % stdout[:max_head_size]

    @classmethod
    def call(cls, cmd, input=None, **kwargs):
        if is_subprocess32:
            kwargs['start_new_session'] = kwargs.get('start_new_session',
                                                     True)  # change default. We want sudo to fail, not to read a password from /dev/tty
        kwargs.setdefault(b'bufsize', -1)
        timeout = kwargs.pop(b'timeout', None)
        if input:
            stdin = subprocess.PIPE
        else:
            stdin = open(os.devnull, 'rb')
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=stdin, **kwargs)
        stdout, stderr = handle_subprocess_pipe_with_timeout(pipe, timeout=timeout, input=input)
        return cls(cmd, pipe.wait(), stdout, stderr)


class SubprocessError(CalledProcessError):
    def __init__(self, subprocess_result):
        super(SubprocessError, self).__init__(subprocess_result.ret, subprocess_result.cmd,
                                              SubprocessResult.head_of_string(subprocess_result.stdout))
        self.stderr = subprocess_result.stderr

    def __str__(self):
        return b'%s: stdout=%r stderr=%r' % (super(SubprocessError, self).__str__(), self.output, self.stderr)


def handle_subprocess_pipe_with_timeout(pipe, timeout, input=None):
    if (not input is None) and not pipe.stdin:
        raise Exception('pipe.stdin must be a stream if you pass in input')
    stdout = ''
    stderr = ''
    kwargs = dict(input=input)
    if timeout:
        kwargs['timeout'] = timeout
    try:
        stdout, stderr = pipe.communicate(**kwargs)
    except TimeoutExpired:
        pipe.kill()
        try:
            # Other solution to handle timeout for shell=True: http://stackoverflow.com/a/4791612/633961
            # related: http://stackoverflow.com/questions/36592068/subprocess-with-timeout-what-to-do-after-timeoutexpired-exception
            stdout, stderr = pipe.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            pass
        raise subprocess.TimeoutExpired(pipe.args, timeout, 'stdout: %r stderr: %r' % (stdout, stderr))
    return (stdout, stderr)
