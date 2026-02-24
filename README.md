Course: ECE 110/210
Assignment: Chip Design Project
Author: Austin Tchang
Title: Integrate and Fire Network

# Overview:
This project is for the Chip Design Project for the ECE 110/210 course. This project implements a Integrate-and-Fire Neuron using Tiny Tapeout.
This neuron accumulates charge in the form of current over time and fires a spike when a threshold is crossed within the state variable.
This project was written using Verilog and using python to test the digital circuit.

# Background:
This neuron models biological neurons when receiving input signals (current) and integrates them until firing an output known as the spike when a certain threshold is reached.
After firing, the state resets. The model can be captured in a single equation, state = state + current, recursively being integrated every clock cycle at a defined current.
Until state has exceeded or is equal to the threshold, the state resets. Thus the integrating (accumulating current) and firing (spike + reset) behavior.

# Core Logic:
The core logic of the model can be found in the neuron.v file. This will be an explanation of design and process.

  > Full Logic:
  >   localparam THRESHOLD = 8'd200; // the threshold for spiking

  >   assign spike = (state >= THRESHOLD); // we spike if the state is above the threshold
  > 
  >   always @(posedge clk) begin
  >       if (!reset_n) begin // if reset is active (active low)
  >           state <= 8'd0;
  >       end else if (spike) begin // if we spiked, reset the state
  >           state <= 8'd0;
  >       end else begin
  >           state <= state + current; // otherwise, integrate the current
  >       end
  >   end

## Threshold Value: 
> localparam THRESHOLD = 8'd200; // the threshold for spiking
This line of code defined the threshold where the state will need to be reached for a spike to happen. Here it is 200.

## Resetting: 
> if (!reset_n) begin // if reset is active (active low)
  > state <= 8'd0;
This condition looks at the reset_n value. If this condition is true, it will reset the state to 0.

## Spiking: 
> end else if (spike) begin // if we spiked, reset the state
  > state <= 8'd0;
This condition looks at the spike value. If this condition is, it will reset the state to 0. The main logic to a Fire section of the Integrate and Fire Neuron, when the threshold is reached.

## Integrating: 
> end else begin
  > state <= state + current; // otherwise, integrate the current
This statement is a if the other conditions are not true. This statement is where the integrating section of the Integrate and Fire Neuron is implemented. Current is added to the state.

# How to test/use:
Tests may be done using the test.py file found in the src. Otherwise, the general process for using it would be to apply rsn_n = 0 and rst_n then drive ui_in with a current for each clock cycle. 
Read uo_out to observe accumulation and when uo_out reaches the threshold, resets the uo_out and ui_out[7] goes high for one cycle.

## Example Image of Tests Passing
This image showcases the testbench for only certain tests passing.
![Tests Passing for test.py](<images/Test Passing.png>)

# Waveform/Timing Diagram
Here is a Waveform/Timing Diagram showcasing current accumulation on clock cycles, when the spike fires, and the state value reseting.
![Timing Diagram for Integrate and Fire Neuron](<images/Timing Diagram.png>)

# Github Workflows
This image shows the workflows for this project passing.
![Github Workflows](<images/Github Workflow.png>)