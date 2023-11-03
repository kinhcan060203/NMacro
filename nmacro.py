import customtkinter
from PIL import Image
import os
from record_page import Record_page
from home_page import Home_page


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("NMacro")
        self.geometry("1050x650")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
        
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(
            image_path, "cute_wolf.png")), size=(36, 36))
        
        self.home_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home.png")), size=(30, 30))
        self.camera_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "camera.png")), size=(30, 30))    
        self.iconbitmap(os.path.join(   
            image_path, "cute_wolf.ico"))



        self.navigation_sidebar = customtkinter.CTkFrame(self, corner_radius=0,fg_color='#FFCCCC')
        self.navigation_sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_wrapper = customtkinter.CTkLabel(self.navigation_sidebar, text="  NMacro", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_wrapper.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_sidebar, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color='#111111', hover_color='#AAAAAA', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                   image=self.home_icon,anchor='w', command=lambda: self.select_frame_by_name("Home"))
        self.home_button.grid(row=1, column=0, sticky="ew",padx=(0,5))      

        self.record_button = customtkinter.CTkButton(self.navigation_sidebar, corner_radius=0, height=40, border_spacing=10, text="Record",
                                              fg_color="transparent", text_color='#111111', hover_color='#AAAAAA', font=customtkinter.CTkFont(size=12, weight="normal"),
                                              image=self.camera_icon,anchor='w', command=lambda: self.select_frame_by_name("Record"))
        self.record_button.grid(row=2, column=0, sticky="ew",padx=(0,5))

        self.record_frame = Record_page(self)
        self.home_frame = Home_page(self)   
        self.select_frame_by_name("Record")

    def select_frame_by_name(self, name):
        self.home_button.configure(
            fg_color='#999999' if name == "Home" else "transparent")
        self.record_button.configure(
            fg_color='#999999' if name == "Record" else "transparent")

        if name == "Home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()   
        if name == "Record":
            self.record_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.record_frame.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
