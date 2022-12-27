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
        game_over = False #True if the game is finished, else False

        while True:
            game.show_background(screen) #Display the board
            game.show_last_move(screen) #Display the previous move
            game.show_possible_moves(screen) #Display possible moves of the piece being dragged
            game.show_pieces(screen) #Display pieces on the board            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            #Determine whether it's a human or an AI turn
            human_turn = (game.next_player == 'white' and white_player) or (game.next_player == 'black' and black_player)
            
            if board.get_all_valid_moves(game) == None: #If a player has no valid moves, he loses the game (checkmate)
                    print("Game Over !")
                    print("white wins !") if game.next_player == 'black' else print("black wins !")
                    pygame.quit()
                    sys.exit()
            
            if human_turn: #Check if a human play this turn
                for event in pygame.event.get():
                    #Event handler
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
                            final_tile = Tile(released_row, released_col)
                            move = Move(initial_tile, final_tile) #Create the new move
                            
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
                    
                    #Close the window and end program when the red cross is pressed
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else: #If it's an AI turn
                if game.next_player == 'white':
                    maximizing = True #We want to maximize the white player's score
                else:
                    maximizing = False #We want to minimize the black player's score
                ai_move = board.ai_best_move(5, game, maximizing) #Get the best move in the current state of the game
                print("AI move")
                print((ai_move.initial_tile.row, ai_move.initial_tile.col), (ai_move.final_tile.row, ai_move.final_tile.col))
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