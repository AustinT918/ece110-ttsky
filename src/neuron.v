`default_nettype none

module neuron (
    input  wire [7:0] current,
    input  wire       clk,
    input  wire       reset_n,
    output reg  [7:0] state,
    output wire       spike
);
    localparam THRESHOLD = 8'd200; // the threshold for spiking

    assign spike = (state >= THRESHOLD); // we spike if the state is above the threshold

    always @(posedge clk) begin
        if (!reset_n) begin // if reset is active (active low)
            state <= 8'd0;
        end else if (spike) begin // if we spiked, reset the state
            state <= 8'd0;
        end else begin
            state <= state + current; // otherwise, integrate the current
        end
    end

endmodule