#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import numpy as np
import brainstorm as bs
import pytest
from brainstorm.utils import NetworkValidationError


@pytest.fixture
def net():
    net = bs.Network.from_layer(
        bs.InputLayer(out_shapes={'default': ('T', 'B', 1)}) >>
        bs.FullyConnectedLayer(2) >>
        bs.FullyConnectedLayer(3) >>
        bs.FullyConnectedLayer(1, name='OutputLayer')
    )
    return net


def test_initialize_default(net):
    net.initialize(7)
    assert np.all(net.buffer.parameters == 7)


def test_initialze_layerwise_dict(net):
    net.initialize({
        'FullyConnectedLayer_1': 1,
        'FullyConnectedLayer_2': 2,
        'OutputLayer': 3})

    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 1)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W == 2)
    assert np.all(net.buffer.OutputLayer.parameters.W == 3)


def test_initialize_layerwise_kwargs(net):
    net.initialize(
        FullyConnectedLayer_1=1,
        FullyConnectedLayer_2=2,
        OutputLayer=3)

    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 1)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W == 2)
    assert np.all(net.buffer.OutputLayer.parameters.W == 3)


def test_initialize_layerwise_plus_default_kwargs(net):
    net.initialize(7,
                   FullyConnectedLayer_1=1,
                   OutputLayer=3)

    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 1)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W == 7)
    assert np.all(net.buffer.OutputLayer.parameters.W == 3)


def test_initialize_weightwise(net):
    net.initialize(7,
                   FullyConnectedLayer_1={'W': 1},
                   FullyConnectedLayer_2={'W': 2, 'default': 3},
                   OutputLayer={'bias': 4})
    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 1)
    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.bias == 7)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W == 2)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.bias == 3)
    assert np.all(net.buffer.OutputLayer.parameters.W == 7)
    assert np.all(net.buffer.OutputLayer.parameters.bias == 4)


def test_initialize_with_array(net):
    net.initialize(0,
                   FullyConnectedLayer_1={'bias': [1, 2]},
                   FullyConnectedLayer_2={'bias': np.array([3, 4, 5]),
                                          'W': [[6, 7],
                                                [8, 9],
                                                [10, 11]]},
                   OutputLayer={'bias': [12]})

    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 0)
    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.bias ==
                  [1, 2])
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.bias ==
                  [3, 4, 5])
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W ==
                  [[6, 7], [8, 9], [10, 11]])
    assert np.all(net.buffer.OutputLayer.parameters.W == 0)
    assert np.all(net.buffer.OutputLayer.parameters.bias == 12)


def test_initialize_with_initializer(net):
    net.initialize(
        default=bs.Uniform(0, 1),
        FullyConnectedLayer_1=bs.Uniform(1, 2),
        FullyConnectedLayer_2={'W': bs.Uniform(2, 3)},
        OutputLayer={'W': bs.Uniform(3, 4), 'bias': bs.Uniform(4, 5)}
    )

    layer1 = net.buffer.FullyConnectedLayer_1.parameters
    layer2 = net.buffer.FullyConnectedLayer_2.parameters
    layer3 = net.buffer.OutputLayer.parameters

    assert np.all(1 <= layer1.W) and np.all(layer1.W <= 2)
    assert np.all(1 <= layer1.bias) and np.all(layer1.bias <= 2)
    assert np.all(2 <= layer2.W) and np.all(layer2.W <= 3)
    assert np.all(0 <= layer2.bias) and np.all(layer2.bias <= 1)
    assert np.all(3 <= layer3.W) and np.all(layer3.W <= 4)
    assert np.all(4 <= layer3.bias) and np.all(layer3.bias <= 5)


def test_initialize_with_layer_pattern(net):
    net.initialize({'default': 0, 'Fully*': 1})

    assert np.all(net.buffer.FullyConnectedLayer_1.parameters.W == 1)
    assert np.all(net.buffer.FullyConnectedLayer_2.parameters.W == 1)
    assert np.all(net.buffer.OutputLayer.parameters.W == 0)


def test_initialize_with_nonmatching_pattern_raises(net):
    with pytest.raises(NetworkValidationError):
        net.initialize({'default': 0, 'LSTM*': 1})

    with pytest.raises(NetworkValidationError):
        net.initialize({'default': 0, 'OutputLayer': {'*_bias': 1}})


def test_initialize_raises_on_missing_initializers(net):
    with pytest.raises(NetworkValidationError):
        net.initialize({'FullyConnected*': 1})

    with pytest.raises(NetworkValidationError):
        net.initialize(
            FullyConnectedLayer_1=1,
            FullyConnectedLayer_2={'b': 2},
            OutputLayer=3)
