import os
import json
import threading
import customtkinter
from time import sleep
from uuid import uuid4
import tkinter.messagebox
from tkinter import *
from PIL import Image
from datetime import datetime
from schedule_parameter import Schedule_Parameter
from more_detail_subwindow import More_Detail_Subwindow
from edit_window import Edit_Record
from config import *




class Scheduler(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Scheduler, self).__init__(master=master)
        self.configure(fg_color='transparent',corner_radius=3)
        self.master = master
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
      
        self.icon_rocket = customtkinter.CTkImage(Image.open(os.path.join(image_path, "rocket.png")), size=(28, 28))
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.schedule_wrapper = customtkinter.CTkFrame(self,corner_radius=3,fg_color='#DDDDDD',
                                                       border_color='#555555',border_width=2)
        self.schedule_wrapper.grid_columnconfigure((1,2,3),weight=1)
        self.schedule_wrapper.grid_rowconfigure(5,weight=1)


        self.label_frame = customtkinter.CTkLabel(self.schedule_wrapper, text="Schedule",justify="center",anchor='center',font=('Helvetica',24,'bold'),text_color='#33CCFF')
        self.label_frame.grid(row=0, column=0,columnspan=10,
                           padx=15, pady=10,
                           sticky="ew")

        self.label_record_name = customtkinter.CTkLabel(self.schedule_wrapper, text="Record name",justify="left",anchor='w',width=100)
        self.label_record_name.grid(row=2, column=0,
                           padx=(15,12), pady=10,
                           sticky="nw")
        self.record_name_var = customtkinter.StringVar(value='')
        self.entry_record_name = customtkinter.CTkEntry(self.schedule_wrapper,textvariable=self.record_name_var)
        self.entry_record_name.grid(row=2, column=1,
                            columnspan=3, padx=(12,15),
                            pady=10, sticky="ew")
        self.entry_record_name.bind('<FocusIn>',lambda e:self.focus_in(self.entry_record_name))
        self.entry_record_name.bind('<FocusOut>',lambda e:self.focus_out(self.entry_record_name))

        self.execute_btn = customtkinter.CTkButton(
            master=self.schedule_wrapper,  corner_radius=10, width=50, height=20, text='Execute',border_color='black',border_width=2,
            fg_color='gray75', hover_color=("gray70", "gray30"),border_spacing=10,font=('Helvetica',14,'bold'),text_color='black',
            image=self.icon_rocket, anchor="center", command=lambda :self.threading_activate(target=self.execute_schedule))
        self.execute_btn.grid(row=15, column=3,sticky='e',padx=15,pady=12)

        self.more_detail_subwindow = More_Detail_Subwindow(self)
        self.schedule_parameter=Schedule_Parameter(self.schedule_wrapper)
        self.schedule_parameter.grid(row=5, column=0,columnspan=5,padx=3,
                            sticky="nsew")
        
        self.edit_window = Edit_Record(self)
        self.TreeView_handles={}
        self.TreeView_handles['schedule_window'] = self.schedule_wrapper
        self.TreeView_handles['edit_window'] = self.edit_window
        self.thread_handle={}
        self.schedule_info={}
        self.current_detail_show=''

        self.show_eventsTreeview(treeView_name='schedule_window')

    def show_eventsTreeview(self,treeView_name):
        treeView = ''
        for name in self.TreeView_handles:
            if name == treeView_name:
                self.TreeView_handles[name].grid(row=0, column=0, sticky="nsew")
                treeView = self.TreeView_handles[name]
            else:
                self.TreeView_handles[name].grid_forget()

        return treeView
    

    def show_detail(self,data):
        record_name = data['record_detail']['record_name']
        self.current_detail_show = record_name
        self.more_detail_subwindow.upload_detail(data)
        self.more_detail_subwindow.grid(row=20, column=0,columnspan=5, sticky="nsew",pady=0)

    def hidden_detail(self):
        self.current_detail_show=''

        self.more_detail_subwindow.grid_forget()


    def focus_in(self,widget):
        widget.configure(border_color="#555555")
    def focus_out(self,widget):
        widget.configure(border_color="#EEEEEE")


        
    def get_record_info(self,record_name):

        dir_path = os.path.join(os.path.dirname(__file__),'My Record')
        located_detail={}
        with open(os.path.join(dir_path,'located_detail.json'),'r',encoding='utf-8') as jsonfile:
            located_detail=json.load(jsonfile)
        folder_located = list(located_detail.keys())[list(located_detail.values()).index(record_name)]
        if folder_located:

            file_path = os.path.join(dir_path,folder_located,'record.json')
            with open(file_path,'r',encoding='utf-8') as f:
                record_detail = json.load(f)['record_detail']
            return record_detail
        else:
            tkinter.messagebox.showwarning(title='Record name',message='Record name not found !!!')
            return False
        
    def execute_schedule(self):

        param = self.schedule_parameter.get_all_param()
        if not param:
            return
        schedule_name = param['schedule_name']
        record_name = self.entry_record_name.get()
        record_detail = self.get_record_info(record_name)
        if not record_detail:
            self.entry_record_name.focus()
            return False
        exec_command=  record_detail['exec_command']
        profile_user=  record_detail['profile_user']

        
        self.execute_btn.configure(fg_color='#CC00CC',text_color='white',hover_color='#CC00CC')
        res = tkinter.messagebox.askyesno("Execute", "Are you sure to execute it ?")
        if not res:
            self.execute_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70')
            return
        upload_timestamp=str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
        folder_located = str(uuid4())
        folder_path = os.path.join(dir_path,folder_located)
        os.mkdir(folder_path)
        modified_timestamp = 'xxxx-xx-xx xx:xx'
        finished_timestamp = 'xxxx-xx-xx xx:xx'
        schedule_info = {
            'folder_located':folder_located,
            'profile_user':profile_user,
            'upload_timestamp':upload_timestamp,
            'modified_timestamp':modified_timestamp,
            'finished_timestamp':finished_timestamp,
            'exec_command':exec_command,
        }

        schedule_info.update(param)
        status_list = ['Waiting']*len(exec_command)
        with open(os.path.join(folder_path,'logs.txt'), 'w',encoding='utf-8') as outfile:
            pass

        located_detail={}
        with open(os.path.join(dir_path,'located_detail.json'),'r',encoding='utf-8') as jsonfile:
            located_detail=json.load(jsonfile)
        new_located = {
            folder_located:schedule_name
        }
        located_detail.update(new_located)
        with open(os.path.join(dir_path,'located_detail.json'),'w',encoding='utf-8') as jsonfile:
            json.dump(located_detail, jsonfile, indent = 4)
                
        data = self.update_schedule_file(schedule_info=schedule_info)
        data['status_list']=status_list
        self.master.execute_schedule_event(data=data)
        self.master.reset_library(record_name=record_name)




    def update_schedule_file(self,schedule_info):
        data={'schedule_detail':schedule_info}
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        folder_path =  schedule_info['folder_located']
        with open(os.path.join(dir_path,folder_path,'schedule.json'), 'w',encoding='utf-8') as outfile:
            json.dump(data,outfile ,indent=4)
        return data

   

    def threading_activate(self,target,args=(),name=''):
        if not name:
            name = uuid4()
        self.thread_handle[name] = threading.Thread(target=target,args=args)
        self.thread_handle[name].daemon = True
        self.thread_handle[name].start()
   

    def reset(self):
        self.execute_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70')
        self.record_name_var.set('')
        self.schedule_parameter.reset()

        
    def upload_file(self,data):
        record_name = data['record_name']
        self.record_name_var.set(record_name)
        schedule_name=self.create_schedule_name(data=data)
        self.schedule_parameter.schedule_name_var.set(schedule_name)


    def create_schedule_name(self,data):
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
        schedule_name = data['record_name'] + '_#'
        with open(os.path.join(dir_path,'located_detail.json'),'r',encoding='utf-8') as jsonfile:
            located_detail=json.load(jsonfile)
        all_schedule_name = located_detail.values()
        i=0
        while True:
            i+=1
            if schedule_name+str(i) not in all_schedule_name:
                break
        return schedule_name+str(i)




  


