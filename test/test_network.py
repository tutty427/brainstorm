#!/usr/bin/env python
# coding=utf-8

from __future__ import division, print_function, unicode_literals
from brainstorm import Network, Gaussian
from brainstorm.layers import Input, Rnn, Lstm
import numpy as np
import pytest

np.random.seed(1234)

NO_CON = set()


def simple_recurrent_net():
    inp = Input(out_shapes={'default': ('T', 'B', 2)})
    net = Network.from_layer(inp >> Rnn(3, name='out'))
    return net


def lstm_net():
    inp = Input(out_shapes={'default': ('T', 'B', 2)})
    net = Network.from_layer(inp >> Lstm(3, name='out'))
    return net


layers_to_test_with_context = [
    simple_recurrent_net,
    lstm_net
]

ids = [f.__name__ for f in layers_to_test_with_context]

@pytest.fixture(params=layers_to_test_with_context, ids=ids)
def net_with_context(request):
    net = request.param()
    return net


def test_context_slice_allows_continuing_forward_pass(net_with_context):
    net = net_with_context
    net.initialize(Gaussian(0.1), seed=1234)
    all_data = np.random.randn(4, 1, 2)

    # First do a pass on all the data
    net.provide_external_data({'default': all_data})
    net.forward_pass()
    final_context = [x.copy() if x is not None else None for x in
                     net.get_context()]
    final_outputs = net.buffer.out.outputs.default

    # Pass only part of data
    data_a = all_data[:2, :, :].copy()
    net.provide_external_data({'default': data_a})
    net.forward_pass()

    # Pass rest of data with context
    data_b = all_data[2:, :, :].copy()
    net.provide_external_data({'default': data_b})
    net.forward_pass(context=net.get_context())
    context = [x.copy() if x is not None else None for x in net.get_context()]
    outputs = net.buffer.out.outputs.default

    # Check if outputs are the same as final_outputs
    print("Outputs:\n", outputs)
    print("Should match:\n", final_outputs[2:])
    assert np.allclose(outputs, final_outputs[2:])

    # Check if context is same as final_context
    assert len(context) == len(final_context), "Context list sizes mismatch!"

    for (x, y) in zip(context, final_context):
        if x is None:
            assert y is None
        else:
            print("Context:\n", x)
            print("Should match:\n", y)
            assert np.allclose(x, y)
