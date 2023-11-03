import os
import json
import threading
import customtkinter
from PIL import Image
from uuid import uuid4
from tkinter import *
from PIL import Image
from datetime import datetime
from pathlib import Path
from child_item import Child_Item
import glob
from config import *


class Tab_Library(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super(Tab_Library, self).__init__(master=master)


        
        self.master = master
        self.configure(fg_color='transparent', corner_radius=3,border_color='#0099FF',border_width=1)
        self.record_child_handles={}
        self.prev_child_name_clicked = ''


    def show_all_record_child(self):

        dir_path = os.path.join(os.path.dirname(__file__),'My Record')
        file_paths =  glob.glob(dir_path + "/*/record.json")
        file_paths.sort(key=lambda x: os.path.getmtime(x),reverse=False)

        for file_path in file_paths:
            desc = {}
            with open(file_path,'r',encoding='utf-8') as f:
                desc = json.load(f)
            self.insert_record_child(desc=desc)

    def show_edit_window(self,data):
        record_name = data['record_detail']['record_name']
        parent = self.record_child_handles[record_name]
        data = data['record_detail']
        self.on_press(data['record_name'])
        self.upload_file(data['record_name'],data)
        parent.btn_edit.configure(fg_color='#0099FF',hover_color='#0099FF')
        parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
        self.master.master.show_detail_event(data={'record_detail': {}})
        treeView = self.master.master.show_scheduler_by_name(treeView_name='edit_window')
        treeView.upload_info(info=data)
    
    def show_more_detail(self,data):
        record_name = data['record_detail']['record_name']
        parent=self.record_child_handles[record_name]
        pre_fg_color = parent.btn_more_detail.cget('fg_color')

        self.on_press(record_name)
        self.upload_file(record_name,data)

        if pre_fg_color=='#0099FF' :
            parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
            self.master.master.show_detail_event(data={'record_detail': {}})
        else:
            parent.btn_more_detail.configure(fg_color='#0099FF',hover_color='#0099FF')
            self.master.master.show_detail_event(data=data)
    def modify_record_child(self, data,pre_record_name):
        record_name = data['record_detail']['record_name']
        pre_record_child=self.record_child_handles[pre_record_name]

        self.record_child_handles.pop(pre_record_name)

        new_record_child=self.create_record_child(record_name,data)
        row = pre_record_child.grid_info()['row']
        new_record_child.grid(row=row, column=0,sticky='snew',padx=5,pady=2)
        pre_record_child.grid_forget()
        
        self.on_press(record_name)
        self.upload_file(record_name,data)
    def reset_child(self,record_name):
        parent = self.record_child_handles[record_name]
        parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
        self.master.master.show_detail_event(data={'record_detail': {}})
        parent.configure(border_color=config['border_unactive_child'])

    def reset_all(self):
        for child_name,parent in self.record_child_handles.items():
            parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
            self.master.master.show_detail_event(data={'record_detail': {}})
            parent.configure(border_color=config['border_unactive_child'])

    def create_record_child(self,record_name,desc):
        saved_record = Child_Item(master=self,desc=desc)
        saved_record.bind("<ButtonPress>", lambda e: self.on_press(record_name=record_name))
        saved_record.bind("<ButtonRelease>", lambda e: self.upload_file(record_name=record_name,data=desc))

        for child_widget in saved_record.winfo_children():
            if not isinstance(child_widget,customtkinter.CTkButton):
                child_widget.bind("<ButtonPress>", lambda e: self.on_press(record_name=record_name))
                child_widget.bind("<ButtonRelease>", lambda e: self.upload_file(record_name=record_name,data=desc))

        self.record_child_handles[record_name] = saved_record
        return saved_record
    
    def insert_record_child(self,desc,is_click=False):
        index = len(self.winfo_children())
        row = 1000 - index
        record_name = desc['record_detail']['record_name']
        saved_record=self.create_record_child(record_name,desc)
        saved_record.grid(row=row, column=0,sticky='snew',padx=5,pady=2)
        if is_click:
            self.on_press(record_name)
            self.upload_file(record_name,desc)

    def on_press(self,record_name):
        parent=self.record_child_handles[record_name]
        prev_child_name = self.prev_child_name_clicked
        if prev_child_name:
            try:

                prev_parent = self.record_child_handles[prev_child_name]
                prev_parent.configure(fg_color='transparent',border_color=config['border_unactive_child'])
                prev_parent.btn_edit.configure(fg_color='#00F5FF',hover_color='#00E5EE')
                if prev_child_name != record_name:
                    prev_parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
        
                    self.master.master.show_detail_event(data={'record_detail': {}})
            except Exception as e:
                pass
                
        self.prev_child_name_clicked = record_name
        parent.configure(border_color='#FFFFFF')

    def upload_file(self,record_name,data,is_show=True):
        parent=self.record_child_handles[record_name]
        parent.configure(border_color=config['border_active_child'],fg_color='#98F5FF')
        self.master.master.upload_file_from_child(data=data)
        if is_show:
            parent.btn_edit.configure(fg_color='#00F5FF',hover_color='#00E5EE')
            treeView = self.master.master.show_scheduler_by_name(treeView_name='schedule_window')




