import os
import customtkinter
from time import sleep
from tkinter import *
from PIL import Image
from config import *

class More_Detail_Subwindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super(More_Detail_Subwindow, self).__init__(master=master)
        self.configure(border_width=2,border_color='#555555',corner_radius=0)

        self.master = master
        self.label_frame = customtkinter.CTkLabel(self, text="Detail",justify="center",anchor='center',font=('Helvetica',24,'bold'),text_color='#33CCFF')
        self.label_frame.grid(row=0, column=0,columnspan=3,
                           padx=5, pady=10,
                           sticky="ew")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)



        self.Left_Frame = customtkinter.CTkScrollableFrame(self,fg_color='transparent',corner_radius=2,border_width=1,border_color='#999999')
        self.Left_Frame.grid_columnconfigure(0,weight=1)
        self.Left_Frame.grid(row=1, column=0,
                           padx=12, pady=(0,5),
                           sticky="nsew")
        
        self.boundary = customtkinter.CTkFrame(self,width=4,border_color='black',fg_color='#0099FF',corner_radius=50,border_width=0)


        self.Right_Frame = customtkinter.CTkScrollableFrame(self,fg_color='transparent',corner_radius=2,border_width=1,border_color='#999999')
        self.Right_Frame.grid_columnconfigure(0,weight=1)

        self.init_left_frame()
        self.init_right_frame()

    def focus_in(self,widget):
        widget.configure(border_color="#555555")
    def focus_out(self,widget):
        widget.configure(border_color="#EEEEEE")
    def modified_schedule_info(self,info):
        title = info['schedule_name']
        note = info['note']
        modified_time = info['modified_time']

        self.title_content.configure(text=title)
        self.modified_time_content.configure(text=modified_time)
        self.note_content.configure(state='normal')
        self.note_content.delete('0.0','end')
        self.note_content.insert('0.0',note)
        self.note_content.configure(state='disabled')

    def upload_detail(self,data):
        schedule_detail = data.get('schedule_detail',{})
        record_detail = data.get('record_detail',{})
        title = ''
        upload_time = ''
        modified_time = ''
        note = ''
        if schedule_detail:
            title = schedule_detail['schedule_name']
            upload_time = schedule_detail['upload_timestamp']
            modified_time = schedule_detail['modified_timestamp']
            finished_time = schedule_detail['finished_timestamp']
            folder_located = schedule_detail['folder_located']
            self.exec_command = schedule_detail['exec_command']
            note = schedule_detail['note']
            status = schedule_detail['status']

            dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
            with open(os.path.join(dir_path,folder_located,'logs.txt'),'r',encoding='utf-8') as f:
                self.log_text = f.read().split('\n\n')

     
            status_color = status_color_list[status]
            self.status_content.configure(text=status,text_color=status_color)
            self.start_run_content.configure(text=schedule_detail['execute_timestamp'])
            self.space_time_content.configure(text=f'{schedule_detail["spacing"]} (minutes)')
            self.finished_time_content.configure(text=finished_time)
            self.modified_time_content.configure(text=modified_time)
            self.title_content.configure(text=title)

            self.update_history_logs(schedule_detail)
            self.update_error_logs(schedule_detail)
            self.show_history_logs()
            


            self.setup_schedule_view()

        elif record_detail:
            title = record_detail['record_name']
            upload_time = record_detail['upload_timestamp']
            note = record_detail['description']
            modified_time = record_detail['modified_timestamp']
            self.title_content.configure(text=title)


        self.upload_time_content.configure(text=upload_time)
        self.modified_time_content.configure(text=modified_time)
        self.note_content.configure(state='normal')
        self.note_content.delete('0.0','end')
        self.note_content.insert('0.0',note)
        self.note_content.configure(state='disabled')

    def update_history_logs(self,schedule_detail):
        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        logs_status = schedule_detail['logs_status']
        values =[]
        executed_log=0
        for log,status in logs_status.items():
            if status in ['Completed','Error']:
                values.append(log)
            if status =='Running':
                values.append('Is Running')
            if status =='Completed':
                executed_log +=1

        if schedule_detail['status'] in ['Completed','Error']:
            self.history_logs_var.set(values[-1])
        
        self.completed_log_content.configure(text=f'{executed_log}/{len(logs_status)}')
        self.comboBox_history_logs.configure(values=values)

    def update_error_logs(self,schedule_detail):
        logs_status = schedule_detail['logs_status']
        values = []
        for log,status in logs_status.items():
            if status =='Error':
                values.append(log)
        
        self.comboBox_error_logs.configure(values=values)


    def setup_schedule_view(self):
        self.grid_columnconfigure(2,weight=1)

        self.boundary.grid(row=1, column=1,pady=(5,10),
                        sticky="ns")
        self.Right_Frame.grid(row=1, column=2,
                    padx=(0,12), pady=(0,5),
                    sticky="nsew")
        
        self.Left_Frame.grid(row=1, column=0,
                    padx=(12,0), pady=(0,5),
                    sticky="nsew")
    def init_right_frame(self):
        self.status_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.label_status = customtkinter.CTkLabel(self.status_block,fg_color='transparent',text_color=config['text_color'], text='Status', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        
        self.label_status.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.status_content = customtkinter.CTkLabel(self.status_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='right',anchor='e')
        self.status_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)


        self.start_run_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.label_start_run = customtkinter.CTkLabel(self.start_run_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Start at', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_start_run.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.start_run_content = customtkinter.CTkLabel(self.start_run_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.start_run_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)

        self.space_time_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.label_space_time = customtkinter.CTkLabel(self.space_time_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Space time', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_space_time.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.space_time_content = customtkinter.CTkLabel(self.space_time_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.space_time_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)

        self.finished_time_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.label_finished_time = customtkinter.CTkLabel(self.finished_time_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Finished at', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                justify='left',anchor='w')
        self.label_finished_time.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.finished_time_content = customtkinter.CTkLabel(self.finished_time_block,fg_color='transparent',text_color=config['text_color'], text='2024-8-50 19:09', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                justify='right',anchor='e')
        self.finished_time_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)

        self.history_logs_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.history_logs_var = customtkinter.StringVar(value="Is Running") 

        
        self.label_history_logs = customtkinter.CTkLabel(self.history_logs_block, width=80,fg_color='transparent',text_color=config['text_color'], text='History Logs', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_history_logs.grid(row=0, column=0, sticky="w",pady=3,padx=8)

        self.comboBox_history_logs = customtkinter.CTkComboBox(master=self.history_logs_block,
                                            values=[],
                                            command=self.show_history_logs,
                                            variable=self.history_logs_var)
        self.comboBox_history_logs.grid(row=0, column=1, sticky="e",pady=3,padx=8)


        self.error_logs_block = customtkinter.CTkFrame(self.Right_Frame,fg_color='transparent',corner_radius=0)
        self.error_logs_var = customtkinter.StringVar(value="") 

        
        self.label_error_logs = customtkinter.CTkLabel(self.error_logs_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Error Logs', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_error_logs.grid(row=0, column=0, sticky="w",pady=3,padx=8)

        self.comboBox_error_logs = customtkinter.CTkComboBox(master=self.error_logs_block,
                                            values=[],
                                            command=self.show_history_logs,
                                            variable=self.error_logs_var)
        self.comboBox_error_logs.grid(row=0, column=1, sticky="e",pady=3,padx=8)



        self.status_block.grid(row=2, column=0,
                           padx=2, pady=1,
                           sticky="ew")
 
        self.start_run_block.grid(row=4, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.space_time_block.grid(row=5, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.finished_time_block.grid(row=6, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.history_logs_block.grid(row=8, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.error_logs_block.grid(row=10, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        
        self.status_block.grid_columnconfigure(1,weight=1)
        self.start_run_block.grid_columnconfigure(1,weight=1)
        self.finished_time_block.grid_columnconfigure(1,weight=1)
        self.space_time_block.grid_columnconfigure(1,weight=1)
        self.history_logs_block.grid_columnconfigure(1,weight=1)
        self.error_logs_block.grid_columnconfigure(1,weight=1)


    def show_error_logs(self,choice):
        self.history_logs_var.set(choice)
        if choice in self.comboBox_error_logs.cget('values'):
            self.error_logs_var.set(choice)
        else:
            self.error_logs_var.set('')

    def show_history_logs(self,choice=None):

        exec_command = self.exec_command
        treeView_list_name = self.comboBox_history_logs.cget('values')
        if not choice and treeView_list_name:
            choice = treeView_list_name[-1]
        log_value = treeView_list_name.index(choice)
        self.show_error_logs(choice)
        if log_value == len(treeView_list_name)-1:
            treeView_name = self.title_content.cget('text')
            treeView=self.master.show_eventsTreeview(treeView_name)
        else:
            log_text=self.log_text[log_value].split("\n")
            treeView_name = self.title_content.cget('text')+'.log'
            treeView=self.master.show_eventsTreeview(treeView_name)
            child_treeView = treeView.children_handles
            for iid in range(1,len(exec_command)-1):
                childView, status_content = child_treeView[iid]
                status=log_text[iid].split('|')[-1]
                if not status:
                    status = 'Not yet'
                status_content.configure(text=status,fg_color = status_fg_color[status])


    def init_left_frame(self):

        self.title_block = customtkinter.CTkFrame(self.Left_Frame,fg_color='transparent',corner_radius=0)
        self.label_title = customtkinter.CTkLabel(self.title_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Title', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_title.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.title_content = customtkinter.CTkLabel(self.title_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.title_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)


        self.upload_time_block = customtkinter.CTkFrame(self.Left_Frame,fg_color='transparent',corner_radius=0)
        self.label_upload_time = customtkinter.CTkLabel(self.upload_time_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Upload at', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_upload_time.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.upload_time_content = customtkinter.CTkLabel(self.upload_time_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.upload_time_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)


        self.modified_time_block = customtkinter.CTkFrame(self.Left_Frame,fg_color='transparent',corner_radius=0)
        self.label_modified_time = customtkinter.CTkLabel(self.modified_time_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Modified at', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_modified_time.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.modified_time_content = customtkinter.CTkLabel(self.modified_time_block,fg_color='transparent',text_color=config['text_color'], text='2023-8-50 19:09', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.modified_time_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)

        self.completed_log_block = customtkinter.CTkFrame(self.Left_Frame,fg_color='transparent',corner_radius=0)

        self.label_completed_log = customtkinter.CTkLabel(self.completed_log_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Completed:', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_completed_log.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.completed_log_content = customtkinter.CTkLabel(self.completed_log_block,fg_color='transparent',text_color=config['text_color'], text='', font=customtkinter.CTkFont(size=12, weight="normal"),
                                                  justify='right',anchor='e')
        self.completed_log_content.grid(row=0, column=1, sticky="e",pady=3,padx=8)


        self.note_block = customtkinter.CTkFrame(self.Left_Frame,fg_color='transparent',corner_radius=0)
        self.label_note = customtkinter.CTkLabel(self.note_block, width=80,fg_color='transparent',text_color=config['text_color'], text='Note', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_note.grid(row=0, column=0, sticky="w",pady=3,padx=8)
        self.note_content = customtkinter.CTkTextbox(self.note_block,border_width=2,border_color='#CCCCCC',state='disabled',
                                         height=100)
        self.note_content.grid(row=1, column=0, sticky="snew",pady=(0,3),padx=8)

        self.note_content.bind('<FocusIn>',lambda e:self.focus_in(self.note_content))
        self.note_content.bind('<FocusOut>',lambda e:self.focus_out(self.note_content))



        self.title_block.grid(row=2, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.upload_time_block.grid(row=4, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.modified_time_block.grid(row=6, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        self.completed_log_block.grid(row=7, column=0,
                           padx=2, pady=1,
                           sticky="ew")
        
        self.note_block.grid(row=8, column=0,
                           padx=2, pady=1,
                           sticky="ew")


        self.title_block.grid_columnconfigure(1,weight=1)
        self.upload_time_block.grid_columnconfigure(1,weight=1)
        self.modified_time_block.grid_columnconfigure(1,weight=1)
        self.completed_log_block.grid_columnconfigure(0,weight=1)
        self.note_block.grid_columnconfigure(0,weight=1)
