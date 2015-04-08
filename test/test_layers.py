#!/usr/bin/env python
# coding=utf-8

from __future__ import division, print_function, unicode_literals
from brainstorm.layers.fully_connected_layer import FullyConnectedLayerImpl
from brainstorm.layers.squared_difference_layer import \
    SquaredDifferenceLayerImpl
from brainstorm.layers.binomial_cross_entropy_layer import \
    BinomialCrossEntropyLayerImpl
from brainstorm.handlers import NumpyHandler
from .helpers import run_layer_test
import numpy as np
np.random.seed(1234)


def test_fully_connected_layer():

    eps = 1e-6
    time_steps = 3
    batch_size = 2
    input_shape = 3
    layer_shape = 2

    in_shapes = {'default': ('T', 'B', input_shape,)}
    layer = FullyConnectedLayerImpl('TestLayer', in_shapes, [], [],
                                    shape=layer_shape,
                                    activation_function='sigmoid')
    layer.set_handler(NumpyHandler(np.float64))
    print("\n---------- Testing FullyConnectedLayer ----------")
    run_layer_test(layer, time_steps, batch_size, eps)


def test_squared_difference_layer():

    eps = 1e-4
    time_steps = 3
    batch_size = 2
    in_shapes = {'inputs_1': ('T', 'B', 3, 2),
                 'inputs_2': ('T', 'B', 3, 2)
                 }

    layer = SquaredDifferenceLayerImpl('TestLayer', in_shapes, [], [])
    layer.set_handler(NumpyHandler(np.float64))

    print("\n---------- Testing SquaredDifferenceLayer ----------")
    run_layer_test(layer, time_steps, batch_size, eps)


def test_binomial_crossentropy_layer():

    eps = 1e-5
    time_steps = 3
    batch_size = 2
    feature_shape = (5,)
    shape = (time_steps, batch_size) + feature_shape
    default = np.random.rand(*shape)
    targets = np.random.randint(0, 2, shape)
    print(default)
    print(targets)
    in_shapes = {'default': ('T', 'B') + feature_shape,
                 'targets': ('T', 'B') + feature_shape
                 }

    layer = BinomialCrossEntropyLayerImpl('TestLayer', in_shapes, [], [])
    layer.set_handler(NumpyHandler(np.float64))

    print("\n---------- Testing BinomialCrossEntropyError ----------")
    run_layer_test(layer, time_steps, batch_size, eps,
                   skip_inputs=['targets'], default=default, targets=targets)
