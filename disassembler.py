import sys
import math

rMap = dict()
rMap[0x458] = "ADD"
rMap[0x450] = "AND"
rMap[0x650] = "EOR"
rMap[0x69B] = "LSL"
rMap[0x69A] = "LSR"
rMap[0x550] = "ORR"
rMap[0x658] = "SUB"
rMap[0x758] = "SUBS"
rMap[0x4D8] = "MUL"
rMap[0x7FD] = "PRNT"
rMap[0x7FC] = "PRNL"
rMap[0x7FE] = "DUMP"
rMap[0x7FF] = "HALT"

iMap = dict()
iMap[0x488] = "ADDI"
iMap[0x489] = "ADDI"
iMap[0x490] = "ANDI"
iMap[0x491] = "ANDI"
iMap[0x690] = "EORI"
iMap[0x691] = "EORI"
iMap[0x590] = "ORRI"
iMap[0x591] = "ORRI"
iMap[0x688] = "SUBI"
iMap[0x689] = "SUBI"
iMap[0x788] = "SUBIS"
iMap[0x789] = "SUBIS"

dMap= dict()
dMap[0x7C2] = "LDUR"
dMap[0x7C0] = "STUR"

# B 11 bit opcode range 0x0A0 to 0xOBF
# B.cond 11 bit opcode range 0x2A0 to 0x2A7
# CB 11 bit opcode range 0x5A0 to 0x5AF

# Range is inclusive of start and exclusive of end
# Add 1 to the end
bRange = range(0x0A0, 0x0C0) 
blRange = range(0x4A0, 0x4CF)    
bCondRange = range(0x2A0, 0x2A8)  
cbRange = range(0x5A0, 0x5B0)

def disassemble(instruction):
    opcode = (instruction >> 21) & 0x7FF

    if opcode in rMap:
        return disassemble_r_type(instruction)
    elif opcode in iMap:
        return disassemble_i_type(instruction)
    elif opcode in dMap:
        return disassemble_d_type(instruction)
    elif opcode in bRange or opcode in blRange:
        return disassemble_b_type(instruction)
    elif opcode in bCondRange:
        return disassemble_b_cond_type(instruction)
    elif opcode in cbRange:
        return disassemble_cb_type(instruction)
    else:
        return "UNKNOWN"


def disassemble_b_type(binary_instruction):
    opcode = (binary_instruction >> 26) & 0x3F  # Extract opcode bits
    BR_address = (binary_instruction >> 0) & 0x3FFFFFF  # Extract the address bits
    BR_address = twos_comp(BR_address, 26)  
    return f"B {BR_address}" if opcode == 0b000101 else f"BL {BR_address}"

def disassemble_b_cond_type(binary_instruction):
    rd = (binary_instruction >> 0) & 0x1F
    BR_address = (binary_instruction >> 5) & 0x7FFFF  # Extract the address bits
    BR_address = twos_comp(BR_address, 19)  
    condition_map = {
        0x0: "EQ",
        0x1: "NE",
        0x2: "HS",
        0x3: "LO",
        0x4: "MI",
        0x5: "PL",
        0x6: "VS",
        0x7: "VC",
        0x8: "HI",
        0x9: "LS",
        0xA: "GE",
        0xB: "LT",
        0xC: "GT",
        0xD: "LE",
    }

    condition = condition_map.get(rd, "UNKNOWN")  # Unknown is default if rd is not in the map
    return f"B.{condition} {BR_address}"

def disassemble_cb_type(binary_instruction):
    opcode = (binary_instruction >> 24) & 0xFF  # Extract opcode bits
    rd = (binary_instruction >> 0) & 0x1F
    BR_address = (binary_instruction >> 5) & 0x7FFFF  # Extract the address bits

    return f"CBZ X{rd}, {BR_address}" if opcode == 0b10110100 else f"CBNZ X{rd}, {BR_address}"


def disassemble_r_type(binary_instruction):
    opcode = (binary_instruction >> 21) & 0x7FF  # Extract opcode bits
    
    rd = (binary_instruction >> 0) & 0x1F
    rn = (binary_instruction >> 5) & 0x1F
    rm = (binary_instruction >> 16) & 0x1F
    
    # if opcode == 0x458: # ADD instruction
    #     return f"ADD X{rd}, X{rn}, X{rm}"
    
    # if opcode == 0x450: # AND instruction
    #     return f"AND X{rd}, X{rn}, X{rm}"
    
    # if opcode == 0x650: # EOR instruction
    #     return f"EOR X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x69B: # LSL instruction
        shamt = (binary_instruction >> 10) & 0x3F
        return f"LSL X{rd}, X{rn}, #{shamt}"
    
    if opcode == 0x69A: # LSR instruction
        shamt = (binary_instruction >> 10) & 0x3F
        return f"LSR X{rd}, X{rn}, #{shamt}"
    
    # if opcode == 0x550: # ORR instruction
    #     return f"ORR X{rd}, X{rn}, X{rm}"
    
    # if opcode == 0x658: # SUB instruction
    #     return f"SUB X{rd}, X{rn}, X{rm}"
    
    # if opcode == 0x758: # SUBS instruction
    #     return f"SUBS X{rd}, X{rn}, X{rm}"
    
    # if opcode == 0x4D8: # MUL instruction
    #     return f"MUL X{rd}, X{rn}, X{rm}"
    
    if opcode == 0x7FD: # PRNT instruction
        return f"PRNT X{rd}"
    
    if opcode == 0x7FC: # PRNL instruction
        return f"PRNL"
    
    if opcode == 0x7FE: # DUMP instruction
        return f"DUMP"
    
    if opcode == 0x7FF: # HALT instruction
        return f"HALT"
    
    elif opcode in rMap:
        return f"{rMap[opcode]} X{rd}, X{rn}, X{rm}"
    else:
        return "UNKNOWN"

def disassemble_i_type(binary_instruction):
    opcode = (binary_instruction >> 21) & 0x7FF  # Extract opcode bits
    
    rd = (binary_instruction >> 0) & 0x1F
    rn = (binary_instruction >> 5) & 0x1F
    imm = (binary_instruction >> 10) & 0xFFF # The textbook says immediates are zero extended, I believe this immediate is unsigned

    if opcode in iMap:
        return f"{iMap[opcode]} X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x488 or opcode == 0x489: # ADDI instruction
    #     return f"ADDI X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x490 or opcode == 0x491: # ANDI instruction
    #     return f"ANDI X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x690 or opcode == 0x691: # EORI instruction
    #     return f"EORI X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x590 or opcode == 0x591: # ORRI instruction
    #     return f"ORRI X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x688 or opcode == 0x689: # SUBI instruction
    #     return f"SUBI X{rd}, X{rn}, #{imm}"
    
    # if opcode == 0x788 or opcode == 0x789: # SUBIS instruction
    #     return f"SUBIS X{rd}, X{rn}, #{imm}"
    
    else:
        return "UNKNOWN"
    
def disassemble_d_type(binary_instruction):
    opcode = (binary_instruction >> 21) & 0x7FF  # Extract opcode bits
    
    rt = (binary_instruction >> 0) & 0x1F
    rn = (binary_instruction >> 5) & 0x1F
    dt_address = (binary_instruction >> 12) & 0x1FF
    dt_address = twos_comp(dt_address, 9)  # Convert to signed 9-bit integer
    
    if opcode == 0x7C2: # LDUR instruction
        return f"LDUR X{rt}, [X{rn}, #{dt_address}]"
    
    if opcode == 0x7C0: # LDUR instruction
        return f"STUR X{rt}, [X{rn}, #{dt_address}]"
    
    
    else:
        return "UNKNOWN"
    
    

def twos_comp(val, bits):
    if (val >> bits - 1 & 0x1): # Check MSB
        val = val ^ int((math.pow(2, bits) - 1)) # flip bits
        val = val + 1 # add 1
        val = -val # make it negative
    return val        

f = open(sys.argv[1], "rb")
lines = []
while(f):
    byte = f.read(4)
    if not byte:
        break 
    instruction = int.from_bytes(byte)
    lines.append(disassemble(instruction))

labels = []
for i, line in enumerate(lines):
    words = line.split(" ")
    if words[0][0] == "B":
        offset = int(words[1])
        lines[i] = f"{words[0]} label{i + offset}"
        labels.append(i+offset)

    if words[0][0] == "C" and words[0][1] == "B":
        offset = int(words[2])
        lines[i] = f"{words[0]} {words[1]} label{i + offset}"
        labels.append(i+offset)



for i, line in enumerate(lines):
    if i in labels:
        line = f"label{i}: {line}"
    print(line)
    