#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import math
from myhdl import *
from ula.ula_modules import adder


@block
def dff(q, d, clk, rst):
    @always_seq(clk.posedge, reset=rst)
    def seq():
        q.next = d

    return instances()


@block
def blinkLedAdder(led, clk, rst):
    x = [Signal(bool(0)) for i in range(32)]
    y = [Signal(bool(0)) for i in range(32)]
    s = [Signal(bool(0)) for i in range(32)]
    c = Signal(bool(0))
    status = Signal(bool(0))

    y[0] = 1
    adder_1 = adder(x, y, s, c)

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if x[24] == 0 and x[23] == 0:
            for i in range(len(x)):
                x[i].next = s[i]
            status.next = status
        else:
            for i in range(len(x)):
                x[i].next = 0
            status.next = not status

    @always_comb
    def comb():
        led.next = status

    return instances()


@block
def blinkLed(led, time_ms, clk, rst):
    ms = 50000
    cnt = Signal(intbv(0)[32:])
    l = Signal(bool(0))

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if cnt < 25000000:
            cnt.next = cnt + 1
        else:
            cnt.next = 0
            l.next = not l

    @always_comb
    def comb():
        led.next = l

    return instances()


@block
def barLed(leds, time_ms, dir, vel, clk, rst):
    ms = 50000
    cnt = Signal(intbv(0)[32:])
    cntLed = Signal(intbv(0)[4:])
    led = Signal(intbv(0)[10:])
    delay = Signal(intbv(0)[32:])

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if cnt < delay:
            # if cnt < time_ms * ms:
            cnt.next = cnt + 1
        else:
            cnt.next = 0
            if cntLed < 10:
                if dir:
                    cntLed.next = cntLed + 1
                else:
                    cntLed.next = cntLed - 1
                led[cntLed].next = 1
            else:
                led.next = 0
                if dir:
                    cntLed.next = 0
                else:
                    cntLed.next = 2**10 - 1

    @always_comb
    def comb():
        leds.next = led

        if vel:
            delay.next = 10000000
        else:
            delay.next = 5000000

    return instances()


@block
def barLed2(leds, time_ms, clk, rst):
    ms = 50000
    cnt = Signal(intbv(0)[32:])
    cntLed = Signal(intbv(0)[4:])
    led = Signal(intbv(0)[10:])

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if cnt < time_ms * ms:
            cnt.next = cnt + 1
        else:
            cnt.next = 0
            if cntLed < 10:
                cntLed.next = cntLed + 1
            else:
                cntLed.next = 0

    @always_comb
    def comb():
        leds.next = intbv(1)[10:] << cntLed

    return instances()
