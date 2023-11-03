import os
import threading
import customtkinter
from PIL import Image
from time import sleep
from uuid import uuid4
import tkinter.messagebox
from tracking.execution import Execution
from tkinter import *
from PIL import Image, ImageTk
from selenium.webdriver.common.by import By



class Tab_Save_Record(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Tab_Save_Record, self).__init__(master=master)

        self.master = master

        self.configure(fg_color='transparent', corner_radius=3,border_color='#0099FF',border_width=1)
        
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.icon_rocket = customtkinter.CTkImage(Image.open(os.path.join(image_path, "rocket.png")), size=(20, 20))
        self.icon_download = customtkinter.CTkImage(Image.open(os.path.join(image_path, "download.png")), size=(20, 20))

        self.grid_columnconfigure(0,weight=1)

        self.label_title = customtkinter.CTkLabel(self,height=20,fg_color='transparent', text="Title:".ljust(10), font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_title.grid(row=2, column=0, sticky="w",padx=5,pady=(10,0))

        self.entry_title = customtkinter.CTkEntry(self ,placeholder_text='Title:...',height=30,text_color='#222222',border_color="#BBBBBB",border_width=2)
        self.entry_title.grid(row=3, column=0,columnspan=3,
                            padx=5,pady=10, sticky="ew")
        
        self.entry_title.bind('<FocusIn>',lambda e:self.focus_in(self.entry_title))
        self.entry_title.bind('<FocusOut>',lambda e:self.focus_out(self.entry_title))

        self.label_description = customtkinter.CTkLabel(self,height=20,fg_color='transparent', text="Description:".ljust(10), font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_description.grid(row=4, column=0, sticky="w",padx=5,pady=(10,0))


        self.entry_description = customtkinter.CTkTextbox(self,border_width=2,border_color='#BBBBBB',height=60,text_color='#222222')
        self.entry_description.grid(row=5, column=0,columnspan=3,
                            padx=5,pady=10, sticky="ew")
        
        self.entry_description.bind('<FocusIn>',lambda e:self.focus_in(self.entry_description))
        self.entry_description.bind('<FocusOut>',lambda e:self.focus_out(self.entry_description))


        self.label_testing = customtkinter.CTkLabel(self,height=20,fg_color='transparent', text="Testing", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_testing.grid(row=7, column=0, sticky="w",padx=5,pady=(10,0))

        self.testing_block = customtkinter.CTkFrame(master=self, fg_color='transparent',corner_radius=5,border_color='black',border_width=2)
        self.testing_block.grid(row=8, column=0 ,columnspan=3, sticky="ew" ,padx=5,pady=10)

        self.label_speed = customtkinter.CTkLabel(self.testing_block,height=20,fg_color='transparent', text="Speed:".ljust(10), font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_speed.grid(row=0, column=0, sticky="ew",pady=10,padx=5)
        
   

        self.speed_blook = customtkinter.CTkFrame(
            master=self.testing_block, corner_radius=0,height=20,fg_color='transparent')
        self.min_label = customtkinter.CTkLabel(self.speed_blook, text="MIN", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.min_label.grid(row=0, column=0, sticky="w",padx=(5,0))
        self.speed_control=customtkinter.CTkSlider(self.speed_blook, from_=2, to=0, number_of_steps=100,width=120)
        self.speed_control.grid(row=0, column=1, sticky="ew")
        self.max_label = customtkinter.CTkLabel(self.speed_blook, text="MAX", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.max_label.grid(row=0, column=2, sticky="e",padx=(0,5))
        self.speed_blook.grid(row=0, column=1,padx=5,pady=10, sticky="ew")
      
        self.label_progress = customtkinter.CTkLabel(self.testing_block,height=20,fg_color='transparent', text="Progress:".ljust(10), font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_progress.grid(row=1, column=0, sticky="w",pady=10,padx=5)


        self.progress_frame = customtkinter.CTkFrame(self.testing_block,fg_color='#33CCFF',corner_radius=50,
                                                            background_corner_colors=['#DDDDDD','#DDDDDD','#DDDDDD','#DDDDDD'])
        self.progress_frame.grid_columnconfigure(0,weight=1)
        self.progress_frame.grid_rowconfigure(0,weight=1)
        self.progress_frame.grid(row=1, column=1,sticky="ew",padx=5,pady=10)

        self.label_current_progress = customtkinter.CTkLabel(self.progress_frame, text="0%",font=('Helvetica',12,'bold'),fg_color='#33CCFF')
        self.label_current_progress.grid(column=1,row=0,padx=(0,10),pady=1)

        self.progress_bar= customtkinter.CTkProgressBar(self.progress_frame,height=14,progress_color='#00FF00',fg_color='#DDDDDD',width=90)
        self.progress_bar.grid(column=0,row=0,sticky='ew',padx=10,pady=0)  
        self.progress_bar.set(0)




        self.btn_testing = customtkinter.CTkButton(
            master=self.testing_block,  corner_radius=8, width=50, text='Run',border_color='#222222',border_width=2,image=self.icon_rocket,compound="left", anchor="center",
            fg_color='gray75', hover_color='gray70',border_spacing=15,font=('Helvetica',14,'bold'),text_color='#222222', command=lambda :self.threading_activate(target=self.test_record,name='test_record'))
        self.btn_testing.grid(row=3, column=1, sticky="e",padx=5,pady=10)

        self.save_record_btn = customtkinter.CTkButton(
            master=self,  corner_radius=8, width=50, text='Save',border_color='#222222',border_width=2,image=self.icon_download,compound="left",
            fg_color='gray75', hover_color='gray70',border_spacing=15,font=('Helvetica',14,'bold'),text_color='#222222', anchor="center",command=self.save_record)
        self.save_record_btn.grid(row=10, column=1, sticky="e",padx=10,pady=20)

        self.profile_user = ''
        self.thread_handle={}
        self.stop_running=True

 

    def focus_in(self,widget):
        widget.configure(border_color="#555555")
    def focus_out(self,widget):
        widget.configure(border_color="#BBBBBB")


    def threading_activate(self,target,args=(),name=''):
        if not name:
            name = uuid4()
        self.thread_handle[name] = threading.Thread(target=target,args=args)
        self.thread_handle[name].daemon = True
        self.thread_handle[name].start()
        
    def stop_testing(self):
        try:
            if self.thread_handle['test_record'].is_alive():
                self.btn_testing.configure(command = None,text='Stopping...')
                self.stop_running=True
        except:
            pass
        
    def reset(self):
        self.stop_testing()
        self.entry_title.delete(0,'end')
        self.entry_description.delete('0.0','end')
        self.speed_control.set(0.5)
        self.progress_bar.set(0)
        

    def change_mode(self,mode):
        if mode == 'record':
            self.save_record_btn.configure(fg_color='#CCCCCC',text_color='#BBBBBB',hover_color='#CCCCCC',border_color='#333333',
                                         width=60,
                                         command=None)
            self.btn_testing.configure(fg_color='#CCCCCC',text_color='#BBBBBB',hover_color='#CCCCCC',border_color='#333333',
                                         width=60,
                                         command=None)
        if mode == 'stop_record':
            self.save_record_btn.configure(fg_color='gray75',text_color='black',hover_color='gray70',border_color='#000000',
                                width=60,
                                command=self.save_record)
            self.btn_testing.configure(fg_color='gray75',text_color='black',hover_color='gray70',border_color='#000000',
                                width=60,
                                command=lambda :self.threading_activate(target=self.test_record,name='test_record'))
        if mode == 'test':
            self.save_record_btn.configure(fg_color='#CCCCCC',text_color='#BBBBBB',hover_color='#CCCCCC',border_color='#333333',
                                width=60,
                                command=None)
            self.btn_testing.configure(text='Stop!',command = self.stop_testing , fg_color='#FF3300',hover_color='#EE0000', width=60)
        if mode == 'stop_test':
            self.save_record_btn.configure(fg_color='gray75',text_color='black',hover_color='gray70',border_color='#000000',
                                width=60,
                                command=self.save_record)
            self.btn_testing.configure(text='Run',command=lambda :self.threading_activate(target=self.test_record,name='test_record'),fg_color='gray75',hover_color='gray70', width=60)



    def test_record(self):
        self.change_mode('test')
        profile_user = self.profile_user
        if not profile_user:
            self.change_mode('stop_test')
            return 
        script = []
        with open('file_1.txt','r',encoding='utf-8') as f:
            script = f.readlines()
        run_function = Execution(profile_user,is_test=True)
        progress_step  = 1/((len(script)-2))
        current_progress=0
        self.progress_bar.set(0)
        self.label_current_progress.configure(text='0%')
        self.stop_running=False
        for command in script:
            speed = float(self.speed_control.get())
            if self.stop_running:
                self.change_mode('stop_test')
                run_function.execute_cmd('end')
                return 
            if command.strip() not in ['end','start']:
                current_progress+=progress_step
                self.progress_bar.set(current_progress)
                self.label_current_progress.configure(text=f'{round(current_progress*100)}%')
            run_function.execute_cmd(command.strip(),time_sleep=speed)
        self.change_mode('stop_test')

    def save_record(self):
        record_name = self.entry_title.get()

        is_exist = self.check_record_name_exist(record_name=record_name)
        if is_exist:
            self.entry_title.focus()
            return
        self.save_record_btn.configure(fg_color='#CC00CC',text_color='white',hover_color='#CC00CC',command=None)

        description = self.entry_description.get('0.0','end')
        profile_user = self.profile_user
        data ={
            'record_name': record_name,
            'description': description,
            'profile_user':profile_user
        }
        res = tkinter.messagebox.askyesno("Save record", "Are you sure to save this record ?")
        if not res:
            self.change_mode('stop_record')
            return

        self.master.master.save_record_from_child(data=data)
        self.reset()
        self.change_mode('stop_record')

    def check_record_name_exist(self, record_name):
        import glob
        if not record_name:
            tkinter.messagebox.showwarning(title='Save Record',message='Record name is empty. Please fill a name')
            return True
        dir_path = os.path.join(os.path.dirname(__file__),'My Record')
        
        json_names = list(map(lambda x: os.path.basename(x), glob.glob(str(dir_path) + "/*/*.json")))
        if record_name +'.json' in json_names:
            tkinter.messagebox.showwarning(title='Save Record',message='Record name already exist. Please use another name')
            return True
        return False