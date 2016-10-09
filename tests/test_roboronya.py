# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def bar():
    return 'bar'


def test_foo(bar):
    assert 'foobar' == 'foo' + bar
