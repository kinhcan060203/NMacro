import customtkinter
from time import sleep
import os
from PIL import Image


class Home_page(customtkinter.CTkFrame):
    def __init__(self,master):
        super(Home_page, self).__init__(master=master)
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")





