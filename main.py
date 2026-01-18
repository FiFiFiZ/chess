import pygame
from math import*
import sys
sys.path.append("./bin")

from assets import Assets #type: ignore

class Game:
    def __init__(self):
        pygame.init()


        self.run = True
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h

        self.SCREEN_WIDTH = 70*8
        self.SCREEN_HEIGHT = 70*8

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill((20,50,150))
        self.fps_cap = 60
        self.mouse = [0, 0, 0]

        self.grid = [[4, 2, 3, 6, 5, 3, 2, 4],
                     [1, 1, 1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [11, 9, 10, 12, 13, 10, 9, 11]]
        self.grid_mono = [[1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [2, 2, 2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2, 2, 2]]
        self.legal_moves = {}
        self.turn = 1

        # tableau with all the legal moves based on the position on the board to make lookup faster?

        # make a list of all possible board states (considering 3 possible values: 0, 1, 2), remove all the impossible board states and from there you can calculate each piece's legal moves in any board state (when reducing down the board state to 3 values (empty, player 1, player 2))
        # and don't make it a list, make it a string because looking up characters in a string is faster

        self.piece_skin = "Standard" # currently selected piece
        self.board_skin = "Salmon" # currently selected board

        self.assets = Assets()
        self.sprites = self.assets.directories
        self.current_sprites = {}
        self.resize_sprite()

        self.piece_dimensions = []
        pieces = ["pawn w", "knight w", "bishop w", "rook w", "queen w", "king w", "", "pawn b", "knight b", "bishop b", "rook b", "queen b", "king b", "legal"]
        for piece in pieces:
            if piece == "":
                self.piece_dimensions.append("")
            else:
                self.piece_dimensions.append(self.current_sprites[piece].get_size())

        self.player = 1 # 1 is white, 2 is black
        self.selected_piece = 0


    def calculate_legal_moves(self, board, turn):
        for file in range(0,8):
            rank = 0
            for cell in board[file]:
                if cell:
                    rank += 1
                    piece = cell%7
                    if piece == 1:
                        self.legal_moves[(rank, file)] = self.pawn_legal(rank, file, board, turn)
                    elif piece == 3:
                        self.legal_moves[(rank, file)] = self.bishop_legal(rank, file, board, turn)

    def pawn_legal(self, rank, file, board, turn):
        if turn == 1:
            if file == 1:
                return [(rank, 2), (rank, 3)]
            else:
                return [(rank, file+1)]
        else:
            if file == 6:
                return [(rank, 5), (rank, 4)]
            else:
                return [(rank, file-1)]

    def bishop_legal(self, rank, file, board, turn):
        self.l_bishop = []
        self.bishop_legal_loop(1, 1, rank, file, board, turn)
        self.bishop_legal_loop(1, -1, rank, file, board, turn)
        self.bishop_legal_loop(-1, 1, rank, file, board, turn)
        self.bishop_legal_loop(-1, -1, rank, file, board, turn)
        return self.l_bishop
                
    def bishop_legal_loop(self, x, y, rank, file, board, turn):
        r = rank
        f = file
        while True:
            r += x # rank
            f += y # file
            if r > 7 or r < 0 or f > 7 or f < 0:
                break
            c = board[r][f] # cell
            if c:
                if turn == 1:
                    if c < 8:
                        break
                    else:
                        self.l_bishop.append((r, f))
                        break
                else:
                    if c > 7:
                        break
                    else:
                        self.l_bishop.append((r, f))
                        break
            else:
                self.l_bishop.append((r, f))

        

    def resize_sprite(self): # resizes skin sprite (pieces) but can me modified to also resize ui or other things
        to_resize = ["pawn w", "pawn b", "knight w", "knight b", "bishop w", "bishop b", "rook w", "rook b", "queen w", "queen b", "king w", "king b", "legal"]
        for item in to_resize:
            self.current_sprites[item] = pygame.transform.scale_by(self.sprites["./src/skins/" + self.piece_skin][item + ".svg"], 0.2)
        to_resize = ["cell 1", "cell 2", "cell 3", "cell 4", "cell 5", "cell 6", "cell 7", "cell 8", "cell 9", "cell 17", "cell 25", "cell 33", "cell 41", "cell 49", "cell 57", "cell b", "cell w"]
        for item in to_resize:
            self.current_sprites[item] = pygame.transform.scale_by(self.sprites["./src/skins/" + self.board_skin][item + ".svg"], 0.2)

        # print ("current sprites: ") 
        # print (self.current_sprites)

    def render_board(self):
        pieces = ["pawn w", "knight w", "bishop w", "rook w", "queen w", "king w", "", "pawn b", "knight b", "bishop b", "rook b", "queen b", "king b", "legal"]
        tile_size = 70
        mousex, mousey = pygame.mouse.get_pos()

        for x_ in range(8):

            if self.player == 1:
                x = x_
            else:
                x = x_

            for y_ in range(8):

                if self.player == 1:
                    y = 7-y_
                else:
                    y = y_
                    
                # if y == 0 or x == 0:
                #     self.screen.blit(self.current_sprites["cell " + str(x+y*8+1)], (x_*tile_size,y_*tile_size))
                if (x_+y_*8+y_)%2 == self.player-1:
                    self.screen.blit(self.current_sprites["cell w"], (x_*tile_size,y_*tile_size))
                else:
                    self.screen.blit(self.current_sprites["cell b"], (x_*tile_size, y_*tile_size))

                if self.mouse[0] == 1 :
                    if self.grid[y][x] != 0: # select piece
                        if self.selected_piece == (x, y):
                            self.selected_piece = 0
                            self.timer_select_piece = 1
                        elif mousex > x_*tile_size and mousex < (x_+1)*tile_size:
                            if mousey > y_*tile_size and mousey > (y+1)*tile_size:
                                self.selected_piece = (x, y)
                                self.timer_select_piece = 1
                    elif self.selected_piece != 0 and self.timer_select_piece == 0: # if click while piece is selected
                        print("selected piece: " + str(self.selected_piece)) 
                        if (x, y) in self.legal_moves[self.selected_piece]: # make a legal move if possible
                            self.grid[y][x] = self.selected_piece
                            self.grid[self.selected_piece[1]][self.selected_piece[0]] = 0
                            self.selected_piece = 0
                        else: # unselect
                            self.selected_piece = 0

                if self.selected_piece != (x, y):
                    if self.grid[y][x] != 0: # draw non-selected piece on the board
                        piece = pieces[self.grid[y][x]-1]
                        x_pos = x_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][0])/2
                        y_pos = y_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][1])/2
                        self.screen.blit(self.current_sprites[piece], (x_pos, y_pos))

                if self.selected_piece != 0: 
                    if (x, y) in self.legal_moves[self.selected_piece]: # draw legal move indicator on cell
                        x_pos = x_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][0])/2
                        y_pos = y_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][1])/2

                        self.screen.blit(self.current_sprites[pieces[13]], (x_pos, y_pos))

                # print(x, y)
        
        if self.selected_piece != 0:
            piece = pieces[self.grid[self.selected_piece[1]][self.selected_piece[0]]-1]
            x_pos = mousex-self.piece_dimensions[pieces.index(piece)][0]/2
            y_pos = mousey-self.piece_dimensions[pieces.index(piece)][1]/2
            self.screen.blit(self.current_sprites[piece], (x_pos, y_pos))

            

    def game_run(self):
        while self.run:
            self.clock.tick(self.fps_cap)
            m = pygame.mouse.get_pressed(num_buttons=3)
            for i in range(0, 3):
                if m[i]:
                    self.mouse[i] += m[i]
                else:
                    self.mouse[i] = 0

            if self.legal_moves == {}:
                self.calculate_legal_moves(self.grid, self.turn)
            # print("legal moves: " + str(self.legal_moves))
            # print("selected piece: " + str(self.selected_piece)) 
            self.render_board()
            self.timer_select_piece = 0
            print(self.mouse)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

Game().game_run()
