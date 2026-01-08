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
        self.grid = [[4, 2, 3, 5, 6, 3, 2, 4],
                     [1, 1, 1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [7, 7, 7, 7, 7, 7, 7, 7],
                     [10, 8, 9, 11, 12, 9, 8, 10]]
        self.grid_mono = [[1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [2, 2, 2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2, 2, 2]]
        self.all_possible_mono = []

        zeros = []
        for i in range(64):
            val = ""
            for j in range(64-i):
                val = val + "0"
            zeros.append(val)

        print(zeros)

        possible = []
        nof = 3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3
        for i in range(nof-1000000000, nof):
            board = self.number_to_base(i, 3)
            if board.count("1") < 1 or board.count("2") < 1 or board.count("1") > 16 or board.count("2") > 16:
                print(board + " no")
                if board > 2222222222222222200000000000000000000000000000000000000000000000:
                    break
                else:
                    continue
            else:
                lenboard = len(board)
                if lenboard < 64:
                    possible.append(zeros[lenboard] + board + "\n")
                else:
                    possible.append(board + "\n")
                print(zeros[lenboard] + board)
        print("FINAL LENGTH: " + str(len(possible)))


        print(possible)

        with open("possible_boards.txt", "w") as f:
            for board in possible:
                print(board) 
                f.write(board)

        print(possible)

        def calculate_bishop(self, pos, board, mono): # mono needs to be a string
            return
            self.ap_bishop = []
            for i in range():
                break
                # break #petit easter egg (kaan)
            self.all_possible_mono[mono] = 0




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
        pieces = ["pawn w", "knight w", "bishop w", "rook w", "queen w", "king w", "pawn b", "knight b", "bishop b", "rook b", "queen b", "king b"]
        for piece in pieces:
            self.piece_dimensions.append(self.current_sprites[piece].get_size())

        self.player = 1 # 1 is white, 2 is black
        self.selected_piece = 0

    def number_to_base(self, n, b): 
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(str(n % b))
            n //= b
        return "".join(digits[::-1])
        # for i in range(len(digits)): 
        #     digits[i] = str(digits[i])
        # print("".join(digits))
        # print("digits: ")
        # print(digits)
        # return "".join(digits)
        # return digits[::-1]


    def resize_sprite(self): # resizes skin sprite (pieces) but can me modified to also resize ui or other things
        to_resize = ["pawn w", "pawn b", "knight w", "knight b", "bishop w", "bishop b", "rook w", "rook b", "queen w", "queen b", "king w", "king b"]
        for item in to_resize:
            self.current_sprites[item] = pygame.transform.scale_by(self.sprites["./src/skins/" + self.piece_skin][item + ".svg"], 0.2)
        to_resize = ["cell 1", "cell 2", "cell 3", "cell 4", "cell 5", "cell 6", "cell 7", "cell 8", "cell 9", "cell 17", "cell 25", "cell 33", "cell 41", "cell 49", "cell 57", "cell b", "cell w"]
        for item in to_resize:
            self.current_sprites[item] = pygame.transform.scale_by(self.sprites["./src/skins/" + self.board_skin][item + ".svg"], 0.2)

        # print ("current sprites: ") 
        # print (self.current_sprites)

    def render_board(self):
        pieces = ["pawn w", "knight w", "bishop w", "rook w", "queen w", "king w", "pawn b", "knight b", "bishop b", "rook b", "queen b", "king b"]
        tile_size = 70
        mousex, mousey = pygame.mouse.get_pos()

        for x_ in range(8):

            if self.player == 1:
                x = 7-x_
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

                if pygame.mouse.get_just_pressed()[0] == 1 and self.grid[y][x] != 0:
                    if mousex > x_*tile_size and mousex < (x_+1)*tile_size:
                        if mousey > y_*tile_size and mousey > (y+1)*tile_size:
                            self.selected_piece = (x, y)
                                    
                if self.grid[y][x] != 0 and self.selected_piece != (x, y):
                    piece = pieces[self.grid[y][x]-1]
                    x_pos = x_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][0])/2
                    y_pos = y_*tile_size+(tile_size-self.piece_dimensions[pieces.index(piece)][1])/2
                    self.screen.blit(self.current_sprites[piece], (x_pos, y_pos))

                # print(x, y)
        
        if self.selected_piece != 0:
            piece = pieces[self.grid[self.selected_piece[1]][self.selected_piece[0]]-1]
            x_pos = mousex-self.piece_dimensions[pieces.index(piece)][0]/2
            y_pos = mousey-self.piece_dimensions[pieces.index(piece)][1]/2
            self.screen.blit(self.current_sprites[piece], (x_pos, y_pos))


            

    def game_run(self):
        while self.run:
            self.clock.tick(self.fps_cap)
            self.render_board()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

Game().game_run()
