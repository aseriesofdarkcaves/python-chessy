class Move:
    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.file}, {self.initial.rank})'
        s += f' -> ({self.final.file}, {self.final.rank})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
