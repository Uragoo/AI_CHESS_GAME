from const import *
from tile import Tile
from piece import *
from move import Move
import copy
import random

class Board:

    def __init__(self):
        self.tiles = [[0,0,0,0,0,0,0,0] for col in range(COLS)] #Initializing Tiles
        self.last_move = None
        self._create()
        self._add_pieces('black')
        self._add_pieces('white')

    def _create(self):
        """
        Create the board
        """
        #Creating all tiles
        for row in range(ROWS):
            for col in range(COLS):
                self.tiles[row][col] = Tile(row, col)

    def _add_pieces(self, color):
        """
        Add pieces for the initial board setup
        """
        row_pawn, row_figure = (1, 0) if color == 'black' else (6, 7)

        #Adding pawns
        for col in range(COLS):
            self.tiles[row_pawn][col] = Tile(row_pawn, col, Pawn(color))
        
        #Adding knights
        self.tiles[row_figure][1] = Tile(row_figure, 1, Knight(color))
        self.tiles[row_figure][6] = Tile(row_figure, 6, Knight(color))

        #Adding bishops
        self.tiles[row_figure][2] = Tile(row_figure, 2, Bishop(color))
        self.tiles[row_figure][5] = Tile(row_figure, 5, Bishop(color))

        #Adding rooks
        self.tiles[row_figure][0] = Tile(row_figure, 0, Rook(color))
        self.tiles[row_figure][7] = Tile(row_figure, 7, Rook(color))

        #Adding the queen
        self.tiles[row_figure][3] = Tile(row_figure, 3, Queen(color))

        #Adding the king
        self.tiles[row_figure][4] = Tile(row_figure, 4, King(color))
        
    def possible_moves(self, piece, row, col, checked=False):
        """
        Determine all valid moves of the piece
        """
        def pawn_moves():
            """
            All possible moves for the pawn pieces
            """
            if piece.moved:
                steps = 1
            else:
                steps = 2
            
            ##Vertical moves
            start = row + piece.direction #Current position with pawn direction
            end = row + (piece.direction * (1 + steps)) #Maximum position (2 forward if it hasn't move yet else 1)
            for move_row in range(start, end, piece.direction):
                if Tile.in_range(move_row): #Check if the move is inside the board
                    if self.tiles[move_row][col].is_empty(): #Check if the tile is empty
                        initial_tile = Tile(row, col)
                        final_tile = Tile(move_row, col)
                        move = Move(initial_tile, final_tile) #Create the new possible move
                        
                        if not checked: #Check if the move has already been checked
                            if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                piece.add_move(move) #Add it to the list
                        else:
                                piece.add_move(move) #Add it to the list    
                    else:
                        #Pawn is blocked
                        break #prevent the pawn to move 2 tiles forward even if an other piece is in front of it
                else:
                    break
            
            ##Diagonal moves
            move_row = row + piece.direction
            move_cols = [
                col - 1,
                col + 1
            ]
            
            for move_col in move_cols:
                if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                    if self.tiles[move_row][move_col].has_hostile_piece(piece.color): #Check if the tile contains an enemy
                        initial_tile = Tile(row, col)
                        final_piece = self.tiles[move_row][move_col].piece
                        final_tile = Tile(move_row, move_col, final_piece)
                        move = Move(initial_tile, final_tile) #Create the new possible move
                        
                        if not checked: #Check if the move has already been checked
                            if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                piece.add_move(move) #Add it to the list
                        else:
                                piece.add_move(move) #Add it to the list  
                                
            ##En passant moves
            if piece.color == 'white':
                initial_pawn_row = 3
                final_pawn_row = 2
            else:
                initial_pawn_row = 4
                final_pawn_row = 5
                
            #Left en passant
            if Tile.in_range(col - 1) and row == initial_pawn_row: #Check if the left tile of the pawn is inside the board and if the pawn is in the fourth row
                if self.tiles[row][col - 1].has_hostile_piece(piece.color): #Check if the pawn has an oponent piece at his left
                    enemy = self.tiles[row][col - 1].piece #Get the enemy piece
                    if isinstance(enemy, Pawn): #Check if the enemy is a pawn
                        if enemy.en_passant: #Check if the enemy just moved 2 tiles
                            initial_tile = Tile(row, col) #Get initial tile
                            final_tile = Tile(final_pawn_row, col - 1, enemy) #Get final tile
                            move = Move(initial_tile, final_tile) #Create the new move
                            
                            if not checked: #Check if the move has already been checked
                                if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                    piece.add_move(move) #Add the pawn move to its list
                            else:
                                piece.add_move(move) #Add the pawn move to its list
                                
            #Right en passant
            if Tile.in_range(col + 1) and row == initial_pawn_row: #Check if the left tile of the pawn is inside the board and if the pawn is in the fourth row
                if self.tiles[row][col + 1].has_hostile_piece(piece.color): #Check if the pawn has an oponent piece at his left
                    enemy = self.tiles[row][col + 1].piece #Get the enemy piece
                    if isinstance(enemy, Pawn): #Check if the enemy is a pawn
                        if enemy.en_passant: #Check if the enemy just moved 2 tiles
                            initial_tile = Tile(row, col) #Get initial tile
                            final_tile = Tile(final_pawn_row, col + 1, enemy) #Get final tile
                            move = Move(initial_tile, final_tile) #Create the new move
                            
                            if not checked: #Check if the move has already been checked
                                if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                    piece.add_move(move) #Add the pawn move to its list
                            else:
                                piece.add_move(move) #Add the pawn move to its list
        
        def knight_moves():
            """
            All possible moves for the knight pieces
            """
            moves = [
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row - 1, col + 2),
            ]
            
            #for each potential move, check if it's inside the board and if a move is possible (empty tile or with an enemy within it)
            for move in moves:
                move_row, move_col = move
                if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                    if self.tiles[move_row][move_col].is_empty_or_hostile(piece.color): #Check if the tile is empty or contains an enemy piece
                        initial_tile = Tile(row, col)
                        final_piece = self.tiles[move_row][move_col].piece
                        final_tile = Tile(move_row, move_col, final_piece)
                        move = Move(initial_tile, final_tile) #Create the new possible move
                        if not checked: #Check if the move has already been checked
                            if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                piece.add_move(move) #Add it to the list
                            else:
                                break #If moving the knight lead to a check situation, it will be the case for all its possible moves, so we break here
                        else:
                                piece.add_move(move) #Add it to the list            
        
            #Defining all bishop moves
            moves = [
                (row + 1, col + 1),
                (row + 2, col + 2),
                (row + 3, col + 3),
                (row + 4, col + 4),
                (row + 5, col + 5),
                (row + 6, col + 6),
                (row + 7, col + 7),
                (row - 1, col - 1),
                (row - 2, col - 2),
                (row - 3, col - 3),
                (row - 4, col - 4),
                (row - 5, col - 5),
                (row - 6, col - 6),
                (row - 7, col - 7),
                (row + 1, col - 1),
                (row + 2, col - 2),
                (row + 3, col - 3),
                (row + 4, col - 4),
                (row + 5, col - 5),
                (row + 6, col - 6),
                (row + 7, col - 7),
                (row - 1, col + 1),
                (row - 2, col + 2),
                (row - 3, col + 3),
                (row - 4, col + 4),
                (row - 5, col + 5),
                (row - 6, col + 6),
                (row - 7, col + 7),
            ]
        
        def line_moves(increments):
            """
            All possible straight line moves that we'll use for the bishop, the rook and the queen
            """
            for increment in increments:
                row_inc, col_inc = increment
                move_row = row + row_inc
                move_col = col + col_inc
                
                while True:
                    if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                        initial_tile = Tile(row, col)
                        final_piece = self.tiles[move_row][move_col].piece
                        final_tile = Tile(move_row, move_col, final_piece)
                        move = Move(initial_tile, final_tile) #Create new possible move
                        
                        if self.tiles[move_row][move_col].is_empty():
                            if not checked: #Check if the move has already been checked
                                if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                    piece.add_move(move) #Add it to the list
                            else:
                                piece.add_move(move) #Add it to the list
                                                           
                        elif self.tiles[move_row][move_col].has_hostile_piece(piece.color):
                            if not checked: #Check if the move has already been checked
                                if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                    piece.add_move(move) #Add it to the list
                            else:
                                    piece.add_move(move) #Add it to the list    
                            break #Prevent to continue looping after reaching an enemy
                            
                        elif self.tiles[move_row][move_col].has_friendly_piece(piece.color):
                            break #Prevent to continue looping behind an ally
                        
                    else:
                        break
                    
                    move_row = move_row + row_inc
                    move_col = move_col + col_inc
        
        def king_moves():
            """
            All king pieces possibe moves
            """
            adjacent_moves = [
                (row - 1, col), #Up move
                (row - 1, col + 1), #Up right move
                (row, col + 1), #Right move
                (row + 1, col + 1), #Down right move
                (row + 1, col), #Down move
                (row + 1, col - 1), #Down left move
                (row, col - 1), #Left move
                (row - 1, col - 1), #Up left move
            ]
            
            for adjacent_move in adjacent_moves:
                move_row, move_col = adjacent_move
                
                if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                    if self.tiles[move_row][move_col].is_empty_or_hostile(piece.color): #Check if the tile is empty or contains an enemy piece
                        initial_tile = Tile(row, col)
                        final_tile = Tile(move_row, move_col)
                        move = Move(initial_tile, final_tile) #Create de new possible move
                        
                        if not checked: #Check if the move has already been checked
                            if not self.in_check(piece, move): #Check if the move does not lead to a check situation
                                piece.add_move(move) #Add it to the list
                            else:
                                break
                        else:
                                piece.add_move(move) #Add it to the list       
                                                     
            if not piece.moved: #Checking if the king has not move yet
                ##Queen Castling
                left_rook = self.tiles[row][0].piece #Get the piece on the far left of the king
                if isinstance(left_rook, Rook): #Check if this piece is a rook
                    if not left_rook.moved: #Check if the rook has not move yet
                        for column in range(1,4): #Loop the tiles between the rook and the king
                            if self.tiles[row][column].has_piece(): #Check if there is a piece on the tile
                                break #break because there is an obstacle between the rook and the king
                            
                            elif column == 3:
                                piece.left_rook = left_rook #Add a reference to the rook
                                
                                ###Rook move
                                initial_tile = Tile(row, 0) #Set the rook initial tile
                                final_tile = Tile(row, 3) #Set the rook destination tile
                                rook_move = Move(initial_tile, final_tile) #Create the new move
                                
                                ###King move
                                initial_tile = Tile(row, col) #Set the king initial tile
                                final_tile = Tile(row, 2) #Set the king destination tile
                                king_move = Move(initial_tile, final_tile) #Create the new move
                                
                                if not checked: #Check if the move has already been checked
                                    if not self.in_check(piece, king_move) and not self.in_check(left_rook, rook_move): #Check if the moves does not lead to a check situation
                                        piece.add_move(king_move) #Add the king move to its list
                                        left_rook.add_move(rook_move) #Add the rook move to its list
                                else:
                                    piece.add_move(king_move) #Add it to the list
                                    left_rook.add_move(rook_move) #Add the rook move to its list 
                                
                ##King castling
                right_rook = self.tiles[row][7].piece #Get the piece on the far right of the king
                if isinstance(right_rook, Rook): #Check if this piece is a rook
                    if not right_rook.moved: #Check if the rook has not move yet
                        for column in range(5,7): #Loop the tiles between the rook and the king
                            if self.tiles[row][column].has_piece(): #Check if there is a piece on the tile
                                break #break because there is an obstacle between the rook and the king
                            
                            elif column == 6:
                                piece.right_rook = right_rook #Add a reference to the rook
                                
                                ###Rook move
                                initial_tile = Tile(row, 7) #Set the rook initial tile
                                final_tile = Tile(row, 5) #Set the rook destination tile
                                rook_move = Move(initial_tile, final_tile) #Create the new move
                                
                                ###King move
                                initial_tile = Tile(row, col) #Set the king initial tile
                                final_tile = Tile(row, 6) #Set the king destination tile
                                king_move = Move(initial_tile, final_tile) #Create the new move
                               
                                if not checked: #Check if the move has already been checked
                                    if not self.in_check(piece, king_move) and not self.in_check(right_rook, rook_move): #Check if the moves does not lead to a check situation
                                        piece.add_move(king_move) #Add the king move to its list
                                        right_rook.add_move(rook_move) #Add the rook move to its list
                                else:
                                    piece.add_move(king_move) #Add it to the list
                                    right_rook.add_move(rook_move) #Add the rook move to its list
        
        if isinstance(piece, Pawn):
            pawn_moves()
        
        elif isinstance(piece, Knight):
            knight_moves()
            
        elif isinstance(piece, Bishop):
            line_moves([
                (1, 1), #down right direction
                (1, -1), #down left direction
                (-1, 1), #up right direction
                (-1, -1) #up left direction
            ])
        
        elif isinstance(piece, Rook):
            line_moves([
                (1, 0), #down direction
                (0, 1), #right direction
                (-1, 0), #up direction
                (0, -1) #left direction
            ])
        
        elif isinstance(piece, Queen):
            line_moves([
                (1, 1), #down right direction
                (1, -1), #down left direction
                (-1, 1), #up right direction
                (-1, -1), #up left direction
                (1, 0), #down direction
                (0, 1), #right direction
                (-1, 0), #up direction
                (0, -1) #left direction
            ])
        
        elif isinstance(piece, King):
            king_moves()
    
    def move(self, piece, move, testing=False):
        """
        Moving a piece on the board
        """
        initial_tile = move.initial_tile
        final_tile = move.final_tile
        
        empty_en_passant = self.tiles[final_tile.col][final_tile.row].is_empty()
        
        self.tiles[initial_tile.col][initial_tile.row].piece = None #Clear the initial tile
        self.tiles[final_tile.col][final_tile.row].piece = piece #Set the piece on his destination tile
        
        if isinstance(piece, Pawn): #Check if the piece is a pawn
            ##Pawn promotion
            self.pawn_promotion(piece, final_tile) #Promote the pawn to Queen
            
            ##Pawn en passant
            difference = final_tile.row - initial_tile.row
            if difference != 0 and empty_en_passant: #Check if the pawn captured an enemy pawn (diagonal move) and if the tile is empty
                self.tiles[initial_tile.col][initial_tile.row + difference].piece = None #Clear the initial tile
                self.tiles[final_tile.col][final_tile.row].piece = piece #Set the piece on his destination tile
            
        ##King and Queen castling
        if isinstance(piece, King): #Check if the piece is the king
            if self.castling(initial_tile, final_tile) and not testing: #Check if we are castling
                difference = final_tile.row - initial_tile.row #Check which castling is done (king or queen castling)
                if difference < 0:
                    rook = piece.left_rook
                else:
                    rook = piece.right_rook
                rook_move = rook.moves[-1]
                self.move(rook, rook_move) #Move the rook with its last possible move (that we just added to the list on the king_moves() function)
        
        piece.moved = True #Set the piece in the "already moved" state
        piece.clear_moves() #Clear the list of possible moves as the piece position has changed
        self.last_move = move #Saving the move as the last piece move
            
    def valid_move(self, piece, move):
        """
        return all possible moves of the piece in the current position
        """
        return move in piece.moves
    
    def get_all_valid_moves(self, game):
        valid_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.tiles[row][col].piece
                if piece != None and piece.color == game.next_player:
                    self.possible_moves(piece, row, col)
                    if piece.moves != None:
                        for move in piece.moves:
                             valid_moves.append(move)
        return valid_moves
    
    def pawn_promotion(self, piece, final_tile):
        """
        Promote pawn that reached his opponent backline
        """
        if final_tile.col == 0 or final_tile.col == 7: #Check if the pawn is on either one of the backlines
            self.tiles[final_tile.col][final_tile.row].piece = Queen(piece.color) #Replace the pawn by a new Queen
    
    def castling(self, initial_tile, final_tile):
        """
        Check if the king is castling
        """
        return abs(initial_tile.row - final_tile.row) == 2
    
    def in_check(self, piece, move):
        """
        Check if there is a check situation
        """
        temp_board = copy.deepcopy(self) #Create a temporary copy of the board
        temp_piece = copy.deepcopy(piece) #Create a temporary copy of the piece
        temp_board.move(temp_piece, move, testing=True) #Move the piece
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.tiles[row][col].has_hostile_piece(piece.color): #Check if there is an enemy piece
                    enemy = temp_board.tiles[row][col].piece #Get the enemy piece
                    temp_board.possible_moves(enemy, row, col, checked=True) #Get all possible moves of the enemy piece
                    for possible_move in enemy.moves: #Loop for each possible moves
                        if isinstance(possible_move.final_tile.piece, King): #Check if there is the oponent king on the final tile
                            return True #Return that there is a check situation
        return False #Return that there is no check situation
    
    def set_en_passant(self, piece):
        """
        Enable the en passant attribut
        """
        if not isinstance(piece, Pawn): #Check if the piece is not a Pawn
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.tiles[row][col].piece, Pawn):
                    self.tiles[row][col].piece.en_passant = False
        
        piece.en_passant = True
        
    def ai_random_move(self, valid_moves):
        return valid_moves[random.randint(0, len(valid_moves) - 1)]    
    
    def ai_best_move(self, depth, game, is_maximizing):
        
        print("The AI is thinking...")
        valid_moves = self.get_all_valid_moves(game)
        board = copy.deepcopy(self)
        optimal_move = None
        
        if valid_moves == None:
            return None
        elif is_maximizing:
            max_value = -CHECKMATE
        
            for move in valid_moves:
                piece = copy.deepcopy(self.tiles[move.initial_tile.col][move.initial_tile.row].piece)
                if piece != None:
                    board.move(piece, move)
                    value = max(max_value, self.minimax(depth - 1, board, game, -CHECKMATE, CHECKMATE, not is_maximizing))
                    if value > max_value:
                        max_value = value
                        optimal_move = move
                        print("new optimal move")
                        print("max value =")
                        print(max_value)
                        print((optimal_move.initial_tile.row, optimal_move.initial_tile.col), (optimal_move.final_tile.row, optimal_move.final_tile.col))
            return optimal_move
        else:
            min_value = CHECKMATE
            for move in valid_moves:
                piece = copy.deepcopy(self.tiles[move.initial_tile.col][move.initial_tile.row].piece)
                if piece != None:
                    board.move(piece, move)
                    value = min(min_value, board.minimax(depth - 1, board, game, -CHECKMATE, CHECKMATE, not is_maximizing))
                    if value < min_value:
                        min_value = value
                        optimal_move = move
                        # print("new optimal move")
                        # print("min value =")
                        # print(min_value)
                        # print((optimal_move.initial_tile.row, optimal_move.initial_tile.col), (optimal_move.final_tile.row, optimal_move.final_tile.col))
            return optimal_move
        
    def minimax(self, depth, board, game, alpha, beta, is_maximizing):
        """
        Returns the optimal move in the current situation
        """
        if depth == 0:
            return board.evaluate_board()
        
        valid_moves = board.get_all_valid_moves(game)
        if is_maximizing:
            if valid_moves == None:
                return -CHECKMATE
            max_value = -CHECKMATE
            for move in valid_moves:
                piece = self.tiles[move.initial_tile.col][move.initial_tile.row].piece
                if piece != None:
                    board.move(piece, move)
                    value = max(max_value, board.minimax(depth - 1, board, game, alpha, beta, False))
                    if value > max_value:
                        max_value = value
            return max_value
        else:
            if valid_moves == None:
                return CHECKMATE
            min_value = CHECKMATE
            for move in valid_moves:
                piece = self.tiles[move.initial_tile.col][move.initial_tile.row].piece
                if piece != None:
                    board.move(piece, move)
                    value = min(min_value, board.minimax(depth - 1, board, game, alpha, beta, True))
                    if value < min_value:
                        min_value = value
            return min_value
        
        
    def evaluate_board(self):
        """
        Evaluate the board state : returns a positive value if white has more material, a negative value if black does
        """
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.tiles[row][col].piece
                if piece != None:
                    score += piece.value
        return score