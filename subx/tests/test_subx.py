# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess
import unittest

import mock
import six
import subx


class Test(unittest.TestCase):
    def test_call(self):
        subprocess_result = subx.call(['echo', 'foo'])
        self.assertEqual(b'foo\n', subprocess_result.stdout)
        self.assertEqual(b'', subprocess_result.stderr)
        self.assertEqual(0, subprocess_result.ret)

    def test_subprocess_result_call__command_which_does_not_exist(self):
        self.assertRaises(OSError, subx.SubprocessResult.call, ['command-which-does-not-exist'])

    def test_subprocess_result_call__read_stdout(self):
        result = subx.SubprocessResult.call(['cat', '/etc/fstab'])
        self.assertEqual(open('/etc/fstab', 'rb').read(), result.stdout)
        self.assertEqual(0, result.ret)
        self.assertEqual(b'', result.stderr)
        self.assertEqual(['cat', '/etc/fstab'], result.cmd)

    def test_subprocess_result_call__read_sterr(self):
        result = subx.SubprocessResult.call(['cat', '/file/which/does/not/exist'], env=dict(LANG='C'))
        self.assertEqual(b'', result.stdout)
        self.assertEqual(1, result.ret)
        self.assertEqual(b'cat: /file/which/does/not/exist: No such file or directory\n', result.stderr)

    def test_subprocess_result_call__read_sterr_and_stdout(self):
        result = subx.SubprocessResult.call(['cat', '/etc/fstab', '/file/which/does/not/exist'],
                                            env=dict(LANG='C'))
        self.assertEqual(open('/etc/fstab', 'rb').read(), result.stdout)
        self.assertEqual(1, result.ret)
        self.assertEqual(b'cat: /file/which/does/not/exist: No such file or directory\n', result.stderr)

    def test_assert_zero_exit_status__ok(self):
        result = subx.call(['cat', '/etc/fstab'], assert_zero_exit_status=True)
        self.assertEqual(open('/etc/fstab', 'rb').read(), result.stdout)
        self.assertEqual(0, result.ret)
        self.assertEqual(b'', result.stderr)
        self.assertEqual(['cat', '/etc/fstab'], result.cmd)

    def test_assert_zero_exit_status__non_zero(self):
        try:
            subx.call(
                ['cat', '/file/which/does/not/exist'], assert_zero_exit_status=True, env=dict(LANG='C'))
        except subx.SubprocessError as exc:
            self.assertEqual(['cat', '/file/which/does/not/exist'], exc.cmd)
            self.assertEqual(1, exc.returncode)
            self.assertEqual(
                "Command '['cat', '/file/which/does/not/exist']' returned non-zero exit status 1: stdout=b'' stderr=b'cat: /file/which/does/not/exist: No such file or directory'",
                str(exc).replace("u'", "'").replace('status 1.:', 'status 1:'))
        else:
            raise AssertionError()

    def test_warn_on_non_zero_exist_status__ok(self):
        result = subx.call(['cat', '/etc/fstab'], warn_on_non_zero_exist_status=True)
        self.assertEqual(open('/etc/fstab', 'rb').read(), result.stdout)
        self.assertEqual(0, result.ret)
        self.assertEqual(b'', result.stderr)
        self.assertEqual(['cat', '/etc/fstab'], result.cmd)

    def test_warn_on_non_zero_exist_status__non_zero(self):
        logs = []
        with mock.patch('subx.logger.warn', lambda msg: logs.append(msg)):
            result = subx.call(
                ['cat', '/file/which/does/not/exist'], assert_zero_exit_status=False, warn_on_non_zero_exist_status=True,
                env=dict(LANG='C'))
        self.assertEqual([
                "subprocess failed <SubprocessResult cmd='cat /file/which/does/not/exist' ret=1 stdout=b'' stderr=b'cat: /file/which/does/not/exist: No such file or directory'>"],
            logs)
        self.assertEqual(1, result.ret)

    def test_subprocess_result__repr(self):
        result = subx.SubprocessResult(cmd=['dummy'], ret=1, stdout=b'my-stdout', stderr=b'my-stderr')
        self.assertEqual("<SubprocessResult cmd='dummy' ret=1 stdout=b'my-stdout' stderr=b'my-stderr'>", repr(result))

    def test_call_with_input(self):
        result = subx.call(['cat'], input=b'foo', timeout=1)
        self.assertEqual("<SubprocessResult cmd='cat' ret=0 stdout=b'foo' stderr=b''>", repr(result))


    def test_repr_of_subprocess_result_is_7bit_ascii__bytestring(self):
        stdout = 'ö'.encode('utf8')
        stderr = 'ü'.encode('utf8')
        self.assertEqual("<SubprocessResult cmd='\\xe4' ret=1 stdout='\\xc3\\xb6' stderr='\\xc3\\xbc'>",
                         repr(subx.SubprocessResult(['ä'], 1, stdout=stdout, stderr=stderr)).replace("b'", "'"))

    def test_sudo_password_prompt_does_not_wait_for_ever(self):
        result = subx.call(['cat', '/dev/tty'], assert_zero_exit_status=False, timeout=10,
                           env=dict(LANG='C'))
        self.assertEqual(1, result.ret)
        self.assertIn(b'No such device or address', result.stderr)

    def test_redirect_stderr_to_stdout(self):
        result = subx.call(['cat', '/does/not/exist', '/etc/fstab'],
                           stderr=subprocess.STDOUT, assert_zero_exit_status=False, env=dict(LANG='C'))
        self.assertFalse(result.stderr)
        self.assertIn(b'cat: /does/not/exist: No such file or directory', result.stdout)

    def test_subx_called_with_incorrect__list_was_ommitted(self):
        self.assertRaises(ValueError, subx.call, 'python', 'setup.py')

    def test_subx_with_shell_is_true(self):
        result = subx.call(['cat'], input=b'foo', shell=True)
        self.assertEqual("<SubprocessResult cmd='cat' ret=0 stdout=b'foo' stderr=b''>", repr(result))

    def test_subx_failure_without_stderr(self):
        self.assertRaises(subx.SubprocessError, subx.call, ['false'], stderr=subprocess.STDOUT)
