#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

import pytest

from brainstorm.structure.architecture import (
    instantiate_layers_from_architecture)


def pytest_addoption(parser):
    parser.addoption("--skipslow", action="store_true",
                     help="skip slow tests")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and item.config.getoption("--skipslow"):
        pytest.skip("skipped because of --skipslow option")


#             /--- A -- C--
# InputLayer -        /    \
#             \--- B ------- D

@pytest.fixture
def layers():
    arch = {
        'InputLayer': {
            '@type': 'InputLayer',
            'out_shapes': {'default': ('T', 'B', 2)},
            '@outgoing_connections': {'A', 'B'}
        },
        'A': {
            '@type': 'FullyConnectedLayer',
            'shape': 3,
            '@outgoing_connections': {'C'}
        },
        'B': {
            '@type': 'FullyConnectedLayer',
            'shape': 5,
            '@outgoing_connections': {'C', 'D'}
        },
        'C': {
            '@type': 'FullyConnectedLayer',
            'shape': 7,
            '@outgoing_connections': {'D'}
        },
        'D': {
            '@type': 'FullyConnectedLayer',
            'shape': 11,
            '@outgoing_connections': set()
        }
    }
    return instantiate_layers_from_architecture(arch)
