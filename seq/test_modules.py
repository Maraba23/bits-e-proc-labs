#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myhdl import *
from seq_modules import *


@block
def test_dd():
    rst = ResetSignal(0, active=1, isasync=True)
    clk = Signal(bool(0))
    din = Signal(intbv(14)[8:])
    d_1 = doubleDabble(din, clk, rst)

    @always(delay(1))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        yield delay(1)

    return instances()


tb = test_dd()
# sim = Simulation(tb)
tb.run_sim(200)
