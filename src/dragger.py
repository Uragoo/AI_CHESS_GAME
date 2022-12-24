import pygame
from const import *

class Dragger:
    
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False
        
    def update_mouse(self, pos):
        """
        Update the position of the mouse
        """
        self.mouseX, self.mouseY = pos
        
    def save_initial(self, pos):
        """
        Save the initial position of a piece before being dragged
        """
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE
    
    def drag_piece(self, piece):
        """
        Putting the piece un drag mode
        """
        self.piece = piece
        self.dragging = True
        
    def undrag_piece(self):
        """
        Disabling drag mode for the actual piece
        """
        self.piece = None
        self.dragging = False
        
    def update_blit(self, surface):
        """
        Updating the image while being dragged
        """
        self.piece.set_texture(size=128) #Setting size to 128 pixels
        texture = self.piece.texture 
        image = pygame.image.load(texture) #Loading image
        image_center = (self.mouseX, self.mouseY) #Centering on x and y axis
        self.piece.texture_rect = image.get_rect(center=image_center) #Getting the image borders
        surface.blit(image, self.piece.texture_rect) #Merging the image inside the tile