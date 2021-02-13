class Memory(bytearray):

    def __setitem__(self, address, value):
        if address < 0 or address > len(self):
            raise ValueError(f"Address {address} out of range 0-{len(self)}")
        elif not isinstance(value, int):
            raise TypeError(f"Value must be int, not {type(value)}")
        elif value < 0 or value > 255:
            raise ValueError(f"Value {value} is outside bounds (0-255)")
        super().__setitem__(address, value)

    def __getitem__(self, address):
        # Useless: already checked by native super method
        if address < 0 or address > len(self):
            raise ValueError(f"Address {address} out of range 0-{len(self)}")
        return super().__getitem__(address)
