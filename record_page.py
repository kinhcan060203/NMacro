import os
import json
import threading
import customtkinter
from PIL import Image
from time import sleep
from uuid import uuid4
import tkinter.messagebox
from tkinter import *
from PIL import Image
from logs import Logs
from record import Record
from scheduler import Scheduler
from side_bar import Side_Bar
from uuid import uuid4
from datetime import datetime
frame_name_list = ['Record','Scheduler','Logs']

class Record_page(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Record_page, self).__init__(master=master)
        self.master = master
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
      
        self.icon_record = customtkinter.CTkImage(Image.open(os.path.join(image_path, "record.jpg")), size=(25, 25))
        self.icon_stop_record = customtkinter.CTkImage(Image.open(os.path.join(image_path, "stop_record.png")), size=(25, 25))
        self.icon_calendar = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calendar.png")), size=(28, 28))
        self.icon_cogwheel = customtkinter.CTkImage(Image.open(os.path.join(image_path, "cogwheel.png")), size=(28, 28))

        self.configure(corner_radius=0,fg_color='#fbd786')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.tool_bar = customtkinter.CTkFrame(
            master=self, fg_color='gray30', corner_radius=0,height=56)


        self.record_btn = customtkinter.CTkButton(
            master=self.tool_bar,  corner_radius=3, height=40, text='Record',border_spacing=4,
            fg_color="gray30", hover_color='gray70',font=customtkinter.CTkFont(size=14, weight="bold"),
            image=self.icon_record, anchor="center", command=lambda :self.change_frame_by_name(name='Record'))


        
        self.scheduler_btn = customtkinter.CTkButton(
            master=self.tool_bar,  corner_radius=3, height=40, text='Scheduler',border_spacing=4,
            fg_color="gray30", hover_color='gray70',font=customtkinter.CTkFont(size=14, weight="bold"),
            image=self.icon_calendar, anchor="center", command=lambda :self.change_frame_by_name(name='Scheduler'))



        self.logs_btn = customtkinter.CTkButton(
            master=self.tool_bar,  corner_radius=3, height=40, text='My Logs',border_spacing=4,
            fg_color="gray30", hover_color='gray70',font=customtkinter.CTkFont(size=14, weight="bold"),
            image=self.icon_cogwheel, anchor="center", command=lambda :self.change_frame_by_name(name='Logs'))


        self.Logs = Logs(self)
        self.Record = Record(self)
        self.Scheduler = Scheduler(self)
        self.Side_Bar = Side_Bar(self)

        self.tool_bar.grid(row=0, column=0,columnspan=5, sticky="ew",padx=5, pady=10)
        self.record_btn.grid(row=0, column=1,padx=(5,0),pady=5)
        self.scheduler_btn.grid(row=0, column=2,padx=(5,0),pady=5)
        self.logs_btn.grid(row=0, column=3,padx=(5,0),pady=5)
        self.Side_Bar.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 5))

        self.thread_handle={}
        
        self.change_frame_by_name(name='Scheduler')

    def show_detail_event(self,data={}):
        record_detail =data.get('record_detail',None)
        schedule_detail =data.get('schedule_detail',None)
        if isinstance(record_detail,dict):
            if record_detail:
                self.Scheduler.show_detail(data)
            else:
                self.Scheduler.hidden_detail()
        if isinstance(schedule_detail,dict):
            if schedule_detail:
                self.Logs.show_detail(data)
            else:
                self.Logs.hidden_detail()

                
    def update_detail_event(self, data):
        record_detail =data.get('record_detail',None)
        schedule_detail =data.get('schedule_detail',None)
        if isinstance(record_detail,dict):
            if record_detail:
                self.update_file_json(data)
                record_name = record_detail['record_name']
                if self.Scheduler.current_detail_show == record_name:
                    self.show_detail_event(data)

        if isinstance(schedule_detail,dict):
            if schedule_detail:
                target = self.Side_Bar.sidebar_handle['scheduler']
                status = schedule_detail['status']
                schedule_name = schedule_detail['schedule_name']
                if status:
                    target.set_status_child(schedule_name,status)
                self.update_file_json(data)
                if self.Logs.current_detail_show == schedule_name:
                    self.show_detail_event(data)


    def update_file_json(self, data):
        
        record_detail =data.get('record_detail',None)
        schedule_detail =data.get('schedule_detail',None)
        if isinstance(record_detail,dict):
            dir_path = os.path.join(os.path.dirname(__file__),'My Record')
            if record_detail:
                folder_located = record_detail['folder_located']
                with open(os.path.join(dir_path,folder_located,'record.json'), "w",encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, indent = 4)
                    
        if isinstance(schedule_detail,dict):
            dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

            if schedule_detail:
                folder_located = schedule_detail['folder_located']
                with open(os.path.join(dir_path,folder_located,'schedule.json'), "w",encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, indent = 4)


    def edit_schedule_event(self,new_schedule_detail,pre_schedule_name,execute_modified=False):
        data = {
            'schedule_detail':new_schedule_detail
        }
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        schedule_name = new_schedule_detail['schedule_name']
        folder_located = new_schedule_detail['folder_located']
        new_name = {
            'schedule_name':schedule_name
        }
        self.update_file_detail(folder_located,new_name,pre_schedule_name)
        self.update_file_json(data)

        self.Logs.exchange_schedule(new_schedule_detail['schedule_name'],pre_schedule_name)
        if execute_modified:
            log_path = os.path.join(dir_path,folder_located,'logs.txt')
            with open(log_path, 'w',encoding='utf-8') as outfile:
                pass
            status_list = ['Waiting']*len(new_schedule_detail['exec_command'])
            data['status_list']=status_list
            self.execute_schedule_event(data=data,insert_new_tab=False)
        target = self.Side_Bar.sidebar_handle['scheduler']
        target.modify_schedule_child(data=data,pre_schedule_name=pre_schedule_name)

    def update_file_detail(self, folder_located,new_name,pre_name):
        record_name =new_name.get('record_name',None)
        schedule_name =new_name.get('schedule_name',None)
        if record_name:
            dir_path = os.path.join(os.path.dirname(__file__),'My Record')
        else:
            dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
        current_name = schedule_name if schedule_name else record_name
        if current_name !=pre_name:
            with open(os.path.join(dir_path,'located_detail.json'),'r+',encoding='utf-8') as jsonfile:
                located_detail=json.load(jsonfile)
                jsonfile.truncate(0)
                jsonfile.seek(0)
                located_detail[folder_located] = current_name
                json.dump(located_detail, jsonfile, indent = 4)


    def edit_record_event(self, new_record_detail,pre_record_name):
        data = {
            'record_detail':new_record_detail
        }
        new_record_name = {
            'record_name':new_record_detail['record_name']
        }
        folder_located = new_record_detail['folder_located']
        self.update_file_detail(folder_located,new_record_name,pre_record_name)
        self.update_file_json(data)
        target = self.Side_Bar.sidebar_handle['library']
        target.modify_record_child(data=data,pre_record_name=pre_record_name)

    def reset_library(self, record_name=''):
        target = self.Side_Bar.sidebar_handle['library']
        if record_name:
            self.Scheduler.hidden_detail()
            target.reset_child(record_name)
        else:
            target.reset_all()

    def execute_schedule_event(self,data,insert_new_tab=True):
        desc = data['schedule_detail']
        status_list =  data['status_list']
        schedule_name = desc["schedule_name"]
        exec_command =  desc['exec_command']
        self.Logs.add_treeView(exec_command = exec_command ,treeView_name=schedule_name,status_list=status_list)
        self.Logs.add_treeView(exec_command = exec_command ,treeView_name=schedule_name+'.log',status_list=status_list)

        if insert_new_tab:
            target = self.Side_Bar.sidebar_handle['scheduler']
            target.insert_schedule_child(data=data,is_click=True)
        self.change_frame_by_name(name='Logs')
        self.threading_activate(target=lambda desc=desc:self.Logs.run_schedule(data=desc))
        self.Scheduler.reset()
        


    def set_external_param_event(self,schedule_name,param):
        target = self.Side_Bar.sidebar_handle['scheduler']
        current_runtime = param.get('runtime',None)
        if current_runtime:
            target.set_runtime_child(schedule_name,current_runtime)



    def change_frame_by_name(self, name):
        target_record = self.Side_Bar.sidebar_handle['record']
        if name =='Scheduler':
            self.scheduler_btn.configure(fg_color="grey70",text_color='black')
            self.Side_Bar.show_navigate_list(list_navigate_name=['library'])
            self.Scheduler.grid(row=1, column=0, sticky="snew",
                          padx=5,pady=(0,5))
        else:
            self.scheduler_btn.configure(fg_color="grey30",text_color='white')
            self.Scheduler.grid_forget()

        if name =='Record':
            self.Side_Bar.show_navigate_list(list_navigate_name=['record'])
            self.record_btn.configure(fg_color="grey70",text_color='black',hover_color='#AAAAAA')

            self.scheduler_btn.configure(state='disabled')
            self.logs_btn.configure(state='disabled')

            self.Record.grid(row=1, column=0, sticky="snew",
                          padx=5,pady=(0,5))
            self.record_event()
        else:
            self.record_btn.configure(fg_color="grey30",text_color='white',hover_color='grey70')
            self.Record.grid_forget()
            target_record.reset()

        if name =='Logs':
            self.logs_btn.configure(fg_color="grey70",text_color='black')
            self.Side_Bar.show_navigate_list(list_navigate_name=['scheduler'])
            self.Logs.grid(row=1, column=0, sticky="snew",
                          padx=5,pady=(0,5))
        else:
            self.logs_btn.configure(fg_color="grey30",text_color='white')
            self.Logs.grid_forget()

    def show_scheduler_by_name(self, treeView_name):
        treeView = self.Scheduler.show_eventsTreeview(treeView_name=treeView_name)
        return treeView
    def show_logs_by_name(self, treeView_name):
        treeView = self.Logs.show_eventsTreeview(treeView_name=treeView_name)
        return treeView


    def upload_file_from_child(self, data):
        record_detail =data.get('record_detail',None)
        schedule_detail =data.get('schedule_detail',None)
        if isinstance(record_detail,dict):
            if record_detail:
                self.Scheduler.upload_file(data=record_detail)
        if isinstance(schedule_detail,dict):
            if schedule_detail:
                exec_command = schedule_detail['exec_command']
                treeView_name = schedule_detail['schedule_name']
                status_list = data['status_list']

                self.Logs.add_treeView(exec_command=exec_command,treeView_name=treeView_name,status_list=status_list)
                self.Logs.add_treeView(exec_command=exec_command,treeView_name=treeView_name+'.log',status_list=status_list)
 

    def stop_record_event(self,external_data={}):
        target = self.Side_Bar.sidebar_handle['record']
        target.change_mode('stop_record')
        target.profile_user = external_data.get('profile_user','')

        self.record_btn.configure(
        image=self.icon_record, command=lambda :self.change_frame_by_name(name='Record'))
        self.scheduler_btn.configure(state='normal',width=100, height=40)
        self.logs_btn.configure(state='normal',width=100, height=40)


    

    def create_record_file_content(self,data):
        dir_path = os.path.join(os.path.dirname(__file__),'My Record')
        exec_command = []
        with open('file_1.txt', 'r',encoding='utf-8') as f:
            exec_command = f.readlines()
        record_name = data['record_name']
        upload_timestamp = str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))
        modified_timestamp='xxxx-xx-xx xx:xx'
        folder_located = str(uuid4())
        folder_path = os.path.join(dir_path,folder_located) 
        os.mkdir(folder_path)
 
        record_detail={

            'record_name':record_name,
            'folder_located':folder_located,
            'description':data['description'],
            'upload_timestamp':upload_timestamp,
            'modified_timestamp':modified_timestamp,
            'profile_user':data['profile_user'],
            'exec_command':exec_command,

        }

        desc = {'record_detail':record_detail}
       
        with open(os.path.join(folder_path,'record.json'), "w",encoding='utf-8') as outfile:
            json.dump(desc, outfile,indent=4)

            
        with open(os.path.join(dir_path,'located_detail.json'),'r+',encoding='utf-8') as jsonfile:
            located_detail=json.load(jsonfile)
            jsonfile.truncate(0)
            jsonfile.seek(0)
            new_located_detail = {
                folder_located:record_name
            }
            located_detail.update(new_located_detail)
            json.dump(located_detail, jsonfile, indent = 4)

        return desc

    def save_record_from_child(self,data={}):
        library_target = self.Side_Bar.sidebar_handle['library']
        desc = self.create_record_file_content(data=data)
        self.reset_library()
        self.Scheduler.reset()
        self.change_frame_by_name(name='Scheduler')
        library_target.insert_record_child(desc=desc,is_click=True)
        self.Record.reset()



    def record_event(self):
        self.Record.reset()
        self.threading_activate(target=self.Record.start_record,name = 'start_record')
        target = self.Side_Bar.sidebar_handle['record']
        target.change_mode('record')

        self.record_btn.configure(
            image=self.icon_stop_record, command=lambda target=self.Record.stop_record_event:self.threading_activate(target=target,name = 'stop_record'))
   

    def threading_activate(self,target,args=(),name=''):
        if not name:
            name = uuid4()
        self.thread_handle[name] = threading.Thread(target=target,args=args)

        self.thread_handle[name].daemon = True
        self.thread_handle[name].start()

