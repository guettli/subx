# -*- coding: utf-8 -*-

import os
import subx
import unittest

class Test(unittest.TestCase):
    def test_readme_rst_valid(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        subx.call(cmd='python setup.py sdist', cwd=base_dir, shell=True)
        subx.call(cmd='twine check dist/*', cwd=base_dir, shell=True)
