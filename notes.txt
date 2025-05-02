# CS321PA2

ADD - R 0x458
ADDI - I 0x488 0x489
AND - R 0x450
ANDI - I 0x490 0x491
B - B 000101
B.cond: This is a CB instruction in which the Rt field is not a register, but a code that indicates the condition extension. These have the values (base 16): 01010100
        0: EQ
        1: NE
        2: HS
        3: LO
        4: MI
        5: PL
        6: VS
        7: VC
        8: HI
        9: LS
        a: GE
        b: LT
        c: GT
        d: LE
BL - B 100101
BR: The branch target is encoded in the Rn field. - R 0x6B0
CBNZ - CB 10110101
CBZ - CB 10110100
EOR - R 0x650
EORI - I 0x690 0x691
LDUR - D 0x7C2
LSL: This instruction uses the shamt field to encode the shift amount, while Rm is unused. - R 0x69B
LSR: Same as LSL. - R 0x69A
ORR - R 0x550
ORRI - I 0x590 0x591
STUR - D 0x7C0
SUB - R 0x658
SUBI - I 0x688 0x689
SUBIS - I 0x788 0x789
SUBS - R 0x758
MUL - R 0x4D8
PRNT: This is an added instruction (part of our emulator, but not part of LEG or ARM) that prints a register name and its contents in hex and decimal.  This is an R instruction.  The opcode is 11111111101. The register is given in the Rd field.
PRNL: This is an added instruction that prints a blank line.  This is an R instruction.  The opcode is 11111111100.
DUMP: This is an added instruction that displays the contents of all registers and memory, as well as the disassembled program.  This is an R instruction.  The opcode is 11111111110.
HALT: This is an added instruction that triggers a DUMP and terminates the emulator.  This is an R instruction.  The opcode is 11111111111