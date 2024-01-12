import pygame

from constants import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # blit methods
    def show_bg(self, surface):
        theme = self.config.theme

        for rank in range(RANKS):
            for file in range(FILES):
                # color
                color = theme.bg.light if (rank + file) % 2 == 0 else theme.bg.dark
                # rect
                rect = (file * SQSIZE, rank * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # rank coordinates
                if file == 0:
                    # color
                    color = theme.bg.dark if rank % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(RANKS - rank), 1, color)
                    lbl_pos = (5, 5 + rank * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # file coordinates
                if rank == 7:
                    # color
                    color = theme.bg.dark if (rank + file) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphabetic_file_name(file), 1, color)
                    lbl_pos = (file * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for rank in range(RANKS):
            for file in range(FILES):
                # piece ?
                if self.board.squares[rank][file].has_piece():
                    piece = self.board.squares[rank][file].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = file * SQSIZE + SQSIZE // 2, rank * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.rank + move.final.file) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.file * SQSIZE, move.final.rank * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.rank + pos.file) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.file * SQSIZE, pos.rank * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.file * SQSIZE, self.hovered_sqr.rank * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, rank, file):
        self.hovered_sqr = self.board.squares[rank][file]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
