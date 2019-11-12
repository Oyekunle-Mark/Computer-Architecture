"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # set memory to a list of 256 zeros
        self.ram = [0] * 256
        # set registers to a list of 8 zeros
        self.reg = [0] * 8
        # set program counter to zero
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""

        # handle exception with a try/except block
        try:
            # initialize address to zero
            address = 0

            # open file name using the with command
            with open(filename, "r") as f:
                # loop through every line in f
                for line in f:
                    # split the line on an #
                    split_line = line.split("#")
                    # initialize command to the left item in the split operation
                    # and call strip on it
                    command = split_line[0].strip()

                    # check if command is an empty string
                    if command == "":
                        # it's a comment, continue
                        continue

                    # convert the binary command to integer using the int function
                    command = int(command, 2)
                    # add command to self.ram at index address
                    self.ram_write(command, address)
                    # increment address
                    address += 1
        except FileNotFoundError:
            # print error message
            print(f"Error: No such file or directory: {filename}")
            # call sys.exit with a positive integer
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # set the variable MUL to it's numberic value
        MUL = 0b10100010

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        # compare if op equals MUL
        elif op == MUL:
            # set self.reg at index reg_a to the value at self.reg at index reg_a
            # multiplied by value at self.reg at index reg_b
            self.reg[reg_a] *= self.reg[reg_b]

        # raise an exception if the op is not supported
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, memory_address):
        """
        Returns the value stored at memory_address index
        of the ram
        """
        # return value at memory_address
        return self.ram[memory_address]

    def ram_write(self, memory_data, memory_address):
        """
        Writes memory_data to index memory_address of
        the ram
        """
        # write memory_data to index memory_address of ram
        self.ram[memory_address] = memory_data

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # set the variable HLT to numeric value
        HLT = 0b00000001
        # set the variable LDI to numeric value
        LDI = 0b10000010
        # set the variable PRN to numeric value
        PRN = 0b01000111

        # loop while True
        while True:
            # read a copy of the current instruction and
            # store it in the a variable IR
            IR = self.ram_read(self.pc)
            # set instruction_size to default 1
            instruction_size = 1
            # read byte at PC + 1 and store it in operand_a
            operand_a = self.ram_read(self.pc + 1)
            # read byte at PC + 2 and store it in operand_b
            operand_b = self.ram_read(self.pc + 2)

            # the third bit in the IR indicates if the operation is to
            # be performed by the ALU, we have to extract it
            # mask IR by 00100000
            masked_IR = IR & 0b00100000
            # bitwise shift it to the right 5 times and store the result in is_alu_operation
            is_alu_operation = masked_IR >> 5

            # check if is_alu_operation is true
            if is_alu_operation:
                # call alu with IR, operand_a, operand_b
                self.alu(IR, operand_a, operand_b)
                # increment instruction size by the operand size
                instruction_size += IR >> 6

            # compare if IR equals HLT
            elif IR == HLT:
                # call sys.exit with a zero as parameter
                sys.exit(0)

            # compare if IR equals LDI
            elif IR == LDI:
                # set self.reg at index operand_a to operand_b
                self.reg[operand_a] = operand_b
                # increment the instruction_size by the operand_size
                instruction_size += IR >> 6

            # compare if IR equals PRN
            elif IR == PRN:
                # get the value at index operand_a of self.reg
                byte_read = self.reg[operand_a]
                # print byte_read
                print(byte_read)
                # increment instruction_size by operand size 1
                instruction_size += IR >> 6

            # add the value of instruction_size to the register PC
            self.pc += instruction_size
