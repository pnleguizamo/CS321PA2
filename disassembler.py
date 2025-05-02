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

def disassemble_i_type(binary_instruction):
    opcode = (binary_instruction >> 21) & 0x7FF  # Extract opcode bits
    
    rd = (binary_instruction >> 0) & 0x1F
    rn = (binary_instruction >> 5) & 0x1F
    imm = (binary_instruction >> 10) & 0xFFF
    
    if opcode == 0x488 or opcode == 0x489: # ADDI instruction
        return f"ADDI X{rd}, X{rn}, #{imm}"
    
    if opcode == 0x490 or opcode == 0x491: # ANDI instruction
        return f"ANDI X{rd}, X{rn}, #{imm}"
    
    if opcode == 0x690 or opcode == 0x691: # EORI instruction
        return f"EORI X{rd}, X{rn}, #{imm}"
    
    if opcode == 0x590 or opcode == 0x591: # ORRI instruction
        return f"ORRI X{rd}, X{rn}, #{imm}"
    
    if opcode == 0x688 or opcode == 0x689: # SUBI instruction
        return f"SUBI X{rd}, X{rn}, #{imm}"
    
    if opcode == 0x788 or opcode == 0x789: # SUBIS instruction
        return f"SUBIS X{rd}, X{rn}, #{imm}"
    
    else:
        return "UNKNOWN"
    

f = open(sys.argv[1], "rb")
while(f):
    byte = f.read(4)
    if not byte:
        break 
    instruction = int.from_bytes(byte)
    print(disassemble_i_type(instruction))
    # print(hex(instruction))