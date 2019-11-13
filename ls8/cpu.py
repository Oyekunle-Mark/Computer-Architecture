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
        # R7 is reserved as the stack pointer (SP)
        # On power on, r7 is set to 0xF4
        self.reg[7] = 0xF4
        # set program counter to zero
        self.pc = 0
        # set instruction_size to default 1
        self.instruction_size = 1
        # set the branch table to am empty dictionary
        self.branch_table = {}

        # Store the numeric values of opcodes
        # set the variable HLT to numeric value
        HLT = 0b00000001
        # set the variable LDI to numeric value
        LDI = 0b10000010
        # set the variable PRN to numeric value
        PRN = 0b01000111
        # set the variable PUSH to its numeric  value
        PUSH = 0x01000101
        # set the variable POP to its numeric  value
        POP = 0x01000110

        # set up the branch table
        self.branch_table[HLT] = self.handle_hlt
        self.branch_table[LDI] = self.handle_ldi
        self.branch_table[PRN] = self.handle_prn
        self.branch_table[PUSH] = self.handle_push
        self.branch_table[POP] = self.handle_pop

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
        # loop while True
        while True:
            # read a copy of the current instruction and
            # store it in the a variable IR
            IR = self.ram_read(self.pc)
            # reset the instruction_size to 1
            self.instruction_size = 1
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
                self.instruction_size += IR >> 6

            # if not an alu operation, use the branch table
            # to find the right method
            else:
                # call branch table at index IR, and pass in IR, operand_a and operand_b as args.
                self.branch_table[IR](IR, operand_a, operand_b)

            # add the value of instruction_size to the register PC
            self.pc += self.instruction_size

    def handle_hlt(self, op=None, opr1=None, opr2=None):
        # call sys.exit with a zero as parameter
        sys.exit(0)

    def handle_ldi(self, op, opr1, opr2):
        # set self.reg at index opr1 to opr2
        self.reg[opr1] = opr2
        # increment the instruction_size by the operand_size
        self.instruction_size += op >> 6

    def handle_prn(self, op, opr1, opr2=None):
        # get the value at index opr1 of self.reg
        byte_read = self.reg[opr1]
        # print byte_read
        print(byte_read)
        # increment instruction_size by operand size 1
        self.instruction_size += op >> 6

    def handle_push(self, op, opr1, opr2=None):
        # Decrement the stack pointer
        # simply decrement the value at self.reg[7]
        self.reg[7] -= 1
        # get the value at the index opr1 of self.reg
        byte_read = self.reg[opr1]
        # write the value to self.ram using ram_write passing the value and stack pointer
        self.ram_write(byte_read, self.reg[7])
        # increment the instruction_size by the operand_size
        self.instruction_size += op >> 6

    def handle_pop(self, op, opr1, opr2=None):
        # read the value at sp of self.ram using ram_read
        byte_read = self.ram_read(self.reg[7])
        # write byte_read to the register at index opr1
        self.reg[opr1] = byte_read
        # increment the stack pointer
        # simply increment the value at self.reg[7]
        self.reg[7] += 1
        # increment the instruction_size by the operand_size
        self.instruction_size += op >> 6
