from instruction_set import instruction_set


class StatusRegister(object):
    def __init__(self):
        self.N = False  # negativ
        self.B = False  # break
        self.D = False  # decimal
        self.I = False  # interrupt (IRQ disabled)
        self.Z = False  # zero
        self.C = False  # carry


class Register(object):
    def __init__(self, size):
        self.size = size
        self.value = 0
        
    def set(self, value):
        if value < 0 or value > 2**self.size:
            raise Exception("Wrong value for register: " + value)
        self.value = value
    
    def get(self):
        return self.value
    
    def inc(self):
        self.set(self.value + 1)
    
    def dec(self):
        self.set(self.value - 1)


class CPU(object):
    def __init__(self, memory, console):
        self.memory = memory
        self.console = console
        self.PC = Register(16)  # program counter
        self.A = Register(8)  # accumulator
        self.X = Register(8)  # x register
        self.Y = Register(8)  # y register
        self.SR = StatusRegister()  # status register
        self.SP = Register(8)  # stack pointer
        
    def run(self, address):
        self.PC.set(address)
        
        while True:
            instr = self.fetch()
            self.PC.inc()
            if instr['mnem'] == 'BRK':
                return
            self.execute(instr)
        
    def fetch(self):
        data = self.memory.read(self.PC.get())
        mnem, arg_type, size = instruction_set[data]
        instruction = {'mnem': mnem, 'arg': arg_type}
        
        # fetch instruction with argument
        if size == 1:
            self.PC.inc()
            data = self.memory.read(self.PC.get())
        elif size == 2:
            self.PC.inc()
            val1 = self.memory.read(self.PC.get())
            self.PC.inc()
            val2 = self.memory.read(self.PC.get())
            data = val2*256+val1
        
        # resolve arguments to real address or value
        if arg_type == 'A':
            instruction['value'] = self.A.get()
        elif 'abs' in arg_type:
            if 'X' in arg_type:
                instruction['address'] = data + self.X.get()
            elif 'Y' in arg_type:
                instruction['address'] = data + self.Y.get()
            else:
                instruction['address'] = data
        elif arg_type == '#':
            instruction['value'] = data
        elif arg_type == 'ind':
            instruction['address'] = self.memory.get((data+1)*256) + self.memory.get(data)
        elif 'ind' in arg_type:
            # TODO: implement indirect adressing
            if arg_type == 'X,ind':
                instruction['address'] = (self.memory.get(data+1+self.Y.get()))
            else: # ind,y
                instruction['address'] = (self.memory.get(data+1)*256 + self.memory.get(data)) + self.Y.get()
        elif arg_type == 'rel':
            if data >> 7:
                instruction['address'] = self.PC.get() - data - 128 
            else:
                instruction['address'] = self.PC.get() + data
        elif 'zpg' in arg_type:
            if arg_type == 'zpg,X':
                instruction['address'] = data + self.X.get()
            if arg_type == 'zpg,Y':
                instruction['address'] = data + self.Y.get()
            else:
                instruction['address'] = data
        
        if 'address' in instruction:
            instruction['value'] = self.memory.read(instruction['address'])
        return instruction
        
    def execute(self, instr):
        # prepare
        mnem = instr['mnem']
        #arg_type = instr['arg_type']
        if 'value' in instr:
            value = instr['value']
        if 'address' in instr:
            address = instr['address']
        
        # comands
        if mnem == 'LDA':
            self.A.set(value)
        elif mnem == 'LDX':
            self.X.set(value)
        elif mnem == 'LDY':
            self.Y.set(value)
        elif mnem == 'TAX':
            self.X.set(self.A.get())
        elif mnem == 'TXA':
            self.A.set(self.X.get())
        elif mnem == 'TAY':
            self.Y.set(self.A.get())
        elif mnem == 'TYA':
            self.A.set(self.Y.get())
        elif mnem == 'STA':
            self.memory.write(address, self.A.get())
        elif mnem == 'CLC':
            self.SR.C = False
        elif mnem == 'ADC':
        # TODO: implement carry flag
            self.A.set(self.A.get() + value)
        elif mnem == 'JSR':
            if address == 0xFFD2:
                self.console.putc(self.A.get())
            else:
                raise Exception('Instruction JSR not implemented for anything beside print (FFD2)')
        elif mnem == 'CMP':
            res = self.A.get() - value
            if res < 0:
                self.SR.N = True
            else:
                self.SR.N = False
            if res == 0:
                self.SR.Z = True
            else:
                self.SR.Z = False
        elif mnem == 'CPX':
            res = self.X.get() - value
            if res < 0:
                self.SR.N = True
            else:
                self.SR.N = False
            if res == 0:
                self.SR.Z = True
            else:
                self.SR.Z = False
        elif mnem == 'CPY':
            res = self.Y.get() - value
            if res < 0:
                self.SR.N = True
            else:
                self.SR.N = False
            if res == 0:
                self.SR.Z = True
            else:
                self.SR.Z = False
        elif mnem == 'BEQ':
            if self.SR.Z:
                self.PC.set(address+1)
        elif mnem == 'INX':
            self.X.inc()
        elif mnem == 'DEX':
            self.X.dec()
        elif mnem == 'INY':
            self.Y.inc()
        elif mnem == 'DEY':
            self.Y.dec()
        elif mnem == 'JMP':
            self.PC.set(address)
        else:
            raise Exception('Instruction not implemented: {}'.format(mnem))
