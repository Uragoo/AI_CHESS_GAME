import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from tile import Tile
import sys

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.hovered_tiles = None
        self.config = Config()

    def show_background(self, surface):
        """
        Display the board
        """
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    #color = (234, 235, 200) # light green
                    color = (240,248,255) # aliceblue
                else:
                    #color = (119, 154, 88) # dark green
                    color = (65,105,225) # royal blue
                    
                tile = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE) # Create the tile

                pygame.draw.rect(surface, color, tile) # Add the tile to the scene
                
                ##Display row numbers
                if col == 0: #We will display the row numbers on the first column
                    #Set the color
                    if row % 2 == 0:
                        color = (65, 105, 225)
                    else:
                        color = (240, 248, 255)
                    label = self.config.font.render(str(ROWS - row), 1, color) #Create the text that will be displayed
                    label_position = (5, 5 + row * SQSIZE) #Set the position of the text
                    surface.blit(label, label_position) #Merge the label within the board
                
                ##Display the column letters
                if row == 7: #We will display the column letters on the bottom row
                    #Set color
                    if (row + col) % 2 == 0:
                        color = (65, 105, 225)
                    else:
                        color = (240, 248, 255)
                    label = self.config.font.render(Tile.get_alphacol(col), 1, color) #Create the text that will be displayed
                    label_position = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20) #Set the position of the label
                    surface.blit(label, label_position) #Merge the label within the board  
    
    def show_pieces(self, surface):
        """
        Display the pieces
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.tiles[row][col].has_piece():
                    piece = self.board.tiles[row][col].piece
                    
                    if piece is not self.dragger.piece: 
                        #Display pieces on the board if they're not being dragged
                        piece.set_texture(size=80) #Set size to 80 pixels
                        image = pygame.image.load(piece.texture) #Load image
                        image_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2 #Center image on x and y axis
                        piece.texture_rect = image.get_rect(center=image_center) #Get the image borders
                        surface.blit(image, piece.texture_rect) #Merge the image inside the tile
                        
    def show_possible_moves(self, surface):
        """
        Display all possible moves of the piece being dragged
        """
        if self.dragger.dragging: #Check if the piece is being dragged
            piece = self.dragger.piece #Get the piece being dragged
            for move in piece.moves:
                #Set color
                if (move.final_tile.row + move.final_tile.col) % 2 == 0:
                    color = (252, 170, 0)
                else:
                    color = (252, 125, 0)
                tile = (move.final_tile.row * SQSIZE, move.final_tile.col * SQSIZE, SQSIZE, SQSIZE) #Create new tile
                pygame.draw.rect(surface, color, tile) #Merge the tile and the color within the board
                
    def show_last_move(self, surface):
        """
        Display the previous move
        """
        if self.board.last_move: #Check if there is a last move
            #Get initial and final tile of the move
            initial_tile = self.board.last_move.initial_tile
            final_tile = self.board.last_move.final_tile
            
            for position in [initial_tile, final_tile]:
                #Set color
                if (position.row + position.col) % 2 == 0:
                    color = (244, 247, 116)
                else:
                    color = (172, 195, 51)
                tile = (position.row * SQSIZE, position.col * SQSIZE, SQSIZE, SQSIZE) #Create new tile
                pygame.draw.rect(surface, color, tile) #Merge the tile and the color within the board
                
    def next_turn(self):
        """
        Switch player turn
        """
        if self.next_player == 'white':
            self.next_player = 'black'
        else:
            self.next_player = 'white'
            
    def reset(self):
        self.__init__()
        
    def game_over(self):
        if self.board.get_all_valid_moves(self) == None: #If a player has no valid moves, he loses the game (checkmate)
            print("Game Over !")
            print("white wins !") if self.next_player == 'black' else print("black wins !")
            pygame.quit()
            sys.exit()