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
        white_player = True #True if a human is playing white, False if it's an AI agent
        black_player = False #True if a human is playing white, False if it's an AI agent

        while True:
            game.show_background(screen) #Display the board
            game.show_last_move(screen) #Display the previous move
            game.show_possible_moves(screen) #Display possible moves of the piece being dragged
            game.show_pieces(screen) #Display pieces on the board            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            #Determine whether it's a human or an AI turn
            human_turn = (game.next_player == 'white' and white_player) or (game.next_player == 'black' and black_player)            
            ai_vs_ai = not white_player and not black_player
            
            for event in pygame.event.get():
                #Event handler
                
                #Close the window and end program when the red cross is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        board.undo_move()
                        game.next_player = 'black' if game.next_player == 'white' else 'white'
                        game.show_background(screen) #Display the board
                        game.show_last_move(screen) #Display the previous move
                        game.show_possible_moves(screen) #Display possible moves of the piece being dragged
                        game.show_pieces(screen) #Display pieces on the board
                    
                if human_turn: #Check if a human play this turn
                    if event.type == pygame.MOUSEBUTTONDOWN: #Check if the player press the mouse
                        dragger.update_mouse(event.pos) #Update the mouse position on the board
                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE
                            
                        if board.tiles[clicked_row][clicked_col].has_piece(): #Check if the tile contains a piece
                            piece = board.tiles[clicked_row][clicked_col].piece #Get the piece on the tile clicked
                            if piece.color == game.next_player: #Check if the piece color can move this turn (if it's white or black turn)
                                board.possible_moves(piece, clicked_row, clicked_col, checked=False) #Get all the piece possible moves
                                dragger.save_initial(event.pos) #Save the piece initial position
                                dragger.drag_piece(piece) #Set the piece in "dragging" mode
                                game.show_background(screen) #Display the board
                                game.show_possible_moves(screen) #Display the possible moves of the piece being dragged
                                game.show_pieces(screen) #Display pieces
                        
                    elif event.type == pygame.MOUSEMOTION: #Check if the mouse is moving
                        if dragger.dragging: #Check if a piece is being dragged
                            dragger.update_mouse(event.pos) #Update mouse position on the board
                            game.show_background(screen) #Display board
                            game.show_last_move(screen) #Display the previous move
                            game.show_possible_moves(screen) #Display the possible moves of the piece being dragged
                            game.show_pieces(screen) #Display pieces except for the one being dragged
                            dragger.update_blit(screen) #Display and keep updating the piece being dragged
                            
                    elif event.type == pygame.MOUSEBUTTONUP: #Check if the player release the mouse button
                        if dragger.dragging: #Check if a piece is being dragged
                            dragger.update_mouse(event.pos)
                            
                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE
                            
                            initial_tile = Tile(dragger.initial_row, dragger.initial_col)
                            moved_piece = board.tiles[dragger.initial_row][dragger.initial_col].piece
                            final_tile = Tile(released_row, released_col)
                            captured_piece = board.tiles[released_row][released_col].piece
                            move = Move(initial_tile, final_tile, moved_piece, captured_piece) #Create the new move
                            
                            if board.valid_move(dragger.piece, move): #Check if the move is valid
                                board.move(dragger.piece, move) #Move the piece in the board
                                board.set_en_passant(dragger.piece) #Enable the en passant attribut
                                game.show_last_move(screen) #Display the last move
                                game.show_background(screen) #Display the board
                                game.show_pieces(screen) #Display the pieces
                                game.next_turn() #Switch the active player turn
                                
                        dragger.undrag_piece() #Disable the piece "dragging" mode
                    
                    elif event.type == pygame.KEYDOWN: #Check if a keyboard key is pressed
                    
                        if event.key == pygame.K_r: #Check if the key pressed is the "r" key
                            game.reset() #Reset the game by creating a entire new board
                            #Reinitialize attributes
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                
                elif ai_vs_ai:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            ai_move = board.ai_best_negamax_move(game) #Get the best move in the current state of the game
                            piece = board.tiles[ai_move.initial_tile.col][ai_move.initial_tile.row].piece #Get the piece related to the move
                            board.move(piece, ai_move) #Move the piece on the board
                            board.set_en_passant(piece) #Enable the "en passant" attribut
                            game.show_last_move(screen) #Display the last move
                            game.show_background(screen) #Display the board
                            game.show_pieces(screen) #Display the pieces
                            game.next_turn() #Set the next player to the opposite color : black if white and white if black
                                
                elif not human_turn: #If it's an AI turn
                    ai_move = board.ai_best_negamax_move(game) #Get the best move in the current state of the game
                    piece = board.tiles[ai_move.initial_tile.col][ai_move.initial_tile.row].piece #Get the piece related to the move
                    board.move(piece, ai_move) #Move the piece on the board
                    board.set_en_passant(piece) #Enable the "en passant" attribut
                    game.show_last_move(screen) #Display the last move
                    game.show_background(screen) #Display the board
                    game.show_pieces(screen) #Display the pieces
                    game.next_turn() #Set the next player to the opposite color : black if white and white if black
                
            pygame.display.update() #Update the game window display
main = Main()
main.mainloop()