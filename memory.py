class Memory(object):

    def __init__(self):
        self.size = 65536
        self.memory = {}

    def write(self, address, value):
        if address < 0 or address > self.size:
            raise Exception("Address out of range: " + address)
        elif not isinstance(value, int):
            raise TypeError(f"Value must be int, not {type(value)}")
        elif value < 0 or value > 255:
            raise ValueError(f"Value {value} is outside bounds (0-255)")
        self.memory[address] = value
    
    def read(self, address):
        if address < 0 or address > self.size:
            raise ValueError(f"Address out of range: {address}")
        if not address in self.memory:
            return 0
        
        return self.memory[address]
