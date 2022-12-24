
class Move:
    
    def __init__(self, init_tile, final_tile):
        self.initial_tile = init_tile
        self.final_tile = final_tile
        
    def __eq__(self, other):
        return self.initial_tile == other.initial_tile and self.final_tile == other.final_tile