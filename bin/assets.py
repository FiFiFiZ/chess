import pygame
import os

class Assets:
    def __init__(self):
        # self.folder_names = {"Standard"}
        self.directories = [os.listdir("./src")]
        self.sprites = []
        self.open_folder()
        # os.chdir("./bin")
        print(os.listdir("./src"))



    def open_folder(self, ):
        for folder in self.directories:
            return
        
Assets()