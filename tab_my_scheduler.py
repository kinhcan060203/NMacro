import os
import json
import customtkinter
from tkinter import *
from PIL import Image
from tab_library import Tab_Library
from child_item import Child_Item
from pathlib import Path
import glob
from config import *



class Tab_My_Scheduler(Tab_Library):
    def __init__(self, master):
        super(Tab_My_Scheduler, self).__init__(master=master)
        self.master = master
        
  
        self.prev_child_name_clicked = ''
        self.child_status_handles = {}
        self.child_handles={}

    def show_all_shedule_child(self):
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
        # self.show_with_upload_time_order(dir_path)
        self.show_with_modified_time_order(dir_path)

    def get_status_from_log(self,log_path,command_length):
        status_list=[]
        with open(log_path,'r',encoding='utf-8') as f:
            all_log = f.read().strip().split("\n\n")
            if len(all_log)==0:
                status_list = ['Waiting']
            else:
                last_log =all_log[-1].split('\n')
                for line in last_log:
                    if line:
                        status_list.append(line.split('|')[-1])
        status_list = status_list+['Waiting']*(command_length-len(status_list))
        return status_list
    
    def show_with_modified_time_order(self, dir_path):
        file_paths =  glob.glob(dir_path + "/*/*.json")
        file_paths.sort(key=lambda x: os.path.getmtime(x),reverse=False)
        for json_path in file_paths:
            data = {}
            log_path = os.path.join(os.path.dirname(json_path),'logs.txt')
            with open(json_path,'r',encoding='utf-8') as f:
                data = json.load(f)
 

            exec_command = data['schedule_detail']['exec_command']
            status_list=self.get_status_from_log(log_path, len(exec_command))
            data['status_list']=status_list
            self.master.master.upload_file_from_child(data=data)
            self.insert_schedule_child(data=data)


    def show_with_upload_time_order(self,dir_path):
        paths = sorted(Path(dir_path).iterdir(), key=os.path.getmtime,reverse=True)
        for dir_path in paths:
            json_paths = glob.glob(str(dir_path) + "/*.json")
            if json_paths:
                data = {}

                with open(json_paths[0],'r',encoding='utf-8') as f:
                    data = json.load(f)
                self.master.master.upload_file_from_child(data=data)
                self.insert_schedule_child(data=data)
        
    def modify_schedule_child(self,data,pre_schedule_name):
      
        schedule_name = data['schedule_detail']['schedule_name']
        pre_schedule_child=self.child_handles[pre_schedule_name]

        if schedule_name!=pre_schedule_name:
            self.child_handles.pop(pre_schedule_name)
            self.child_status_handles.pop(pre_schedule_name)
        new_schedule_child=self.create_schedule_child(data)
        row = pre_schedule_child.grid_info()['row']
        new_schedule_child.grid(row=row, column=0,sticky='snew',padx=5,pady=2)
        pre_schedule_child.grid_forget()
        
        self.on_press(schedule_name)
        self.on_release(schedule_name)

    def create_schedule_child(self,desc):
        schedule_name = desc['schedule_detail']['schedule_name']
        status = desc['schedule_detail']['status']
        saved_record = Child_Item(master=self,desc=desc)
        border_color = status_color_list[status]

        self.child_status_handles[schedule_name] = status
        self.child_handles[schedule_name] = saved_record

        saved_record.configure(border_color=border_color)
        saved_record.bind("<ButtonPress>", lambda e,schedule_name=schedule_name: self.on_press(schedule_name))
        saved_record.bind("<ButtonRelease>", lambda e,schedule_name=schedule_name: self.on_release(schedule_name))
        for child_widget in saved_record.winfo_children():
            if not isinstance(child_widget,customtkinter.CTkButton):
                child_widget.bind("<ButtonPress>", lambda e,schedule_name=schedule_name: self.on_press(schedule_name))
                child_widget.bind("<ButtonRelease>", lambda e,schedule_name=schedule_name: self.on_release(schedule_name))
        return saved_record
    
    def insert_schedule_child(self,data,is_click=False):
        schedule_name = data['schedule_detail']['schedule_name']
        index = len(self.winfo_children())
        row = 1000 - index
        saved_record = self.create_schedule_child(data)
        saved_record.grid(row=row, column=0,sticky='snew',padx=5,pady=2)
        if is_click:
            self.on_press(schedule_name)
            self.on_release(schedule_name)

    def set_status_child(self,schedule_name,new_status):
        color = status_color_list[new_status]
        child = self.child_handles[schedule_name]
        child_fg_color = child.cget('fg_color')
        if child_fg_color=='#98F5FF' :
            child.configure(border_color=color)

        child.status_content.configure(text_color=color,text = new_status)
        self.child_status_handles[schedule_name] = new_status

    def set_runtime_child(self,schedule_name,current_runtime):
        self.child_handles[schedule_name].update_runtime(current_runtime)


    def on_press(self,schedule_name):
        prev_child_name = self.prev_child_name_clicked
        parent = self.child_handles[schedule_name]

        if prev_child_name:
            try:
                prev_parent = self.child_handles[prev_child_name]
                prev_border_color = status_color_list[self.child_status_handles[prev_child_name]]
                prev_parent.configure(border_color=prev_border_color,fg_color='transparent')
                prev_parent.btn_edit.configure(fg_color='#00F5FF',hover_color='#00E5EE')
                if prev_child_name != schedule_name:
                    prev_parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
                    self.master.master.show_detail_event(data={'schedule_detail': {}})
            except Exception as e:
                pass
    
        self.prev_child_name_clicked = schedule_name
        parent.configure(border_color='#FFFFFF')

    def on_release(self,schedule_name,is_show=True):
        parent = self.child_handles[schedule_name]
        border_color = status_color_list[self.child_status_handles[schedule_name]]
        parent.configure(border_color=border_color,fg_color='#98F5FF')
        if is_show:
            parent.btn_edit.configure(fg_color='#00F5FF',hover_color='#00E5EE')
            self.master.master.show_logs_by_name(treeView_name=schedule_name)

    def show_edit_window(self,data):
        schedule_name = data['schedule_detail']['schedule_name']
        parent = self.child_handles[schedule_name]
        data = data['schedule_detail']
        self.on_press(data['schedule_name'])
        self.on_release(data['schedule_name'],is_show=False)
        parent.btn_edit.configure(fg_color='#0099FF',hover_color='#0099FF')
        parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
        self.master.master.show_detail_event(data={'schedule_detail': {}})
        treeView = self.master.master.show_logs_by_name(treeView_name='edit_window')
        treeView.upload_schedule_param(data=data)

    def show_more_detail(self,data):
        schedule_name = data['schedule_detail']['schedule_name']
        parent = self.child_handles[schedule_name]
        self.on_press(schedule_name)
        self.on_release(schedule_name)
        pre_fg_color = parent.btn_more_detail.cget('fg_color')
        if pre_fg_color=='#0099FF' :
            parent.btn_more_detail.configure(fg_color='#00F5FF',hover_color='#00E5EE')
            self.master.master.show_detail_event(data={'schedule_detail': {}})
            
        else:
            parent.btn_more_detail.configure(fg_color='#0099FF',hover_color='#0099FF')
            self.master.master.show_detail_event(data=data)