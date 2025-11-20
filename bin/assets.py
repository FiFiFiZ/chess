import pygame
import os

class Assets:
    def __init__(self):

        self.sprites = []
        self.directories = {}

        print("what's in src: " + str(os.listdir("src")))
        # os.chdir("./src")

        self.open_folder("./src")

        print(self.directories)
        
        # print(os.listdir("./src/skins/long (3D VIEW)"))



    def open_folder(self, path):
        files_in_path = os.listdir(path)

        for fileType in files_in_path:
            if "."  not in fileType: # if folder
                self.directories[path + "/" + fileType] = {}
                self.open_folder(path + "/" + fileType)
            else: # if file
                # load image and assign a value to key at the proper location in dictionary
                self.directories[path][fileType] = pygame.image.load(path + "/" + fileType) # this adds an item in the folder location and assigns it the image data
        
Assets()
