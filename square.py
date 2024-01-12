from constants import ALPHABETIC_FILE_MAP


class Square:

    def __init__(self, rank, file, piece=None):
        self.rank = rank
        self.file = file
        self.piece = piece

    def __eq__(self, other):
        return self.rank == other.rank and self.file == other.file

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    @staticmethod
    def get_alphabetic_file_name(file):
        return ALPHABETIC_FILE_MAP[file]
