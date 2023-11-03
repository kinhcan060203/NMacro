import os
import json
import customtkinter
from PIL import Image
from time import sleep
import tkinter.messagebox
from tkinter import *
from PIL import Image
import schedule
from tracking.execution import Execution
from datetime import datetime
from more_detail_subwindow import More_Detail_Subwindow
from treeView import TreeView
from edit_window import Edit_Schedule
from config import *




class Logs(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Logs, self).__init__(master=master)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color='white',corner_radius=0)

        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
        
        self.master=master

        self.progress_frame = customtkinter.CTkFrame(self,fg_color='#33CCFF',corner_radius=50,
                                                     background_corner_colors=['#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF'])
        self.progress_bar= customtkinter.CTkProgressBar(self.progress_frame,height=20,progress_color='#00FF00',fg_color='#DDDDDD')
        self.label_current_progress = customtkinter.CTkLabel(self.progress_frame, text="0%",font=('Helvetica',16,'bold'),fg_color='#33CCFF')
        self.progress_frame.grid_columnconfigure(0,weight=1)
        self.progress_frame.grid_rowconfigure(0,weight=1)   
        self.progress_bar.grid(column=0,row=0,sticky='ew',padx=10,pady=1)  
        self.label_current_progress.grid(column=1,row=0,padx=(0,10),pady=2)

        self.TreeView_handles = {}
        self.schedule_info = {}
        self.current_detail_show=''
        self.edit_window = Edit_Schedule(self)
        self.more_detail_subwindow = More_Detail_Subwindow(self)

        self.TreeView_handles['edit_window'] = self.edit_window
        self.add_treeView(exec_command=[],treeView_name='root',status_list=[])
        self.show_eventsTreeview('root')


    def show_detail(self,data):
        schedule_name = data['schedule_detail']['schedule_name']
        self.current_detail_show = schedule_name
        self.more_detail_subwindow.upload_detail(data)
        self.more_detail_subwindow.grid(row=1, column=0, sticky="nsew",pady=0)
        
    def hidden_detail(self):
        self.current_detail_show=''
        self.more_detail_subwindow.grid_forget()

    def show_eventsTreeview(self,treeView_name):
        treeView = ''

        for name in self.TreeView_handles:
            if name == treeView_name:
                self.TreeView_handles[name].grid(row=0, column=0, sticky="nsew")
                treeView = self.TreeView_handles[name]
            else:
                self.TreeView_handles[name].grid_forget()

        return treeView

    def add_treeView(self, exec_command,treeView_name,status_list):
        treeView = TreeView(self)
        self.TreeView_handles[treeView_name]=treeView
        self.prepare_events_and_insert(exec_command,treeView_name,status_list)
        return treeView
    
    def exchange_schedule(self,new_schedule_name, previous_schedule_name):
        if previous_schedule_name in self.TreeView_handles:
            self.TreeView_handles[new_schedule_name] = self.TreeView_handles[previous_schedule_name]
            self.TreeView_handles[new_schedule_name+'.log'] = self.TreeView_handles[previous_schedule_name+'.log']

        if previous_schedule_name != new_schedule_name:
            self.TreeView_handles.pop(previous_schedule_name)
            self.TreeView_handles.pop(previous_schedule_name+'.log')


    def prepare_events_and_insert(self,exec_command,treeView_name,status_list):
        if exec_command:
            iid=0
            treeView=self.TreeView_handles[treeView_name]
            tab_bar_list = []
            for event in exec_command:
                event = event.strip()
                if event in ['start','end']:
                    continue
                try:

                    current_window_handle,url,action = event.split('|')
                    action = json.loads('['+action.replace("'",'"')+']')[0]
   
                    if current_window_handle not in tab_bar_list:
                        tab_bar_list.append(current_window_handle)
                        treeView.insert_tab_treeView(current_window_handle=current_window_handle)

                except Exception as e:

                    current_window_handle = event.split()[1]
                    tab_bar_list.append(current_window_handle)
                    treeView.insert_tab_treeView(current_window_handle=current_window_handle)
                    action = {'TEXT':f'Mở tab thứ {current_window_handle}'}

                iid+=1

                fg_color_childView=treeView.hex_color_handles[current_window_handle]
                status = status_list[iid]
                treeView.insert_childView(iid,text=action['TEXT'],status=status,fg_color_childView=fg_color_childView)

    def run_schedule(self,data):

        execute_timestamp = data['execute_timestamp']
        is_scheduled=data['is_scheduled']
        self.progress_bar.set(0)
        self.label_current_progress.configure(text='0%')
        self.progress_frame.place(relx=0.5,rely=1,anchor='center',y=-20,relwidth=0.95)
        if is_scheduled=='yes':
            schedule.every().day.at(execute_timestamp.split()[-1]).do(lambda :self.run_script(data=data))
            # while True:
            #     schedule.run_pending()
            #     sleep(1)
        else:
            self.run_script(data=data)


    def run_script(self,data):

        dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')

        schedule_name = data['schedule_name']
        profile_user = data['profile_user']
        exec_command = data['exec_command']
        treeView=self.TreeView_handles[schedule_name]
        spacing = data['spacing']*60
        runtime = data['runtime']
        folder_located = data['folder_located']
        log_path = os.path.join(dir_path,folder_located,'logs.txt')
        json_path = os.path.join(dir_path,folder_located,'schedule.json')
        child_treeView = treeView.children_handles
        run_function = Execution(profile_user)
        progress_step  = 1/(runtime*(len(exec_command)-2))
        current_progress=0
        self.stop_running=False
        param = {'runtime':0}
        final_state='Completed'

        for j in range(len(data['logs_status'])):
            data['logs_status'][f'Log {j+1}'] = 'Waiting'
        data['status'] = 'Waiting'
        self.master.update_detail_event(data={'schedule_detail':data})

        for i in range(runtime):
            iid = 0
            param['runtime']+=1
            self.master.set_external_param_event(schedule_name,param)

            data['logs_status'][f'Log {i+1}'] = 'Running'
            data['status'] = 'Running'
            self.master.update_detail_event(data={'schedule_detail':data})

            with open(log_path,'a',encoding='utf-8') as log_file:

                for command in exec_command:
                    time = datetime.now()
                    try:
                        try:
                            childView, status_content = child_treeView[iid]
                            childView.configure(border_color='green')
                            status_content.configure(text='Processing',fg_color = status_fg_color['Processing'])
                        except Exception as e:
                            pass
                        if self.stop_running:
                            run_function.execute_cmd('end')
                            return 
                        run_function.execute_cmd(command.strip(),time_sleep=0)
                        log = f'#{i+1}|{time}|{command.strip()}|Completed\n'
                        log_file.write(log)


                        if command.strip() not in ['end','start']:
                
                            current_progress+=progress_step
                            self.progress_bar.set(current_progress)
                            self.label_current_progress.configure(text=f'{round(current_progress*100)}%')
           
                        try:
                            childView, status_content = child_treeView[iid]
                            childView.configure(border_color='white')
                            status_content.configure(text='Completed',fg_color = status_fg_color['Completed'])
                        except Exception as e:
                            pass    

                    except Exception as e:
                        log = f'#{i+1}|{time}|{command.strip()}|Error\n'
                        log_file.write(log)

                        try:
                            childView, status_content = child_treeView[iid]
                            childView.configure(border_color='white')
                            status_content.configure(text='Error',fg_color = status_fg_color['Error'])
                        except Exception as e:
                                pass
                        final_state = 'Error'
                    iid+=1

                log_file.write('\n')


            if i+1 != runtime:
                for childView,status_content in child_treeView.values():
                    status_content.configure(text='Waiting',fg_color = status_fg_color['Waiting'])
                data['logs_status'][f'Log {i+1}'] = 'Completed'
                data['status'] = 'Waiting'
                self.master.update_detail_event(data={'schedule_detail':data})
                sleep(spacing)

                
        self.progress_frame.place_forget()
        data['logs_status'][f'Log {i+1}'] = final_state
        data['status'] = final_state
        data['finished_timestamp'] = str(datetime.now().strftime(r'%Y-%m-%d %H:%M'))

        self.master.update_detail_event(data={'schedule_detail':data})

        return schedule.CancelJob
        

    def reset(self):  
        self.show_eventsTreeview('root')
        self.tab_bar_list={}
        self.tabTreeView={}
