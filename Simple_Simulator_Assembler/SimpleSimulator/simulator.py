memory = {}

# INITIALIZE MEMORY
for i in range(128):
    key = format(i, '07b')  # Convert the index to 8-bit binary string , '08b' pads the address if need be .
    memory[key] = "0" * 16  # Initialize all the key values as a 16-bit string of zeros

Instruction_list = []

while True:
    try:
        line = input()
    except EOFError:
        break
    binary_string = line.strip()  # Remove leading/trailing whitespace, including the newline character
    Instruction_list.append(binary_string)

k = len(Instruction_list)

# setting the instructions in the memory
# the instructions are in the first k memory addresses of the memory

for i in range(k):
    key = format(i, '07b')
    memory[key] = Instruction_list[i]


# to get idea of opcode type which will be of help in the EX unit
def opcode_type(opcode):
    opcode_info = {"00000": "add", "00001": "sub", "00010": "mov1", "00011": "movr", "00100": "ld",
                   "00101": "st", "00110": "mul", "00111": "div", "01000": "rs ", "01001": "ls", "01010": "xor",
                   "01011": "or", "01100": "and", "01101": "not", "01110": "cmp", "01111": "jmp", "11100": "jlt",
                   "11101": "jgt", "11111": "je", "11010": "hlt", "10010": "movf", "10001": "subf", "10000": "addf"}
    for key in opcode_info:
        if key == opcode:
            return opcode_info[key]


# need to return it as a  16 bit value .
reg = {"PC": 0, "000": 0, "001": 0, "010": 0, "011": 0,
       "100": 0, "101": 0, "110": 0, "111": "0" * 16, }


# FLAGS OPERATIONS
def clearFlag():
    reg["111"] = "0" * 16


def Overflow():
    reg["111"] = "0" * 12 + "1" + "000"
    return


def Less():
    reg["111"] = "0" * 13 + "1" + "00"
    return


def Greater():
    clearFlag()
    reg["111"] = "0" * 14 + "1" + "0"
    return


def Equal():
    reg["111"] = "0" * 15 + "1"
    return


# The values in registers are integers , before printing we convert them to 16 bit binary

def dec_to_bin16(number):
    # doubt , the number is value stored in the register which I guess is an integer , check mov command
    # I have to make sure that decimal value of immediate value is unloaded in the register .check mov1
    binary = bin(int(number) & 0xffff)[2:]  # Convert number to 16-bit binary string
    binary = binary.zfill(16)  # Pad with leading zeros if necessary
    return binary


def dec_to_bin7(decimal):
    binary = bin(decimal)[2:]  # Convert decimal to binary string
    binary = binary.zfill(7)  # Pad with leading zeros to ensure 7 bits
    return binary


'''def find_first_one(string):
    for index, char in enumerate(string):
        if char == '1':
            return index
    return -1

def float_to_binary(flt):
    whole, dec = str(float(flt)).split(".")
    print("Whole part:", whole)
    whole = bin(int(whole))[2:].zfill(5)  # Convert whole part to binary and remove '0b' prefix
    print("Whole part (binary):", whole)

    dec = "0." + dec
    print("Decimal part:", dec)

    binary_dec = ""
    i = 0
    while float(dec) != 0.0 and i < 5:
        dec = str(float(dec) * 2)
        bit = dec.split(".")[0]
        print("bit:", bit)
        dec = "0." + dec.split(".")[1]
        dec = float(dec)
        print("dec:", dec)
        binary_dec += bit
        i += 1

    binary_dec = binary_dec + "00000"
    print("Decimal part (binary):", binary_dec)
    k = whole + binary_dec
    print("Binary representation:", k)

    idx = find_first_one(k)
    if not (-3 <= len(whole) - idx <= 5):
        print("Invalid floating-point number")
        return None

    print("1 + mantissa:", k[:idx + 1] + "." + k[idx + 1:])
    exp = len(whole) - (idx + 1)
    print("exp:", exp)
    E = exp + 3  # bias 3
    bin_exp = bin(E)[2:].zfill(3)
    print("E:", E)
    print("bin_exp:", bin_exp)
    mantissa = k[idx + 1 :][:5]
    print("mantissa:", mantissa)
    converted_binary = bin_exp + mantissa

    print("Converted binary:", converted_binary)
    if len(converted_binary) < 8:
        converted_binary = "0" * (8 - len(converted_binary)) + converted_binary

    print("Final binary:", converted_binary)
    return converted_binary

n = input("Enter a floating-point number: ")
k = float_to_binary(n)

def binary_to_float(string):
    E = string[:3]
    e = int(E, 2) - 3
    mantissa = string[3:]
    p = "000001" + mantissa
    print(p)
    idx = 5 + e
    p = p[:idx + 1] + "." + p[idx + 1:]
    whole, dec = p.split(".")
    bit = 0
    for i in range(len(whole)):
        bit += int(whole[i]) * (2 ** (len(whole) - i - 1))
    for j in range(len(dec)):
        bit += int(dec[j]) * (2 ** (-j - 1))
    return bit

result = binary_to_float(k)
print("Converted back to float:", result)

 '''


def add(reg, instruction):
    # type A
    filler_bits = instruction[5:7]
    clearFlag()
    reg1 = instruction[7:10]
    reg2 = instruction[10: 13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg3] + reg[reg2]
    if reg[reg1] > 65535:  # 2^16 = 65535 which is the max value that can be stored in a register.
        Overflow()

    reg[reg1] = reg[reg1] % 65536

    # state of registers after each instruction is executed .
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if key != "PC":
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    # print the simulator status in the desired format , DONE
    # I dont have a 8 bit PC , I still dont , maybe now , dont think it will generate accurate values though ...
    # i have incremented the value of PC by 16 bits ( moving to next memory address ) after each instruction , shayad se 1  bit bhi ho skti hai
    # neither 16 bit data values for registeres ,  I do  now ....
    # and ra is supposed to be free ig  , DONT KNOW done without ra .
    reg["PC"] += 1


def sub(reg, instruction):
    # type A
    filler_bits = instruction[5:7]
    clearFlag()
    reg1 = instruction[7:10]
    reg2 = instruction[10: 13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg2] - reg[reg3]
    if reg[reg1] < 0:
        Overflow()
        reg[reg1] = 0

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] += 1


# reg to reg
def movr(reg, instruction):
    # type c
    reg1 = instruction[10:13]
    reg2 = instruction[13:]
    # of type mov reg FLAGS
    # the instruction reads FLAGS register and writes the data into reg1
    # the format in FLAGS register is binary
    # whereas we are storing int type right now into our registers ...
    # we are not clearing the flag before making use of the register
    if reg2 == "111":
        reg[reg1] = int(reg[reg2], 2)


    else:
        reg[reg1] = reg[reg2]

    # clearing the flag
    clearFlag()

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] += 1


# NOT SURE ,made changes
def mov1(reg, instruction):
    # type b
    reg1 = instruction[6:9]
    imm_val = instruction[9:]
    '''mem_address = instruction[8:] # memory address from which the value is to be loaded 
    imm_val = memory[mem_address] # imm_val is stored in the mem_address which is in the memory
    reg[reg1] = imm_val  # moves the immediate value into the specified register 
    '''
    # moves the decimal val of immediate unto the register .
    reg[reg1] = int(imm_val, 2)
    clearFlag()

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    # Print a newline after the loop
    reg["PC"] += 1


def ld(reg, instruction):
    # type d
    clearFlag()
    filler_bit = instruction[5]
    reg1 = instruction[6:9]
    mem_address = instruction[9:]
    if mem_address in memory:
        reg[reg1] = int(memory[mem_address], 2)
    # the memory contains all the values as binary numbers ,
    #  whereas we want the the value in registers to be of integer format

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] += 1


# doubt

def st(reg, instruction):
    clearFlag()
    reg1 = instruction[6:9]  # figures out the register
    mem_address = instruction[9:]  # figures out the mem_address to which the data is transfered
    data = reg[reg1]
    mem_data = dec_to_bin16(data)  # takes the data from reg1 , which is in integer form , converts to binary
    memory[mem_address] = mem_data  # stores the  binary data in the specified mem_address
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])  # Print a newline after the loop

    reg["PC"] += 1


def mul(reg, instruction):
    # type A
    clearFlag()

    filler_bits = instruction[5:7]
    reg1 = instruction[7:10]
    reg2 = instruction[10:13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg2] * reg[reg3]
    if reg[reg1] > 65535:
        Overflow

        reg[reg1] = 0

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])  # Print a newline after the loop
    reg["PC"] += 1


# recheck
def div(reg, instruction):
    # type  c
    clearFlag()
    reg3 = instruction[10:13]
    reg4 = instruction[13:]

    if reg[reg4] == 0:
        Overflow()
        reg['000'] = 0
        reg['001'] = 0
    else:
        reg['000'] = reg[reg3] // reg[reg4]
        reg['001'] = reg[reg3] % reg[reg4]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    print()

    reg["PC"] += 1


def rs(reg, instruction):
    clearFlag()
    reg1 = instruction[6:9]
    imm_val = instruction[9:]  # is binary
    shift_value = int(imm_val, 2)  # convert to int to signify no of places
    reg[reg1] = reg[reg1] >> shift_value  # >> right shift operator

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


def ls(reg, instruction):
    clearFlag()
    reg1 = instruction[6:9]
    imm_val = instruction[9:]  # is binary
    shift_value = int(imm_val, 2)  # convert to int to signify no of places
    reg[reg1] = reg[reg1] << shift_value  # << left  shift operator

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


def xor(reg, instruction):
    # type a
    clearFlag()
    filler_bits = instruction[5:7]
    reg1 = instruction[7:10]
    reg2 = instruction[10:13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg2] ^ reg[reg3]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] += 1


def or_(reg, instruction):
    # type a
    clearFlag()
    filler_bits = instruction[5:7]
    reg1 = instruction[7:10]
    reg2 = instruction[10:13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg2] | reg[reg3]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


def and_(reg, instruction):
    # type a
    clearFlag()
    filler_bits = instruction[5:7]
    reg1 = instruction[7:10]
    reg2 = instruction[10:13]
    reg3 = instruction[13:]
    reg[reg1] = reg[reg2] & reg[reg3]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


# check
def not_(reg, instruction):
    # type  c
    clearFlag()
    reg1 = instruction[10:13]
    reg2 = instruction[13:]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


def cmp(reg, instruction):
    # type c
    clearFlag()
    reg1 = instruction[10:13]
    reg2 = instruction[13:]
    if reg[reg1] == reg[reg2]:
        Equal()
    if reg[reg1] > reg[reg2]:
        reg["111"] = "0" * 14 + "1" + "0"
    if reg[reg1] < reg[reg2]:
        Less()
    k = reg["111"]

    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


# doubt
def jmp(reg, instruction):
    # When to clear the flag ?
    mem_address = instruction[9:]
    clearFlag()
    link_register_value = reg["PC"] + 1
    reg["PC"] = int(mem_address, 2)
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])
    reg["PC"] += 1


def jlt(reg, instruction):
    # When to clear the flag ?
    mem_address = instruction[9:]
    link_register_value = reg["PC"] + 1
    if reg["111"][-3] == "1":
        reg["PC"] = int(mem_address, 2)

    clearFlag()
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] = link_register_value


def jgt(reg, instruction):
    mem_address = instruction[9:]
    link_register_value = reg["PC"] + 1
    if reg["111"][-2] == "1":
        reg["PC"] = int(mem_address, 2)

    clearFlag()
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    print(reg["111"])

    reg["PC"] = link_register_value


def je(reg, instruction):
    mem_address = instruction[9:]
    link_register_value = reg["PC"] + 1

    if reg["111"][-1] == "1":  # checks if equal flag is set
        reg["PC"] = int(mem_address, 2)

    clearFlag()  # binary
    for key in reg:
        if key == "PC":
            print(dec_to_bin7(reg["PC"]), end="        ")
        if key == "111":
            break
        else:
            if (key != "PC"):
                print(dec_to_bin16(reg[key]), end=" ")
    reg["PC"] = link_register_value


i = 0
while i < k:
    instruction = Instruction_list[i]
    opcode = instruction[:5]
    opcode_result = opcode_type(opcode)

    if opcode_result == "add":
        add(reg, instruction)

    if opcode_result == "sub":
        sub(reg, instruction)

    if opcode_result == "mov1":
        mov1(reg, instruction)

    if opcode_result == "movr":
        movr(reg, instruction)

    if opcode_result == "ld":
        ld(reg, instruction)

    if opcode_result == "st":
        st(reg, instruction)
    if opcode_result == "mul":
        mul(reg, instruction)

    if opcode_result == "div":
        div(reg, instruction)

    if opcode_result == "rs":
        rs(reg, instruction)

    if opcode_result == "ls":
        ls(reg, instruction)

    if opcode_result == "xor":
        xor(reg, instruction)

    if opcode_result == "or":
        or_(reg, instruction)

    if opcode_result == "and":
        and_(reg, instruction)

    if opcode_result == "not":
        not_(reg, instruction)

    if opcode_result == "cmp":
        cmp(reg, instruction)

    if opcode_result == "jmp":
        jmp(reg, instruction)

    if opcode_result == "jlt":
        jlt(reg, instruction)

    if opcode_result == "jgt":
        jgt(reg, instruction)

    if opcode_result == "je":
        je(reg, instruction)

    '''if opcode_result == "addf":
        addf(reg ,instruction)

    if opcode_result == "subf":
        subf(reg ,instruction)

    if opcode_result == "movf":
        movf(reg ,instruction)
'''
    if opcode_result == "hlt":

        for key in reg:
            if key == "PC":
                print(dec_to_bin7(reg["PC"]), end="        ")
            if key == "111":
                break
            else:
                if (key != "PC"):
                    print(dec_to_bin16(reg[key]), end=" ")
        print(reg["111"])
        break
    i += 1

# After exiting the while loop , print the memory dump
for mem_address in memory:
    print(memory[mem_address])
