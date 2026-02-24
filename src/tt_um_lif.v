`default_nettype none

module tt_um_lif (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    assign uio_oe  = 8'hFF;
    assign uio_out = {7'b0, spike};

    wire spike;

    lif neuron (
        .current (ui_in),
        .clk     (clk),
        .reset_n (rst_n),
        .state   (uo_out),
        .spike   (spike)
    );

    wire _unused = &{ena, uio_in, 1'b0};

endmodule