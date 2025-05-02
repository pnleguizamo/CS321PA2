import sys

def disassemble_r_type(binary_instruction):
    opcode = (binary_instruction >> 21) & 0x7FF  # Extract opcode bits
    
    rd = (binary_instruction >> 0) & 0x1F
    rn = (binary_instruction >> 5) & 0x1F
    rm = (binary_instruction >> 16) & 0x1F
    
    if opcode == 0x458: # ADD instruction
        return f"ADD X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x450: # AND instruction
        return f"AND X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x650: # EOR instruction
        return f"EOR X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x69B: # LSL instruction
        shamt = (binary_instruction >> 10) & 0x3F
        return f"LSL X{rd}, X{rn}, #{shamt}"
    
    if opcode == 0x69A: # LSR instruction
        shamt = (binary_instruction >> 10) & 0x3F
        return f"LSR X{rd}, X{rn}, #{shamt}"
    
    if opcode == 0x550: # ORR instruction
        return f"ORR X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x658: # SUB instruction
        return f"SUB X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x758: # SUBS instruction
        return f"SUBS X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x4D8: # MUL instruction
        return f"MUL X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x7FD: # PRNT instruction
        return f"PRNT X{rd}"
    
    if opcode == 0x7FC: # PRNL instruction
        return f"PRNL"
    
    if opcode == 0x7FE: # DUMP instruction
        return f"DUMP"
    
    if opcode == 0x7FF: # HALT instruction
        return f"HALT"
    else:
        return "UNKNOWN"

f = open(sys.argv[1], "rb")
while(f):
    byte = f.read(4)
    if not byte:
        break 
    instruction = int.from_bytes(byte)
    print(disassemble_r_type(instruction))
    # print(hex(instruction))