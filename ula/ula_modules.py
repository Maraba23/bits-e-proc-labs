#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    s = Signal(bool())
    c = Signal(bool())

    @always_comb
    def comb():
        s = a ^ b
        c = a & b

        soma.next = s
        carry.next = c

        # print("a: %s b: %s | s: %s c: %s" % (bin(a), bin(b), bin(s), bin(c)))

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]

    haList[0] = halfAdder(a, b, s[0], s[1])  # 2
    haList[1] = halfAdder(c, s[0], soma, s[2])  # 3

    @always_comb
    def comb():
        carry.next = s[1] | s[2]  # 4

    return instances()


@block
def adder2bits(x, y, soma, carry):
    c_ = [Signal(bool()) for i in range(2)]
    f0 = fullAdder(x[0], y[0], 0, soma[0], c_[0])
    f1 = fullAdder(x[1], y[1], c_[0], soma[1], carry)

    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    c = [Signal(bool(0)) for i in range(n + 1)]
    fa_list = [None for i in range(n)]

    for i in range(n):
        fa_list[i] = fullAdder(x[i], y[i], c[i], soma[i], c[i + 1])

    @always_comb
    def comb():
        carry.next = c[n]

    return instances()


@block
def adderModbv(x, y, soma, carry):
    @always_comb
    def comb():
        sum = x + y
        soma.next = sum
        if sum > x.max - 1:
            carry.next = 1
        else:
            carry.next = 0

    return comb


@block
def addBcd(x1, x0, y1, y0):
    n0 = ConcatSignal(x1, x0)
    n1 = ConcatSignal(y1, y0)

    @always_comb
    def comb():
        s = n0 + n1
        breakpoint()
        if s[8:] > 9:
            s = s + 6
        print(bin(s, 16))

    return comb
