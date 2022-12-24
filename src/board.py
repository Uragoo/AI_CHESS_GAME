from const import *
from tile import Tile
from piece import *
from move import Move

class Board:

    def __init__(self):
        #Initializing Tiles
        self.tiles = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('black')
        self._add_pieces('white')

    def _create(self):
        #Creating all tiles
        for row in range(ROWS):
            for col in range(COLS):
                self.tiles[row][col] = Tile(row, col)

    def _add_pieces(self, color):
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
        
    def possible_moves(self, piece, row, col):
        """
        Determine all valid moves of the piece
        """
        def pawn_moves():
            #Defining all pawn moves
            if piece.moved:
                steps = 1
            else:
                steps = 2
            
            #Vertical moves
            start = row + piece.direction #Current position with pawn direction
            end = row + (piece.direction * (1 + steps)) #Maximum position (2 forward if it hasn't move yet else 1)
            for move_row in range(start, end, piece.direction):
                if Tile.in_range(move_row): #Check if the move is inside the board
                    if self.tiles[move_row][col].is_empty(): #Check if the tile is empty
                        initial_tile = Tile(row, col)
                        final_tile = Tile(move_row, col)
                        move = Move(initial_tile, final_tile) #Create the new possible move
                        piece.add_move(move) #Add it to the list
                    else:
                        #Pawn is blocked
                        break #prevent the pawn to move 2 tiles forward even if an other piece is in front of it
                else:
                    break
            
            #Diagonal moves
            move_row = row + piece.direction
            move_cols = [
                col - 1,
                col + 1
            ]
            
            for move_col in move_cols:
                if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                    if self.tiles[move_row][move_col].has_hostile_piece(piece.color): #Check if the tile contains an enemy
                        initial_tile = Tile(row, col)
                        final_tile = Tile(move_row, move_col)
                        move = Move(initial_tile, final_tile) #Create the new possible move
                        piece.add_move(move) #Add it to the list
        
        def knight_moves():
            #Defining all knight possible moves
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
                        final_tile = Tile(move_row, move_col)
                        move = Move(initial_tile, final_tile) #Create the new possible move
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
            for increment in increments:
                row_inc, col_inc = increment
                move_row = row + row_inc
                move_col = col + col_inc
                
                while True:
                    if Tile.in_range(move_row, move_col): #Check if the move is inside the board
                        initial_tile = Tile(row, col)
                        final_tile = Tile(move_row, move_col)
                        move = Move(initial_tile, final_tile) #Create new possible move
                        
                        if self.tiles[move_row][move_col].is_empty():
                            piece.add_move(move) #Add it to the list
                        
                        if self.tiles[move_row][move_col].has_hostile_piece(piece.color):
                            piece.add_move(move) #Add it to the list
                            break #Prevent to continue looping after reaching an enemy
                            
                        if self.tiles[move_row][move_col].has_friendly_piece(piece.color):
                            break #Prevent to continue looping behind an ally
                        
                    else:
                        break
                    
                    move_row = move_row + row_inc
                    move_col = move_col + col_inc
        
        def king_moves():
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
                                move = Move(initial_tile, final_tile) #Create the new move
                                left_rook.add_move(move) #Add it to the list of possible move of the rook
                                
                                ###King move
                                initial_tile = Tile(row, col) #Set the king initial tile
                                final_tile = Tile(row, 2) #Set the king destination tile
                                move = Move(initial_tile, final_tile) #Create the new move
                                piece.add_move(move) #Add it to the list of possible move of the king
                                
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
                                print((final_tile.row, final_tile.col))
                                move = Move(initial_tile, final_tile) #Create the new move
                                right_rook.add_move(move) #Add it to the list of possible move of the rook
                                
                                ###King move
                                initial_tile = Tile(row, col) #Set the king initial tile
                                final_tile = Tile(row, 6) #Set the king destination tile
                                move = Move(initial_tile, final_tile) #Create the new move
                                piece.add_move(move) #Add it to the list of possible move of the king
        
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
    
    def move(self, piece, move):
        """
        Moving a piece on the board
        """
        initial_tile = move.initial_tile
        final_tile = move.final_tile
        
        self.tiles[initial_tile.col][initial_tile.row].piece = None #Clear the initial tile
        self.tiles[final_tile.col][final_tile.row].piece = piece #Set the piece on his destination tile
        
        ##Pawn promotion
        if isinstance(piece, Pawn): #Check if the piece is a pawn
            self.check_promotion(piece, final_tile) #Promote the pawn to Queen
            
        ##King castling
        if isinstance(piece, King): #Check if the piece is the king
            if self.castling(initial_tile, final_tile): #Check if we are castling
                difference = final_tile.row - initial_tile.row #Check which castling is done (king or queen castling)
                print(difference)
                if difference < 0:
                    rook = piece.left_rook
                else:
                    rook = piece.right_rook
                rook_move = rook.moves[-1]
                self.move(rook, rook_move) #Move the rook with its last possible move (that we just added to the list on line 234)
        
        piece.moved = True #Set the piece in the "already moved" state
        piece.clear_moves() #Clear the list of possible moves as the piece position has changed
        self.last_move = move #Saving the move as the last piece move
    
    def valid_move(self, piece, move):
        """
        return all possible moves of the piece in the current position
        """
        return move in piece.moves
    
    def check_promotion(self, piece, final_tile):
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