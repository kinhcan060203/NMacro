import os
import os
import customtkinter
from tkinter import *
from PIL import Image
from tab_save_record import Tab_Save_Record
from tab_library import Tab_Library
from tab_my_scheduler import Tab_My_Scheduler

tab_name_list=['record','library','scheduler']




class Side_Bar(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Side_Bar, self).__init__(master=master)

        self.master = master

        self.configure(fg_color='pink', corner_radius=3,border_color='black',border_width=1,width=280)
        self.grid_propagate(0)
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)


        self.navigate_tab = customtkinter.CTkFrame(master=self, fg_color='transparent')
        self.navigate_tab.grid(row=0, column=0 , sticky="sw", padx=5,pady=5,columnspan=3)


        self.tab_save_record = customtkinter.CTkButton(
            master=self.navigate_tab,  corner_radius=3, width=60, height=32,
            text='Save record',font=('Helvetica',12,'bold'),text_color='#FFFFFF',anchor='center',
            command=lambda :self.change_tab_by_name(name = 'record'))
        
        self.tab_library = customtkinter.CTkButton(
            master=self.navigate_tab,  corner_radius=3, width=60, height=32,
            text='Library',font=('Helvetica',12,'bold'),text_color='#FFFFFF',anchor='center',
            command=lambda :self.change_tab_by_name(name = 'library'))
        
        self.tab_my_scheduler = customtkinter.CTkButton(
            master=self.navigate_tab,  corner_radius=3, width=60, height=32,
            text='My Scheduler',font=('Helvetica',12,'bold'),text_color='#FFFFFF',anchor='center',
            command=lambda :self.change_tab_by_name(name = 'scheduler'))

 
        
        self.tab_navigate_handle = {}

        self.sidebar_handle = {}

        self.tab_navigate_handle['record'] = self.tab_save_record
        self.tab_navigate_handle['library'] = self.tab_library
        self.tab_navigate_handle['scheduler'] = self.tab_my_scheduler


        self.sidebar_handle['record'] = Tab_Save_Record(self)
        self.sidebar_handle['library'] = Tab_Library(self)
        self.sidebar_handle['scheduler'] = Tab_My_Scheduler(self)

        self.sidebar_handle['library'].show_all_record_child()
        self.sidebar_handle['scheduler'].show_all_shedule_child()




        
    def clear_navigate_list(self,list_navigate_name=[]):
        list_navigate_name = list_navigate_name if list_navigate_name else tab_name_list

        for name in list_navigate_name:
            self.tab_navigate_handle[name].grid_forget()
            self.sidebar_handle[name].grid_forget()


    def show_navigate_list(self,list_navigate_name):
        self.clear_navigate_list()
        for i,name in enumerate(list_navigate_name):
            self.tab_navigate_handle[name].grid(row=0, column=i, sticky="w",padx=(0,5))
        self.change_tab_by_name(list_navigate_name[0])

    def change_tab_by_name(self, name):
        for tab_name in tab_name_list:
            if tab_name == name:
                self.tab_navigate_handle[tab_name].configure(fg_color="#828282")
                self.sidebar_handle[tab_name].grid(row=1, column=0,columnspan=3, sticky="snew",
                          padx=(5,8), pady=5)

            else:
                self.tab_navigate_handle[tab_name].configure(fg_color="#CFCFCF")
                self.sidebar_handle[tab_name].grid_forget()


    

