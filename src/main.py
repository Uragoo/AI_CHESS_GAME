import pygame
import sys
from const import *
from game import Game
from tile import Tile
from move import Move

class Main:

    def __init__(self):
        #Display the game window
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AI CHESS GAME')
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_background(screen) #Display the board
            game.show_last_move(screen) #Display the previous move
            game.show_possible_moves(screen) #Display possible moves of the piece being dragged
            game.show_pieces(screen) #Display pieces on the board            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                """
                Dragger event
                """
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    #checking if the tile contains a piece
                    if board.tiles[clicked_row][clicked_col].has_piece():
                        piece = board.tiles[clicked_row][clicked_col].piece #Get the piece on the tile clicked
                        if piece.color == game.next_player: #Check if the piece color can move this turn (if it's white or black turn)
                            board.possible_moves(piece, clicked_row, clicked_col) #Get all the piece possible moves
                            dragger.save_initial(event.pos) #Save the piece initial position
                            dragger.drag_piece(piece) #Set the piece in "dragging" mode
                            game.show_background(screen) #Display the board
                            game.show_possible_moves(screen) #Display the possible moves of the piece being dragged
                            game.show_pieces(screen) #Display pieces
                    
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos) #Updating mouse position on the board
                        game.show_background(screen) #Display board
                        game.show_last_move(screen) #Display the previous move
                        game.show_possible_moves(screen) #Display the possible moves of the piece being dragged
                        game.show_pieces(screen) #Display pieces except for the one being dragged
                        dragger.update_blit(screen) #Display and keep updating the piece being dragged
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        initial_tile = Tile(dragger.initial_row, dragger.initial_col)
                        final_tile = Tile(released_row, released_col)
                        move = Move(initial_tile, final_tile)
                        
                        if board.valid_move(dragger.piece, move): #Check if the move is valid
                            board.move(dragger.piece, move) #Move the piece in the board
                            game.show_last_move(screen) #Display the last move
                            game.show_background(screen) #Display the board
                            game.show_pieces(screen) #Display the pieces
                            game.next_turn()
                            
                    dragger.undrag_piece() #Disable the piece "dragging" mode
                
                elif event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                #Close the window and end program when the red cross is pressed
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()
main = Main()
main.mainloop()