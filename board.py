from constants import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import copy
import os


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for file in range(FILES)]
        self.last_move = None
        self._create_squares()
        self._set_initial_piece_state('white')
        self._set_initial_piece_state('black')

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.rank][final.file].isempty()

        # console board move update
        self.squares[initial.rank][initial.file].piece = None
        self.squares[final.rank][final.file].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.file - initial.file
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.rank][initial.file + diff].piece = None
                self.squares[final.rank][final.file].piece = piece
                if not testing:
                    sound = Sound(os.path.join(f'{SOUNDS_PATH}/capture.wav'))
                    sound.play()

            # pawn promotion
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.file - initial.file
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.rank == 0 or final.rank == 7:
            self.squares[final.rank][final.file].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.file - final.file) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for rank in range(RANKS):
            for file in range(FILES):
                if isinstance(self.squares[rank][file].piece, Pawn):
                    self.squares[rank][file].piece.en_passant = False

        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for rank in range(RANKS):
            for file in range(FILES):
                if temp_board.squares[rank][file].has_enemy_piece(piece.color):
                    p = temp_board.squares[rank][file].piece
                    temp_board.calc_moves(p, rank, file, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def calc_moves(self, piece, rank, file, bool=True):
        """
        Calculate all the possible (valid) moves of a specific piece on a specific position
        """

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = rank + piece.dir
            end = rank + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][file].isempty():
                        # create initial and final move squares
                        initial = Square(rank, file)
                        final = Square(possible_move_row, file)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = rank + piece.dir
            possible_move_cols = [file - 1, file + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(rank, file)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en passant
            if Square.in_range(file - 1) and rank == r:
                if self.squares[rank][file - 1].has_enemy_piece(piece.color):
                    p = self.squares[rank][file - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(rank, file)
                            final = Square(fr, file - 1, p)
                            # create a new move
                            move = Move(initial, final)

                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

            # right en passant
            if Square.in_range(file + 1) and rank == r:
                if self.squares[rank][file + 1].has_enemy_piece(piece.color):
                    p = self.squares[rank][file + 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(rank, file)
                            final = Square(fr, file + 1, p)
                            # create a new move
                            move = Move(initial, final)

                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (rank - 2, file + 1),
                (rank - 1, file + 2),
                (rank + 1, file + 2),
                (rank + 2, file + 1),
                (rank + 2, file - 1),
                (rank + 1, file - 2),
                (rank - 1, file - 2),
                (rank - 2, file - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(rank, file)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = rank + row_incr
                possible_move_col = file + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(rank, file)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (rank - 1, file + 0),  # up
                (rank - 1, file + 1),  # up-right
                (rank + 0, file + 1),  # right
                (rank + 1, file + 1),  # down-right
                (rank + 1, file + 0),  # down
                (rank + 1, file - 1),  # down-left
                (rank + 0, file - 1),  # left
                (rank - 1, file - 1),  # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(rank, file)
                        final = Square(possible_move_row, possible_move_col)  # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[rank][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[rank][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(rank, 0)
                                final = Square(rank, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(rank, file)
                                final = Square(rank, 2)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[rank][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[rank][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(rank, 7)
                                final = Square(rank, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(rank, file)
                                final = Square(rank, 6)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1),  # left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create_squares(self):
        """
        Creates the squares within the board.
        """
        for rank in range(RANKS):
            for file in range(FILES):
                self.squares[rank][file] = Square(rank, file)

    def _set_initial_piece_state(self, color):
        """
        Internal function to set the initial states of the pieces on the board.

        :param color: the colour of the pieces to add
        """
        pawn_rank, back_rank = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for file in range(FILES):
            self.squares[pawn_rank][file] = Square(pawn_rank, file, Pawn(color))

        # knights
        self.squares[back_rank][1] = Square(back_rank, 1, Knight(color))
        self.squares[back_rank][6] = Square(back_rank, 6, Knight(color))

        # bishops
        self.squares[back_rank][2] = Square(back_rank, 2, Bishop(color))
        self.squares[back_rank][5] = Square(back_rank, 5, Bishop(color))

        # rooks
        self.squares[back_rank][0] = Square(back_rank, 0, Rook(color))
        self.squares[back_rank][7] = Square(back_rank, 7, Rook(color))

        # queen
        self.squares[back_rank][3] = Square(back_rank, 3, Queen(color))

        # king
        self.squares[back_rank][4] = Square(back_rank, 4, King(color))
