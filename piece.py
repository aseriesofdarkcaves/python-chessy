import os

from constants import *


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        """
        :param name: the name of the piece
        :param color: the colour of the piece
        :param value: the value of the piece
        :param texture: the texture to use when representing the piece
        :param texture_rect: TODO: figure this out and document it
        """
        self.name = name
        self.color = color
        # ternary assignment statement in python
        # white pieces have positive values, black have negative values
        value_sign = 1 if color == 'white' else -1
        # this normalises piece values so that they're always positive
        self.value = value * value_sign
        # a list of moves made by the piece so far
        self.moves = []
        # boolean to track whether a piece has been moved already or not
        self.moved = False
        # the texture to use when representing the piece
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        """
        Sets the texture to use when representing the piece.

        :param size: the square size of the texture
        :return: the path to the texture
        """
        self.texture = os.path.join(f'{TEXTURES_PATH}/{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color):
        # ternary assignment statement in python
        # negative values indicate an up direction in pygame, whilst positive indicates down direction
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)
