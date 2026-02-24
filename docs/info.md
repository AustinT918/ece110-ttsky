<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This Integrate and Fire Neuron takes in input currents and integrates them into the state until it reaches the Threshold (200).
When the Neuron reaches the Threshold, a spike will occur and the state will reset. This is an improvement/implementation from the initial assignment of the Leaky Integrate and Fire Neuron which resets the state when it reaches its threshold.

## How to test

Testing is done through the test.py file. The file goes through a total of 6 tests. 
Test 1 sees if the current is being integrated properly into the state.
Test 2 checks if spike has NOT occured yet since the state should be lower than the threshold.
Test 3 integrates more current over a calculated amount of cycles for when the neuron is expected to fire. This test checks if the neuron has fired and resets the state to 0, ready for the next current integration for the next spike.
Test 4 spikes multiple times, expecting 3 spikes.
Test 5 sets current to 0 and it expects that the state should not be changing.
Test 6 resets the circuit and thus will clear the state the middle of its run.

## External hardware

N/A
