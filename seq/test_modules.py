#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myhdl import *
from .seq_modules import *


def test_dff():
    rst = ResetSignal(0, active=1, isasync=True)
    clk = Signal(bool(0))
    q, d = [Signal(bool(0)) for i in range(2)]
    dut1 = dff(q, d, clk, rst)

    @always(delay(5))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        d.next = 1
        yield clk.negedge
        assert q == 1

        d.next = 0
        yield clk.negedge
        assert q == 0

    sim = Simulation(dut1, [stimulus, clkgen])
    traceSignals(dut1)
    sim.run(20)
    sim.quit()
