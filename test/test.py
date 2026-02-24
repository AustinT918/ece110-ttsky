# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # -------------------------------------------------------------------------
    # Reset
    # -------------------------------------------------------------------------
    dut.ena.value    = 1
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    dut.rst_n.value  = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value  = 1

    # Sample on falling edge — outputs are stable here (not mid-transition)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected state=0 after reset, got {int(dut.uo_out.value)}"
    dut._log.info("PASS: state is 0 after reset")

    # -------------------------------------------------------------------------
    # Test 1: state integrates properly — grows by current each cycle
    # -------------------------------------------------------------------------
    dut._log.info("Test 1: integration")
    dut.ui_in.value = 10

    for cycle in range(1, 6):
        await RisingEdge(dut.clk)  # clock ticks, state updates
        await FallingEdge(dut.clk) # sample once outputs are settled
        expected = 10 * cycle
        actual = int(dut.uo_out.value)
        assert actual == expected, \
            f"Cycle {cycle}: expected state={expected}, got {actual}"
        dut._log.info(f"  cycle {cycle}: state={actual} ✓")

    # -------------------------------------------------------------------------
    # Test 2: no spike yet (state=50, well below threshold=200)
    # -------------------------------------------------------------------------
    assert int(dut.uio_out.value) & 0x01 == 0, "Spike should not be high yet"
    dut._log.info("PASS: no spike below threshold")

    # -------------------------------------------------------------------------
    # Test 3: neuron fires when state reaches 200, then resets to 0
    # current=10, so fires every 200/10 = 20 cycles from a clean reset
    # already at state=50, so 15 more cycles to threshold
    # -------------------------------------------------------------------------
    dut._log.info("Test 3: waiting for spike")
    spike_seen = False

    for cycle in range(30):
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)
        state = int(dut.uo_out.value)
        spike = int(dut.uio_out.value) & 0x01
        dut._log.info(f"  state={state}, spike={spike}")

        if spike and not spike_seen:
            spike_seen = True
            dut._log.info("PASS: spike fired")
            # one cycle later state should have reset to 0
            await RisingEdge(dut.clk)
            await FallingEdge(dut.clk)
            assert int(dut.uo_out.value) == 0, \
                f"Expected reset to 0 after spike, got {int(dut.uo_out.value)}"
            dut._log.info("PASS: state reset to 0 after spike")
            break

    assert spike_seen, "Neuron never spiked — check threshold / current"

    # -------------------------------------------------------------------------
    # Test 4: regular spiking — inter-spike intervals should all be equal
    # current=20, threshold=200 → fires every 10 cycles
    # -------------------------------------------------------------------------
    dut._log.info("Test 4: regular spiking with current=20")
    dut.ui_in.value = 20
    spike_times = []

    for cycle in range(100):
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)
        if int(dut.uio_out.value) & 0x01:
            spike_times.append(cycle)
            if len(spike_times) == 3:
                break

    assert len(spike_times) == 3, f"Expected 3 spikes, only got {len(spike_times)}"
    isi1 = spike_times[1] - spike_times[0]
    isi2 = spike_times[2] - spike_times[1]
    assert isi1 == isi2, f"Inter-spike intervals not equal: {isi1} vs {isi2}"
    dut._log.info(f"PASS: regular spiking, ISI={isi1} cycles")

    # -------------------------------------------------------------------------
    # Test 5: zero current — state should not change
    # -------------------------------------------------------------------------
    dut._log.info("Test 5: zero current holds state")
    dut.ui_in.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    state_before = int(dut.uo_out.value)

    await ClockCycles(dut.clk, 10)
    await FallingEdge(dut.clk)
    state_after = int(dut.uo_out.value)

    assert state_before == state_after, \
        f"State changed with zero current: {state_before} -> {state_after}"
    dut._log.info(f"PASS: state held at {state_after} with zero current")

    # -------------------------------------------------------------------------
    # Test 6: reset mid-run clears state
    # -------------------------------------------------------------------------
    dut._log.info("Test 6: reset clears state mid-run")
    dut.ui_in.value = 30
    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    assert int(dut.uo_out.value) == 0, \
        f"Expected state=0 after mid-run reset, got {int(dut.uo_out.value)}"
    dut._log.info("PASS: mid-run reset cleared state")

    dut._log.info("All tests passed!")