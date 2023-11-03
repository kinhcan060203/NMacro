import os
import json
import customtkinter
import tkinter as tk
from PIL import Image
from time import sleep
from tkinter import *
from PIL import Image
from datetime import datetime
import random
status_fg_color = {
        'Completed':'#00FF00',
        'Waiting':'#CDAA7D',
        'Error':'#FF0000',
        'Processing':'#97FFFF',
        'Scheduled':'#BF3EFF',
    }

config = {'tab_active':'#888888','unactive_tab':'#BBBBBB','unactive_hover_tab':'#AAAAAA','active_mode_text':'#3366CC','unactive_mode_text':'#0099FF'}


def rgb_to_hex(r, g, b):
    return '#'+('{:02X}' * 3).format(r, g, b)


class TreeView(customtkinter.CTkFrame):
    def __init__(self, master):
        super(TreeView, self).__init__(master=master)

        self.master = master

        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images")
        
        self.wolf_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "cute_wolf.png")), size=(15, 15))


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.tab_bar = customtkinter.CTkFrame(master=self, height=26, fg_color=config['unactive_tab'],corner_radius=0)
        self.tab_bar.grid(row=0,column=0, sticky="nsew",columnspan=2)

        self.bottom_border_top_bar = customtkinter.CTkFrame(master=self, height=6, fg_color=config['tab_active'],corner_radius=0)
        self.bottom_border_top_bar.grid(row=1,column=0, sticky="ew",columnspan=2)

        self.configure(fg_color='grey30',corner_radius=0)
        self.treeView_screen = customtkinter.CTkScrollableFrame(self,fg_color='grey30',corner_radius=0)
        self.treeView_screen.grid_columnconfigure(0,weight=1)   
        self.treeView_screen.grid(row=3, column=0, sticky="nsew",columnspan=2)

        self.label_event = customtkinter.CTkLabel(master=self, height=24, fg_color='#00F5FF',text='Event',corner_radius=0,
                                                  justify="center", anchor="center",font=('Helvetica',12,'bold'),text_color='#333333')
        self.label_event.grid(row=2,column=0, sticky="ew")
        self.label_status = customtkinter.CTkLabel(master=self, height=24,width=97, fg_color='#54FF9F',text='Status',corner_radius=0,
                                                  justify="center", anchor="center",font=('Helvetica',12,'bold'),text_color='#333333')
        self.label_status.grid(row=2,column=1, sticky="ew")

        self.hex_color_handles = {}
        self.children_handles = {}
    
    def insert_tab_treeView(self,current_window_handle):

        random_rgb = random.sample(range(100,250), 3)

        hex_color = rgb_to_hex(*random_rgb)
        self.hex_color_handles[current_window_handle]=hex_color

        new_tab = customtkinter.CTkButton(
            master=self.tab_bar,  corner_radius=0, width=100, height=24,fg_color=hex_color,hover_color=hex_color,
            text=f'tab {current_window_handle}',font=('Helvetica',12,'bold'),text_color='#333333',anchor='center')
        
        new_tab.grid(row=0, column=len(self.tab_bar.winfo_children()))

    def insert_childView(self,iid, text,status='Waiting', fg_color_childView = '#33CCFF'):
    
        text = ' '*3+text
        fg_color = status_fg_color[status]
        childView =customtkinter.CTkFrame(master=self.treeView_screen,corner_radius=0,fg_color=fg_color_childView,border_color='white',border_width=2)
        content = customtkinter.CTkLabel(master=childView,image=self.wolf_icon,compound='left', text=text,fg_color='transparent',text_color='black',corner_radius=0,anchor='w')
        status_content = customtkinter.CTkLabel(master=childView,text=status,width=80,fg_color=fg_color,text_color='black',corner_radius=2,anchor='center',justify='center',
                                              font=('Helvetica',12,'bold'))
        childView.grid_columnconfigure(0,weight=1)
        childView.bind('<Button>',command=lambda e,iid=iid,childView = childView: self.click_childView(iid=iid,childView=childView))
        childView.bind('<Enter>',command=lambda e,iid=iid,childView = childView: self.enter_childView(iid=iid,childView=childView))
        childView.bind('<Leave>',command=lambda e,iid=iid,childView = childView: self.leave_childView(iid=iid,childView=childView))
        content.bind('<Button>',command=lambda e,iid=iid,childView = childView: self.click_childView(iid=iid,childView=childView))
        content.bind('<Enter>',command=lambda e,iid=iid,childView = childView: self.enter_childView(iid=iid,childView=childView))
        content.bind('<Leave>',command=lambda e,iid=iid,childView = childView: self.leave_childView(iid=iid,childView=childView))
        content.grid(column=0,row=0,padx=4,sticky='w',pady=5)
        status_content.grid(column=1,row=0,sticky='nsew',padx=2,pady=2)

        childView.grid(column=0,row=iid,sticky='ew')
        self.children_handles[iid] = [childView,status_content]
        return childView 

    def enter_childView(self,iid,childView):
        # if iid in self.pare_child_handle:
        #     childView.configure(fg_color='#00F5FF')
        # else:
        #     childView.configure(fg_color='#00F5FF') 
        pass

    def leave_childView(self,iid,childView):
        # if iid in self.pare_child_handle:
        #     childView.configure(fg_color='#33FFFF')
        # else:
        #     childView.configure(fg_color='#33FFFF') 
        pass
    def click_childView(self,iid,childView):
        pass