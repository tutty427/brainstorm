#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals


class BufferView(list):
    def __init__(self, buffer_names, buffers, full_buffer=None):
        super(BufferView, self).__init__(buffers)
        if not len(buffers) == len(buffer_names):
            raise ValueError("Length mismatch between buffers and names ({} !="
                             " {})".format(len(buffers), len(buffer_names)))
        self._full_buffer = full_buffer
        self._buffer_names = tuple(buffer_names)
        for i, n in enumerate(buffer_names):
            self.__dict__[n] = self[i]

    def adjust(self, buffer_names, buffers, full_buffer=None):
        assert self._buffer_names == buffer_names
        self._full_buffer = full_buffer
        for i, (n, b) in enumerate(zip(buffer_names, buffers)):
            self[i] = b
            self.__dict__[n] = self[i]
        return self

    def _asdict(self):
        return dict(zip(self._buffer_names, self))

    def items(self):
        return self._asdict().items()

    def keys(self):
        return self._asdict().keys()

    def values(self):
        return self._asdict().values()

    def __getitem__(self, item):
        if isinstance(item, int):
            return super(BufferView, self).__getitem__(item)
        return self.__dict__[item]

    def __contains__(self, item):
        return item in self._buffer_names
