import os
import json
import customtkinter
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from PIL import Image
from datetime import datetime
from schedule_parameter import Schedule_Parameter

def check_exist_name(dir_path,name,except_name=''):
    with open(os.path.join(dir_path,'located_detail.json'),'r',encoding='utf-8') as jsonfile:
        located_detail=json.load(jsonfile)
        if name in located_detail.values() and name!=except_name:
            return True
        return False
    

class Edit_Info_Window(customtkinter.CTkFrame):
    def __init__(self, master, mode):

        super(Edit_Info_Window, self).__init__(master=master)
        self.configure(corner_radius=5,fg_color='transparent')
    
        self.mode = mode
        label_title = 'Schedule name' if mode =='schedule' else 'Record name'
        label_noteBox = 'Note' if mode =='schedule' else 'Description'
       
        self.label_title = customtkinter.CTkLabel(self, text=label_title,justify="left",anchor='w',width=100)
        self.label_title.grid(row=0, column=0,
                           padx=12, pady=10,
                           sticky="nw")
        self.grid_columnconfigure(1,weight=1)
        
        self.title_var = customtkinter.StringVar(value='')
        self.entry_title = customtkinter.CTkEntry(self,textvariable=self.title_var)

        self.entry_title.bind('<FocusIn>',lambda e:self.focus_in(self.entry_title))
        self.entry_title.bind('<FocusOut>',lambda e:self.focus_out(self.entry_title))

        self.entry_title.grid(row=0, column=1,columnspan=3,
                            padx=12,pady=10, 
                            sticky="ew")
        
        
        self.label_noteBox = customtkinter.CTkLabel(self,
                                        text=label_noteBox)
        self.label_noteBox.grid(row=1, column=0,
                              padx=12, pady=5,
                              sticky="ws")
        self.noteBox = customtkinter.CTkTextbox(self,border_width=2,border_color='#CCCCCC',
                                         height=100)
        self.noteBox.grid(row=2, column=0,
                             columnspan=3, padx=12,
                             pady=(0,10), sticky="nsew")
        
        self.noteBox.bind('<FocusIn>',lambda e:self.focus_in(self.noteBox))
        self.noteBox.bind('<FocusOut>',lambda e:self.focus_out(self.noteBox))




        
    def focus_in(self,widget):
        widget.configure(border_color="#555555")
    def focus_out(self,widget):
        widget.configure(border_color="#EEEEEE")
    def get_info(self):
        if self.mode == 'record':
            return {
                'record_name':self.title_var.get(),
                'description':self.noteBox.get('0.0','end')
            }
        else:
            return {
                'schedule_name':self.title_var.get(),
                'note':self.noteBox.get('0.0','end')
            }
    def upload_info(self,info):
        if self.mode=='schedule':
            schedule_name = info.get('schedule_name','')
            note = info.get('note','')
            self.title_var.set(schedule_name)
            self.noteBox.delete('0.0','end')
            self.noteBox.insert('0.0',note)
        if self.mode=='record':
            record_name = info.get('record_name','')
            description = info.get('description','')
            self.title_var.set(record_name)
            self.noteBox.delete('0.0','end')
            self.noteBox.insert('0.0',description)

class Edit_Record(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Edit_Record, self).__init__(master=master)
        self.configure(corner_radius=3,fg_color='#DDDDDD',border_color='#555555',border_width=2)
        self.grid_columnconfigure(0,weight=1)
        
        self.record_info={}

        self.label_edit_schedule = customtkinter.CTkLabel(self, text="Edit Record",justify="center",anchor='center',font=('Helvetica',24,'bold'),text_color='#33CCFF')
        self.label_edit_schedule.grid(row=0, column=0,
                           padx=15, pady=10,
                           sticky="ew")
        
        self.edit_window = Edit_Info_Window(self,mode='record')
        self.edit_window.grid(row=3, column=0,
                           padx=8,pady=6,
                           sticky="nsew")

        self.save_btn = customtkinter.CTkButton(
            master=self,  corner_radius=10, width=80, height=50, text='Save',border_color='black',border_width=2,
            fg_color='gray75', hover_color=("gray70", "gray30"),border_spacing=10,font=('Helvetica',16,'bold'),text_color='black',
            anchor="center",command=self.edit_record)
        self.save_btn.place(relx=1,rely=1,y=-10,x=-8,anchor='se')
        
    def edit_record(self):
        dir_path = os.path.join(os.path.dirname(__file__),'My Record')

        info=self.edit_window.get_info()
        pre_record_name = self.record_info['record_name']
        record_name = info['record_name']
        is_exist=check_exist_name(dir_path,record_name,pre_record_name)
        if is_exist:
            tkinter.messagebox.showwarning(title='Edit Record',message='Record name already exist. Please use another name')
            return 

        self.save_btn.configure(fg_color='#CC00CC',text_color='white',hover_color='#CC00CC',state='disabled')
        res = tkinter.messagebox.askyesno("Edit", "Are you sure to edit this record ?")
        if not res:
            self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')
            return
        self.record_info['modified_timestamp'] = str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))
        self.record_info.update(info)
        self.master.master.edit_record_event(new_record_detail=self.record_info,pre_record_name = pre_record_name)
        self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')

    def upload_info(self,info):
        self.record_info = info
        self.edit_window.upload_info(info)



class Edit_Schedule(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Edit_Schedule, self).__init__(master=master)
        self.master=master
        self.configure(corner_radius=3,fg_color='#DDDDDD',border_color='#555555',border_width=2)
        self.grid_columnconfigure(0,weight=1)


        self.schedule_info = {}
        self.label_edit_schedule = customtkinter.CTkLabel(self, text="Edit Shedule",justify="center",anchor='center',font=('Helvetica',24,'bold'),text_color='#33CCFF')
        self.label_edit_schedule.grid(row=0, column=0,
                           padx=15, pady=10,
                           sticky="ew")

        
        self.Edit_Info_Window=Edit_Info_Window(self,mode='schedule')

        self.Edit_Info_Window.grid(row=3, column=0,
                           padx=8,pady=6,
                           sticky="nsew")
        
        self.change_param_var = tk.StringVar(value='off')

        self.is_change_param = customtkinter.CTkCheckBox(self,
                                     text="You want to modify schedule param?",
                                     variable=self.change_param_var,command=lambda :self.show_schedule_param(),
                                     onvalue="on", offvalue="off")
        

        self.is_change_param.grid(row=8, column=0,columnspan=3,pady=5,padx=8,
                           sticky="ew")
        self.Schedule_Parameter = Schedule_Parameter(self)
        self.Schedule_Parameter.configure(fg_color='#DDDDDD',corner_radius=5)
        


        self.save_btn = customtkinter.CTkButton(
            master=self,  corner_radius=10, width=80, height=50, text='Save',border_color='black',border_width=2,
            fg_color='gray75', hover_color=("gray70", "gray30"),border_spacing=10,font=('Helvetica',16,'bold'),text_color='black',
            anchor="center",command=self.edit_schedule)
        self.save_btn.place(relx=1,rely=1,y=-10,x=-8,anchor='se')

    

    def show_schedule_param(self):
        if self.change_param_var.get()=='on':
            data = self.Edit_Info_Window.get_info()
            self.Edit_Info_Window.grid_forget()

            self.Schedule_Parameter.grid(row=3, column=0,
                           padx=8,pady=6,
                           sticky="nsew")
            self.Schedule_Parameter.upload_info(data)

        else:
            data = self.Schedule_Parameter.get_info()
            self.Schedule_Parameter.grid_forget()
            self.Edit_Info_Window.grid(row=3, column=0,
                           padx=8,pady=6,
                           sticky="nsew")
            self.Edit_Info_Window.upload_info(data)


    def edit_schedule(self):
        pre_schedule_name = self.schedule_info['schedule_name']
        self.save_btn.configure(fg_color='#CC00CC',text_color='white',hover_color='#CC00CC',state='disabled')
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        res = tkinter.messagebox.askyesno("Edit", "Are you sure to edit this schedule ?")

        self.schedule_info['modified_timestamp'] = str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))
        
        if self.change_param_var.get()=='on':
            param = self.Schedule_Parameter.get_all_param(schedule_name=pre_schedule_name)
            if not param:
                self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')
                return

            self.schedule_info.update(param)
            self.schedule_info['finished_timestamp'] = 'xxxx-xx-xx xx:xx'
            if not res:
                self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')
                return
            self.master.master.edit_schedule_event(new_schedule_detail=self.schedule_info,pre_schedule_name = pre_schedule_name,execute_modified=True)
      
        else:
            info = self.Edit_Info_Window.get_info()
            schedule_name = self.schedule_info['schedule_name']
            check_exist_name(dir_path,schedule_name,pre_schedule_name)
            self.schedule_info.update(info)
            if not res:
                self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')
                return
            self.master.master.edit_schedule_event(new_schedule_detail=self.schedule_info,pre_schedule_name = pre_schedule_name,execute_modified=False)
        self.save_btn.configure(fg_color='gray75',text_color='black',hover_color='grey70',state='normal')

    def upload_schedule_param(self,data):
        self.schedule_info = data
        self.change_param_var.set('off')
        self.show_schedule_param()
        self.Schedule_Parameter.upload_param(data)
        self.Edit_Info_Window.upload_info(data)


