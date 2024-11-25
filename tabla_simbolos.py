class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, name, type):
        if name in self.symbols:
            raise ValueError(f"Error: La variable '{name}' ya fue declarada.")
        self.symbols[name] = type

    def exists(self, name):
        return name in self.symbols

    def __str__(self):
        return str(self.symbols)
