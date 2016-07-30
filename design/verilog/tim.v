
`timescale 1 ns / 100 ps

module tim (_CLK);

   input _CLK;

   /* ****************************************************************** */
   /* wires */
   /* ****************************************************************** */
   wire         _CLK;
   wire  [15:0] A_D;
   wire   [3:0] A_F;
   wire  [22:0] BUS_A;
    reg  [22:0] _BUS_A;
    reg         _BUS_A_en;
   wire  [15:0] BUS_D;
    reg  [15:0] _BUS_D;
    reg         _BUS_D_en;
   wire         BUS_R;
    reg         _BUS_R;
    reg         _BUS_R_en;
   wire         BUS_W;
    reg         _BUS_W;
    reg         _BUS_W_en;
   wire         CLK0;
   wire         CLK1;
   wire         CLK2;
   wire         CLK3;
   wire  [15:0] D_A;
   wire  [15:0] D_B;
   wire  [15:0] D_C;
   wire         D_Ca;
   wire         D_H;
   wire         D_J;
   wire         D_Mr;
   wire         D_Mt;
   wire         D_Mw;
   wire   [2:0] D_Op;
   wire   [3:0] D_RFa;
   wire   [3:0] D_RFb;
   wire   [3:0] D_Ra;
   wire   [3:0] D_Rb;
   wire   [3:0] D_Rc;
   wire   [3:0] D_Rd;
   wire         D_S;
   wire   [2:0] D_SF;
   wire         D_T;
   wire         DC_J;
   wire         DC_Mr;
   wire         DC_Mw;
   wire   [3:0] DC_Rd;
   wire         DC_S;
   wire         DC_T;
   wire  [15:0] DE_A;
   wire  [15:0] DE_B;
   wire  [15:0] DE_C;
   wire         DE_Ca;
   wire         DE_J;
   wire         DE_Mr;
   wire         DE_Mt;
   wire         DE_Mw;
   wire   [2:0] DE_Op;
   wire  [15:0] DE_PC;
   wire   [3:0] DE_Ra;
   wire   [3:0] DE_Rb;
   wire   [3:0] DE_Rc;
   wire   [3:0] DE_Rd;
   wire         DE_S;
   wire   [2:0] DE_SF;
   wire         DE_T;
   wire  [15:0] EC_D;
   wire         EC_I;
   wire         EC_J;
   wire         EC_Mr;
   wire         EC_Mt;
   wire         EC_Mw;
   wire   [3:0] EC_Rd;
   wire         EC_S;
   wire         EC_T;
   wire   [3:0] EM_AF;
   wire  [15:0] EM_C;
   wire  [15:0] EM_D;
   wire         EM_I;
   wire         EM_J;
   wire         EM_Mr;
   wire         EM_Mt;
   wire         EM_Mw;
   wire  [15:0] EM_PC;
   wire   [3:0] EM_Rd;
   wire         EM_S;
   wire   [2:0] EM_SF;
   wire         EM_T;
   wire  [15:0] _E_S;
   wire  [15:0] F_A;
   wire  [15:0] F_B;
   wire  [15:0] F_C;
   wire  [15:0] FC_I;
   wire  [15:0] F_I;
   wire  [15:0] F_PC;
   wire  [15:0] FD_I;
   wire  [15:0] FD_PC;
   wire         H_H;
   wire  [15:0] I_D;
   wire         I_I;
   wire   [3:0] I_Rd;
   wire         I_T;
   wire         MC_Ir;
   wire         MC_Mr;
   wire         MC_Mw;
   wire   [3:0] MC_Rd;
   wire  [15:0] MW_D;
   wire         MW_I;
   wire         MW_IE;
   wire  [15:0] MW_PC;
   wire   [3:0] MW_Rd;
   wire         MW_T;
   wire  [15:0] M_D;
   wire  [15:0] R_A;
   wire  [15:0] R_B;
   wire   [5:0] R_CS;
   wire   [5:0] R_DS;
   wire         R_IE;
   wire         R_M;
   wire         S_S;


   /* ****************************************************************** */
   /* modules */
   /* ****************************************************************** */
   clock CLOCK (
       .CLK0	(CLK0),
       .CLK1	(CLK1),
       .CLK2	(CLK2),
       .CLK3	(CLK3),
       ._CLK	(_CLK)
   );


   devices DEVICES (
       .BUS_A	(BUS_A),
       .BUS_D	(BUS_D),
       .BUS_R	(BUS_R),
       .BUS_W	(BUS_W)
   );


   decode_control DECODE_CONTROL (
       .DC_J	(DC_J),
       .DC_Mr	(DC_Mr),
       .DC_Mw	(DC_Mw),
       .DC_Rd	(DC_Rd),
       .DC_S	(DC_S),
       .DC_T	(DC_T),
       .D_J	(D_J),
       .D_Mr	(D_Mr),
       .D_Mw	(D_Mw),
       .D_Rd	(D_Rd),
       .D_S	(D_S),
       .D_T	(D_T),
       .EM_J	(EM_J),
       .H_H	(H_H),
       .I_I	(I_I)
   );

   decode_decode DECODE_DECODE (
       .D_Rd	(D_Rd),
       .D_Ra	(D_Ra),
       .D_Rc	(D_Rc),
       .D_Rb	(D_Rb),
       .D_S	(D_S),
       .D_H	(D_H),
       .D_T	(D_T),
       .D_J	(D_J),
       .D_RFa	(D_RFa),
       .D_RFb	(D_RFb),
       .D_B	(D_B),
       .D_C	(D_C),
       .D_A	(D_A),
       .D_SF	(D_SF),
       .D_Ca	(D_Ca),
       .D_Op	(D_Op),
       .FD_I	(FD_I),
       .D_Mr	(D_Mr),
       .D_Mt	(D_Mt),
       .D_Mw	(D_Mw),
       .R_A	(R_A),
       .R_B	(R_B)
   );


   decode_hazard DECODE_HAZARD (
       .DE_Mr	(DE_Mr),
       .DE_Rd	(DE_Rd),
       .D_Ra	(D_Ra),
       .D_Rb	(D_Rb),
       .EM_J	(EM_J),
       .H_H	(H_H)
   );


   decode_rf DECODE_RF (
       .CLK2	(CLK2),
       .D_Ra	(D_Ra),
       .D_Rb	(D_Rb),
       .FD_PC	(FD_PC),
       .I_D	(I_D),
       .I_I	(I_I),
       .I_Rd	(I_Rd),
       .R_A	(R_A),
       .R_B	(R_B),
       .R_CS	(R_CS),
       .R_DS	(R_DS),
       .R_IE	(R_IE),
       .R_M	(R_M)
   );


   execute_alu_bs EXECUTE_ALU_BS (
       .DE_Op	(DE_Op),
       .F_A	(F_A),
       .F_B	(F_B),
       ._E_S	(_E_S)
   );


   execute_alu EXECUTE_ALU (
       .A_D	(A_D),
       .A_F	(A_F),
       .DE_Op	(DE_Op),
       .DE_Ca	(DE_Ca),
       .F_A	(F_A),
       .F_B	(F_B)
   );


   execute_control EXECUTE_CONTROL (
       .A_D	(A_D),
       .DE_J	(DE_J),
       .DE_Mr	(DE_Mr),
       .DE_Mt	(DE_Mt),
       .DE_Mw	(DE_Mw),
       .DE_Rd	(DE_Rd),
       .DE_S	(DE_S),
       .DE_T	(DE_T),
       .EC_D	(EC_D),
       .EC_I	(EC_I),
       .EC_J	(EC_J),
       .EC_Mr	(EC_Mr),
       .EC_Mt	(EC_Mt),
       .EC_Mw	(EC_Mw),
       .EC_Rd	(EC_Rd),
       .EC_S	(EC_S),
       .EC_T	(EC_T),
       .EM_J	(EM_J),
       .I_I	(I_I),
       .I_T	(I_T),
       .PIC_I	(PIC_I),
       .R_IE	(R_IE),
       .S_S	(S_S)
   );


   execute_forward EXECUTE_FORWARD (
       .DE_A	(DE_A),
       .DE_B	(DE_B),
       .DE_C	(DE_C),
       .DE_Ra	(DE_Ra),
       .DE_Rb	(DE_Rb),
       .DE_Rc	(DE_Rc),
       .EM_D	(EM_D),
       .EM_Rd	(EM_Rd),
       .F_A	(F_A),
       .F_B	(F_B),
       .F_C	(F_C),
       .MW_D	(MW_D),
       .MW_Rd	(MW_Rd)
   );


   fetch_control FETCH_CONTROL (
       .EM_J	(EM_J),
       .FC_I	(FC_I),
       .F_I	(F_I),
       .I_I	(I_I)
   );


   fetch_fetch FETCH_FETCH (
       .BUS_A	(BUS_A),
       .BUS_D	(BUS_D),
       .BUS_R	(BUS_R),
       .BUS_W	(BUS_W),
       .CLK0	(CLK0),
       .CLK3	(CLK3),
       .F_I	(F_I),
       .F_PC	(F_PC),
       .R_CS	(R_CS),
       .R_M	(R_M)
   );


   fetch_pc FETCH_PC (
       .CLK1	(CLK1),
       .EM_D	(EM_D),
       .EM_J	(EM_J),
       .F_PC	(F_PC),
       .H_H	(H_H)
   );


   memory_control MEMORY_CONTROL (
       .EM_Mr	(EM_Mr),
       .EM_Mw	(EM_Mw),
       .EM_Rd	(EM_Rd),
       .I_I	(I_I),
       .MC_Ir	(MC_Ir),
       .MC_Mr	(MC_Mr),
       .MC_Mw	(MC_Mw),
       .MC_Rd	(MC_Rd)
   );


   memory_memory MEMORY_MEMORY (
       .BUS_A	(BUS_A),
       .BUS_D	(BUS_D),
       .BUS_R	(BUS_R),
       .BUS_W	(BUS_W),
       .CLK1	(CLK1),
       .CLK2	(CLK2),
       .EM_C	(EM_C),
       .EM_D	(EM_D),
       .EM_Mt	(EM_Mt),
       .MC_Ir	(MC_Ir),
       .MC_Mr	(MC_Mr),
       .MC_Mw	(MC_Mw),
       .M_D	(M_D),
       .R_CS	(R_CS),
       .R_DS	(R_DS)
   );


   memory_skip MEMORY_SKIP (
       .EM_AF	(EM_AF),
       .EM_S	(EM_S),
       .EM_SF	(EM_SF),
       .S_S	(S_S)
   );

   register_de REGISTER_DE (
       .CLK0	(CLK0),
       .DC_J	(DC_J),
       .DC_Mr	(DC_Mr),
       .DC_Mw	(DC_Mw),
       .DC_Rd	(DC_Rd),
       .DC_S	(DC_S),
       .DC_T	(DC_T),
       .DE_A	(DE_A),
       .DE_B	(DE_B),
       .DE_C	(DE_C),
       .DE_Ca	(DE_Ca),
       .DE_J	(DE_J),
       .DE_Mr	(DE_Mr),
       .DE_Mt	(DE_Mt),
       .DE_Mw	(DE_Mw),
       .DE_Op	(DE_Op),
       .DE_PC	(DE_PC),
       .DE_Ra	(DE_Ra),
       .DE_Rb	(DE_Rb),
       .DE_Rc	(DE_Rc),
       .DE_Rd	(DE_Rd),
       .DE_S	(DE_S),
       .DE_SF	(DE_SF),
       .DE_T	(DE_T),
       .D_A	(D_A),
       .D_B	(D_B),
       .D_C	(D_C),
       .D_Ca	(D_Ca),
       .D_Mt	(D_Mt),
       .D_Op	(D_Op),
       .D_Ra	(D_Ra),
       .D_Rb	(D_Rb),
       .D_Rc	(D_Rc),
       .D_SF	(D_SF),
       .FD_PC	(FD_PC)
   );

   register_em REGISTER_EM (
       .A_F	(A_F),
       .CLK0	(CLK0),
       .DE_PC	(DE_PC),
       .DE_SF	(DE_SF),
       .EC_D	(EC_D),
       .EC_I	(EC_I),
       .EC_J	(EC_J),
       .EC_Mr	(EC_Mr),
       .EC_Mt	(EC_Mt),
       .EC_Mw	(EC_Mw),
       .EC_Rd	(EC_Rd),
       .EC_S	(EC_S),
       .EC_T	(EC_T),
       .EM_AF	(EM_AF),
       .EM_C	(EM_C),
       .EM_D	(EM_D),
       .EM_I	(EM_I),
       .EM_J	(EM_J),
       .EM_Mr	(EM_Mr),
       .EM_Mt	(EM_Mt),
       .EM_Mw	(EM_Mw),
       .EM_PC	(EM_PC),
       .EM_Rd	(EM_Rd),
       .EM_S	(EM_S),
       .EM_SF	(EM_SF),
       .EM_T	(EM_T),
       .F_C	(F_C)
   );

   register_fd REGISTER_FD (
       .CLK0	(CLK0),
       .FD_I	(FD_I),
       .FD_PC	(FD_PC),
       .F_I	(F_I),
       .F_PC	(F_PC),
       .H_H	(H_H)
   );

   register_mw REGISTER_MW (
       .CLK0	(CLK0),
       .EM_I	(EM_I),
       .EM_PC	(EM_PC),
       .EM_T	(EM_T),
       .MC_Rd	(MC_Rd),
       .MW_D	(MW_D),
       .MW_I	(MW_I),
       .MW_IE	(MW_IE),
       .MW_PC	(MW_PC),
       .MW_Rd	(MW_Rd),
       .MW_T	(MW_T),
       .M_D	(M_D),
       .R_IE	(R_IE)
   );

   writeback_interrupts WRITEBACK_INTERRUPTS (
       .I_D	(I_D),
       .I_I	(I_I),
       .I_Rd	(I_Rd),
       .I_T	(I_T),
       .MW_D	(MW_D),
       .MW_I	(MW_I),
       .MW_IE	(MW_IE),
       .MW_PC	(MW_PC),
       .MW_Rd	(MW_Rd),
       .MW_T	(MW_T)
   );

endmodule
