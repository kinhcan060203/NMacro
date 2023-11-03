import customtkinter
from PIL import Image
import tkinter as tk
import tkinter
from datetime import datetime
import os
import json
from config import *

def check_exist_name(dir_path,name,except_name=''):
    with open(os.path.join(dir_path,'located_detail.json'),'r',encoding='utf-8') as jsonfile:
        located_detail=json.load(jsonfile)

        if name in located_detail.values() and name!=except_name:
            return True
        return False

class Schedule_Parameter(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Schedule_Parameter, self).__init__(master=master)

        
        self.grid_columnconfigure((1,2,3),weight=1)
        self.configure(corner_radius=0,fg_color='transparent')
        self.master=master


        self.label_schedule_name = customtkinter.CTkLabel(self, text="Schedule name",justify="left",anchor='w',width=100)
        self.label_schedule_name.grid(row=1, column=0,
                           padx=12, pady=10,
                           sticky="nw")
        
        self.schedule_name_var = customtkinter.StringVar(value='')
        self.entry_schedule_name = customtkinter.CTkEntry(self,textvariable=self.schedule_name_var)

        self.entry_schedule_name.bind('<FocusIn>',lambda e:self.focus_in(self.entry_schedule_name))
        self.entry_schedule_name.bind('<FocusOut>',lambda e:self.focus_out(self.entry_schedule_name))

        self.entry_schedule_name.grid(row=1, column=1,columnspan=3,
                            padx=12,pady=10, 
                            sticky="ew")


        self.label_runtime = customtkinter.CTkLabel(self,
                                  text="Run time")
        
        self.label_runtime.grid(row=4, column=0,
                              padx=12, pady=10,
                              sticky="w")
        self.runtime_block = customtkinter.CTkFrame(self,fg_color='transparent')

        self.label_run_loop_number = customtkinter.CTkLabel(self.runtime_block, text="(time)",width=40)

        
        self.label_run_loop_number.grid(row=0, column=1,
                                    padx=5, pady=5,
                                    sticky="w")
        
        self.runtime_block.grid(row=4, column=1,columnspan=2,
                                    padx=12, pady=5,
                                    sticky="w")
        self.entry_runtime = customtkinter.CTkOptionMenu(self.runtime_block,height=20,width=20, values=list(map(str,range(1,21))))
        self.entry_runtime.grid(row=0, column=0,padx=5, pady=5, sticky="w")
        

        self.label_space_time = customtkinter.CTkLabel(self, text="Spacing")
        self.label_space_time.grid(row=5, column=0,
                                    padx=12, pady=10,
                                    sticky="w")
        self.space_time_var = customtkinter.StringVar(value='0')
        self.space_time_block = customtkinter.CTkFrame(self,fg_color='transparent')
        self.entry_space_time = customtkinter.CTkEntry(self.space_time_block,textvariable=self.space_time_var,
                                                       width=80)
        self.label_minute = customtkinter.CTkLabel(self.space_time_block, text="(minute)",width=40)
        self.entry_space_time.grid(row=0, column=0,
                                    padx=5, pady=5,
                                    sticky="w")
        
        self.label_minute.grid(row=0, column=1,
                                    padx=5, pady=5,
                                    sticky="w")
        
        self.space_time_block.grid(row=5, column=1,columnspan=2,
                                    padx=12, pady=5,
                                    sticky="w")
        
        self.entry_space_time.bind('<FocusIn>',lambda e:self.focus_in(self.entry_space_time))
        self.entry_space_time.bind('<FocusOut>',lambda e:self.focus_out(self.entry_space_time))


        self.label_notify = customtkinter.CTkLabel(self, text="Notification")
        self.label_notify.grid(row=7, column=0,
                           padx=12, pady=10,
                           sticky="ws")
        
        self.notifyVar = tk.StringVar(value='None')
 
 
        self.CMSRadioButton = customtkinter.CTkRadioButton(self,width=130,
                                   text="CMS",
                                   variable=self.notifyVar,
                                         value="Phone")
        
        self.CMSRadioButton.grid(row=7, column=3,
                                  padx=12, pady=10,
                                  sticky="ew")
 
        self.EmailRadioButton = customtkinter.CTkRadioButton(self,width=130,
                                     text="Email",
                                     variable=self.notifyVar,
                                     value="Email")
        
        self.EmailRadioButton.grid(row=7, column=2,
                                    padx=12, pady=10,
                                    sticky="ew")
         
        self.noneRadioButton = customtkinter.CTkRadioButton(self,width=130,
                                    text="None",
                                    variable=self.notifyVar,
                                    value="None")
        self.noneRadioButton.grid(row=7, column=1, padx=12,
                                  pady=10, sticky="ew")
 
        
        self.is_schedule = tk.StringVar(value='no')

        self.no_schedule = customtkinter.CTkRadioButton(self,height=36,
                                     text="Run now",
                                     variable=self.is_schedule,
                                     value="no",command=lambda :self.setting_schedule(status=0))
        self.no_schedule.grid(row=9, column=0,
                                    padx=12, pady=10,
                                    sticky="ew")

        self.yes_schedule = customtkinter.CTkRadioButton(self,height=36,
                                     text="Schedule",
                                     variable=self.is_schedule,
                                     value="yes",command=lambda :self.setting_schedule(status=1))
        self.yes_schedule.grid(row=9, column=1,
                                    padx=12, pady=10,
                                    sticky="ew")

        self.label_noteBox = customtkinter.CTkLabel(self,
                                        text="Note")
        self.label_noteBox.grid(row=12, column=0,
                              padx=15, pady=(10,2),
                              sticky="ws")
        self.noteBox = customtkinter.CTkTextbox(self,border_width=2,border_color='#CCCCCC',
                                         height=100)
        self.noteBox.grid(row=13, column=0,
                             columnspan=4, padx=15,
                             pady=(0,10), sticky="nsew")
        
        self.noteBox.bind('<FocusIn>',lambda e:self.focus_in(self.noteBox))
        self.noteBox.bind('<FocusOut>',lambda e:self.focus_out(self.noteBox))

        self.time_setting = customtkinter.CTkFrame(self,fg_color='transparent')

        self.hour = customtkinter.CTkButton(self.time_setting,text="00H",width=36,fg_color='#FFFFFF',border_color='#CCCCCC',border_width=2,command=self.show_hour,
                                                text_color='black',hover_color='#FFFFFF')
        self.minute = customtkinter.CTkButton(self.time_setting,text="00M",width=36,fg_color='#FFFFFF',border_color='#CCCCCC',border_width=2,command=self.show_minute,
                                              text_color='black',hover_color='#FFFFFF')

        self.time_seperate = customtkinter.CTkLabel(self.time_setting, text=":",font=('Helvetica',16,'bold'))


        self.hour.grid(row=0, column=0)
        self.time_seperate.grid(row=0, column=1,padx=5)
        self.minute.grid(row=0, column=2)


        self.hour.bind('<FocusIn>',lambda e:self.focus_in(self.hour))
        self.hour.bind('<FocusOut>',lambda e:self.focus_out(self.hour))
        self.minute.bind('<FocusIn>',lambda e:self.focus_in(self.minute))
        self.minute.bind('<FocusOut>',lambda e:self.focus_out(self.minute))




   




        self.hour_slider = customtkinter.CTkScrollableFrame(self,height=1,width=30,corner_radius=5,fg_color='#EEEEEE')
        self.minute_slider = customtkinter.CTkScrollableFrame(self,height=0,width=35,corner_radius=5,fg_color='#EEEEEE')

        self.exec_command=''
        self.thread_handle={}
        self.init_frame()

    
    def check_time_valid(self,timestamp):
        try:
            timestamp_now = datetime.today()
            timestamp_schedule = datetime.strptime(timestamp,r"%Y-%m-%d %H:%M")
            if timestamp_schedule < timestamp_now:
                tkinter.messagebox.showwarning(title='Time setting',message='Time setting is not valid, please try again!')
                return False
        except Exception as e:
            tkinter.messagebox.showwarning(title='Time setting',message='Time setting is not valid, please try again!')
            return False
        return True
    
    def get_all_param(self,schedule_name=''):
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        schedule_name_var = self.schedule_name_var.get()
        is_exist =check_exist_name(dir_path,schedule_name_var,schedule_name)
        if is_exist:
            tkinter.messagebox.showwarning(title='Setting Schedule',message='Schedule name is exist, please set another name')

            self.entry_schedule_name.focus()
            return
        is_scheduled = self.is_schedule.get() 


        execute_timestamp = str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))
        runtime = int(self.entry_runtime.get())

        if is_scheduled=='no':
            status = 'Waiting'
            logs_status = {f'Log {i}':'Waiting' for i in range(1,runtime+1)}

        else:
            status = 'Scheduled'
            logs_status = {f'Log {i}':'Scheduled' for i in range(1,runtime+1)}

            try:
                hour = self.hour.cget('text')[:-1]
                minute = self.minute.cget('text')[:-1]
                date = self.entry_schedule.entry.get()
                date = datetime.strptime(date,r"%m/%d/%Y").strftime(r"%Y-%m-%d")
                execute_timestamp = f'{date} {hour}:{minute}'
            except Exception as e:
                pass
            is_valid = self.check_time_valid(execute_timestamp)
            if not is_valid:
                return  False

        note = self.noteBox.get('0.0','end')
        spacing = self.entry_space_time.get()
        notify_type = self.notifyVar.get()
        try:
            spacing=float(spacing)
        except ValueError:
            spacing = 0

        param = {
            'schedule_name':schedule_name_var,
            'is_scheduled':is_scheduled,
            'execute_timestamp':execute_timestamp,
            'spacing':spacing,
            'runtime':runtime,
            'logs_status':logs_status,
            'status':status,
            'notify_type':notify_type,
            'note':note,

        }

        return param
    
    def init_frame(self):
        self.bind('<Button 1>',self.click_background)

        for hour in range(24):
            text=f'{str(hour).zfill(2)}'
            hour_btn = customtkinter.CTkButton(hover_color='#DDDDDD',text_color='black',
            master=self.hour_slider,  corner_radius=10,width=30, height=10, text=text,fg_color='#CCCCCC',command=lambda text=text:self.update_hour(text))
            hour_btn.grid(row=hour, column=0,sticky='ew',padx=2,pady=2)
            hour_btn.bind('<Button 1>',self.click_background)

        for minute in range(60):
            text=f'{str(minute).zfill(2)}'
            minute_btn = customtkinter.CTkButton(hover_color='#DDDDDD',text_color='black',
            master=self.minute_slider,  corner_radius=10,width=30, height=10, text=text,fg_color='#CCCCCC',command=lambda text=text:self.update_minute(text))
            minute_btn.grid(row=minute, column=0,sticky='ew',padx=2,pady=2)
            minute_btn.bind('<Button 1>',self.click_background)

        for wid in self.winfo_children():
            if not isinstance(wid,customtkinter.CTkSlider):
                wid.bind('<Button 1>',self.click_background)

    def click_background(self,e):
        self.hour_slider.place_forget()
        self.minute_slider.place_forget()
    def update_hour(self,hour):
        self.hour.configure(text=f'{hour}H')

    def update_minute(self,minute):
        self.minute.configure(text=f'{minute}M')
    def show_hour(self):
        x = self.time_setting.winfo_x()
        width = self.time_setting.winfo_width()
        y = self.time_setting.winfo_y()
        self.minute_slider.place_forget()

        self.hour_slider.place(x=x-width*0.5,y=y-10,anchor='n')

    def show_minute(self):
        x = self.time_setting.winfo_x()
        width = self.time_setting.winfo_width()
        y = self.time_setting.winfo_y()
        self.hour_slider.place_forget()
        self.minute_slider.place(x=x-width*0.5+50,y=y-10,anchor='n')

    def setting_schedule(self,status,timestamp=None):

        timestamp = timestamp if timestamp else datetime.today()
        _ , hour_and_minute = str(timestamp).split()
        hour,minute = hour_and_minute.split(':')[:2]
        if status:
        
            self.hour.configure(text=f'{hour}H')
            self.minute.configure(text=f'{minute}M')
       
            self.time_setting.grid(row=9, column=3, padx=12,
                            pady=10, sticky="ew")
            
            import ttkbootstrap as tb
            try:
                self.entry_schedule.grid_forget()
            except Exception as e:
                pass
            self.entry_schedule = tb.DateEntry(self, bootstyle="light", firstweekday=0,startdate=timestamp)

            self.entry_schedule.grid(row=9, column=2, padx=12,
                            pady=10, sticky="ew")
        else:
            try:
                self.time_setting.grid_forget()
            except Exception as e:
                pass
            try:
                self.entry_schedule.grid_forget()
            except Exception as e:
                pass
    def focus_in(self,widget):
        widget.configure(border_color="#555555")
    def focus_out(self,widget):
        widget.configure(border_color="#EEEEEE")

    def reset(self):
        self.click_background(0)
        self.setting_schedule(0)
        self.schedule_name_var.set('')
        self.noteBox.delete('0.0','end')
        self.is_schedule.set('no')
        self.entry_runtime.set(1)
        self.notifyVar.set('None')
        self.space_time_var.set('0.0')


    def get_info(self):
        schedule_name=self.schedule_name_var.get()
        note=self.noteBox.get('0.0','end')
        data = {
            'schedule_name':schedule_name,
            'note':note

        }
        return data
    
    def upload_info(self,data):
        note=data['note']
        schedule_name_var=data['schedule_name']
        self.schedule_name_var.set(schedule_name_var)
        self.noteBox.delete('0.0','end')
        self.noteBox.insert('0.0',note)

    def upload_param(self,data):
        is_scheduled=data['is_scheduled']
        execute_timestamp=data['execute_timestamp']
        date, hour_and_minute = execute_timestamp.split()
        hour, minute = hour_and_minute.split(':')
        notify_type=data['notify_type']
        spacing=data['spacing']
        runtime=data['runtime']
        profile_user=data['profile_user']

        self.entry_runtime.set(runtime)
        self.space_time_var.set(spacing)
        self.notifyVar.set(notify_type)
        self.is_schedule.set(is_scheduled)


        if is_scheduled=='yes':
            timestamp = datetime.strptime(execute_timestamp, '%Y-%m-%d %H:%M')
            self.setting_schedule(1,timestamp=timestamp)
            self.hour.configure(text=f'{hour}H')
            self.minute.configure(text=f'{minute}M')
            self.yes_schedule.configure(command=lambda: self.setting_schedule(1,timestamp=timestamp))
        else:
            self.yes_schedule.configure(command=lambda: self.setting_schedule(1))




