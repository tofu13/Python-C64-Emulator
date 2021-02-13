import struct


class ProgramLoader(object):
    def __init__(self, memory):
        self.memory = memory
    
    def load_file(self, path):
        with open(path, "rb") as f:
            data = f.read()

        address = struct.unpack('H', data[:2])[0]
        
        for byte in data[2:]:
            self.memory[address] = struct.unpack('B', bytes([byte]))[0]
            address += 1
