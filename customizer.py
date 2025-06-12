# imports
import pygame # helps rendering graphics
from PIL import Image # helps w advanced image handling
import os # for file path and directory operations

# class
class Customizer:
    # method that defines customizer class
    def __init__(self):
        # Variables as instance attributes
        self.baseWidth = 1300
        self.baseHeight = 1900
        self.scaleMult = 1.3

        # Load background image once during initialization
        # self.background = pygame.image.load("assets/backgrounds/DressingRoom.png").convert()
    
    # method for total customization
    def overall(self):
        print("Customizer run method called — test successful!")
