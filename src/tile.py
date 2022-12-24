
class Tile:
    
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    
    def __init__(self, col, row, piece=None):
        self.col = col
        self.row = row
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        #Check if the tile contains a piece
        return self.piece != None
    
    def has_hostile_piece(self, color):
        #Check if the tile contains a rival piece
        return self.has_piece() and self.piece.color != color
    
    def has_friendly_piece(self, color):
        #Check if the tile contains a friendly piece
        return self.has_piece() and self.piece.color == color
    
    def is_empty(self):
        #Check if the tile is empty / contains no piece
        return not self.has_piece()
    
    def is_empty_or_hostile(self, color):
        #Check if the tile is either empty or contains an ennemy
        return self.is_empty() or self.has_hostile_piece(color)
    
    @staticmethod
    def in_range(*args):
        #Check if all arguments are inside the board
        for arg in args:
            if arg < 0 or arg > 7:
                return False
            
        return True
    
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]