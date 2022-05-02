"""A basic check to make sure that we are using a mypyc-compiled version when expected."""

import extyper

from unittest import TestCase
import os


class MypycTest(TestCase):
    def test_using_mypyc(self) -> None:
        if os.getenv('TEST_MYPYC', None) == '1':
            assert not extyper.__file__.endswith('.py'), "Expected to find a mypyc-compiled version"
