import sys
import csv

JTAG_Data = [0] * 288


class std_logic(object):
    """docstring for std_logic."""

    def __init__(self, dPin, ePin):
        self.dPin = dPin
        self.ePin = ePin

    def set_value(self, value):
        global JTAG_Data
        JTAG_Data[self.dPin] = value
        JTAG_Data[self.ePin] = 1
    def disable(self):
        global JTAG_Data
        JTAG_Data[self.ePin] = 0





Main_Bus = [std_logic(143, 142), std_logic(140, 139), std_logic(134, 133), std_logic(128, 127), std_logic(125, 124), std_logic(122, 121), std_logic(116, 115), std_logic(110, 109)]
Count = std_logic(224, 223)
CounterOutControl = std_logic(218, 217)
LowJumpRegLoad = std_logic(197, 197)
HighJumpRegLoad = std_logic(194, 193)
JumpEnable = std_logic(191, 190)
MemWriteControl = std_logic(173, 172)
InsRegControl = std_logic(215, 214)

#Everything else needs to be in the disable state; drive reset?

#these are otheroutput pins
CLK = std_logic(14, 13)
MainRegOutputControl =  std_logic(185, 184) #set high
MemOutEnable =  std_logic(179, 178) # set high
Ram_Addr_Enable =  std_logic(161, 160)# set high
StackOutControl =  std_logic(149, 148)# set high


def Bus_Write(BUS, VECTOR):
    for bit in range(len(BUS)):
        BUS[bit].set_value(int(VECTOR[-(bit+1)]))


def read_binaries(file_name):
    if file_name.split(".")[-1] == "bin":
        try:
            f = open(file_name, 'r')
            program = f.read()
            f.close()
            instructions = program.split()
        except Exception as e:
            print("Incorrect Input file was specified")
            exit()
    elif file_name.split(".")[-1] == "hex":
        f = open(file_name, 'r')
        program = f.read()
        f.close()
        n = 2
        hex = [program[i:i+n] for i in range(0, len(program), n)]
        numerical = [(int(hexed, 16)) for hexed in hex[0:-1]]
        n = 8
        instructions = ['{0:{fill}{width}b}'.format(
            (x + 2**n) % 2**n, fill='0', width=n) for x in numerical]
    else:
        print("bang")
        print("Incorrect Input file was specified")
        exit()
    return instructions



Data_Bank = []


def main():

    #bootup sequence (puts pins to safe values)
    global Data_Bank
    MainRegOutputControl.set_value(1)
    MemOutEnable.set_value(1)
    Ram_Addr_Enable.set_value(1)
    StackOutControl.set_value(1)
    CLK.set_value(0)
    InsRegControl.set_value(0)

    Test_Sequence = "10101010"
    #display test data
    Bus_Write(Main_Bus, Test_Sequence)
    Data_Bank.append(JTAG_Data.copy())
    
    ##INIT COMPLETE##

    # #step1 intialise counter
    # Bus_Write(Main_Bus, "00000000")
    # Count.set_value(0)
    # CounterOutControl.set_value(0) #Count Output
    # MemWriteControl.set_value(1) #disable writing
    # LowJumpRegLoad.set_value(0) #prepare to Jump
    # HighJumpRegLoad.set_value(0) #prepare to Jump
    # JumpEnable.set_value(1) #prepare to Jump
    # Data_Bank.append(JTAG_Data.copy())
    #
    # #latch the Buffers
    # LowJumpRegLoad.set_value(1)
    # HighJumpRegLoad.set_value(1)
    # Data_Bank.append(JTAG_Data.copy())
    #
    # #Preset the Counter
    # Count.set_value(1)
    # LowJumpRegLoad.set_value(0) #probs not necessary
    # HighJumpRegLoad.set_value(0) #probs not necessary
    # Data_Bank.append(JTAG_Data.copy())


    # instructions = read_binaries(sys.argv[1])
    # for instruction in instructions:
    #     #bang out the instructon
    #     JumpEnable.set_value(0)
    #     Count.set_value(0)
    #     Bus_Write(Main_Bus, instruction)
    #     Data_Bank.append(JTAG_Data.copy())
    #

    # # write in the data
    # Bus_Write(Main_Bus, "11001100")
    # Count.set_value(0)
    # JumpEnable.set_value(0)
    # MemWriteControl.set_value(0)
    # Data_Bank.append(JTAG_Data.copy())
    #
    #
    # #disable writing and show something differnet
    # MemWriteControl.set_value(1)
    # Bus_Write(Main_Bus, "00110011")
    # Data_Bank.append(JTAG_Data.copy())


    # #relenquish the bus
    # for signal in Main_Bus:
    #     signal.disable()
    # #drive the ram
    # MemOutEnable.set_value(0)
    # Data_Bank.append(JTAG_Data.copy())




    # Bus_Write(Main_Bus, "11111111")
    # Data_Bank.append(JTAG_Data.copy())
    # LowJumpRegLoad.set_value(1)
    # HighJumpRegLoad.set_value(1)
    # Count.set_value(0)
    # JumpEnable.set_value(1) #prepare to Jump
    # Data_Bank.append(JTAG_Data.copy())
    # Count.set_value(1) #counter has been preset
    # Data_Bank.append(JTAG_Data.copy())

    flat_Data = [item for sublist in Data_Bank for item in sublist]
    with open("blank.c" ,"r") as f:
        data = f.read()
    data = (data.split("\n"))
    data[6] = "#define BANKLENGTH " + str(len(flat_Data)//288)
    data[7] = ("prog_uint8_t data[] = " + str(flat_Data)+";").replace("[","{").replace("]", "}")
    data[7] = list(data[7])
    data[7][17] = "["
    data[7][18] = "]"
    data[7] = "".join(data[7])

    with open("out.c", "w") as f:
        for line in data:
            f.write(line + "\n")

    print("sucess")


main()
