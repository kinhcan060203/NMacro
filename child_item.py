import os
import json
import customtkinter
from PIL import Image
import tkinter.messagebox
from tkinter import *
from PIL import Image
import glob
import shutil

config = {'border_active_child':'#0099FF','border_unactive_child':'#555555','text_color':'#333333'}

status_color_list = {
        'Completed':'#33CC33',
        'Error':'#FF0000',
        'Scheduled':'#BF3EFF',
        'Running':'#0066FF',
        'Waiting':'#CDAA7D'
    }

class Child_Item(customtkinter.CTkFrame):
    def __init__(self, master,desc={}):
        super(Child_Item, self).__init__(master=master)

        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
        
        self.master = master

        self.icon_garbage = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bin.png")), size=(15, 15))
        self.icon_detail = customtkinter.CTkImage(Image.open(os.path.join(image_path, "detail.png")), size=(15, 15))
        self.icon_edit = customtkinter.CTkImage(Image.open(os.path.join(image_path, "edit.png")), size=(15, 15))
        self.runtime = ''
        self.status=''
        self.record_detail=desc.get('record_detail',{})
        self.schedule_detail=desc.get('schedule_detail',{})
        if self.record_detail:
            dir_path = os.path.join(os.path.dirname(__file__),'My Record')
            self.description = self.record_detail['description']
            self.status_color = '#222222'
            self.item_name = self.record_detail['record_name']
            self.upload_timestamp = self.record_detail['upload_timestamp']
            folder_located =self.record_detail['folder_located']
            self.folder_path = os.path.join(dir_path,folder_located)
        if self.schedule_detail:
            dir_path = os.path.join(os.path.dirname(__file__),'My Schedule')
            self.status = self.schedule_detail['status']
            self.runtime = self.schedule_detail['runtime']
            self.item_name = self.schedule_detail['schedule_name']
            self.upload_timestamp =self.schedule_detail['upload_timestamp']
            self.status_color= status_color_list[self.status]
            folder_located =self.schedule_detail['folder_located']
            self.folder_path = os.path.join(dir_path,folder_located)

        self.configure(border_color=self.status_color,fg_color='#DDDDDD',border_width=2,corner_radius=8,background_corner_colors=['#DDDDDD','#DDDDDD','#DDDDDD','#DDDDDD'])
        self.upload_timestamp = ' | '.join(self.upload_timestamp.split())
        self.item_name = self.item_name[:25] +' ...' if self.item_name[25:] else self.item_name[:25]
        

        self.label_title = customtkinter.CTkLabel(self, width=220,fg_color='transparent',text_color=config['text_color'], text=self.item_name, font=customtkinter.CTkFont(size=12, weight="bold"),
                                                  justify='left',anchor='w')
        self.label_title.grid(row=0, column=0,columnspan=3, sticky="w",pady=(3,5),padx=8)

        if self.runtime:
            self.runtime_content = customtkinter.CTkLabel(self,width=10,fg_color='transparent',text_color='black', text=f'{0}/{self.runtime}', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        justify='right',anchor='e')
            self.runtime_content.grid(row=0, column=2, sticky="e",pady=2,padx=5)

        if self.status:
            
            self.label_status = customtkinter.CTkLabel(self, height=30,fg_color='transparent',text_color=config['text_color'], text='Status:', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        justify='left',anchor='w')
            self.label_status.grid(row=1, column=0, sticky="w",pady=2,padx=8)

            self.status_content = customtkinter.CTkLabel(self,width=20,fg_color='transparent',text_color=self.status_color, text=self.status, font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        justify='right',anchor='e')
            self.status_content.grid(row=1, column=1,columnspan=2, sticky="e",pady=2,padx=5)


        self.btn_more_detail = customtkinter.CTkButton(width=30,height=10,image=self.icon_detail,hover_color='#00E5EE',text_color='black',border_spacing=4,font=customtkinter.CTkFont(size=12, weight="bold"),
            master=self,  corner_radius=5, text='More detail',fg_color="#00F5FF",command=lambda folder_path=self.folder_path: self.show_detail(folder_path=folder_path))
        self.btn_more_detail.grid(row=10, column=0,sticky="w",pady=5,padx=5)



        self.btn_delete = customtkinter.CTkButton(width=10,height=10,image=self.icon_garbage,hover_color='#CC6666',text_color='black',
            master=self,  corner_radius=5, text='',fg_color="#FF6666",command=lambda folder_path=self.folder_path: self.item_folder_delete(folder_path=folder_path))
        self.btn_delete.grid(row=10, column=2,sticky="e",pady=5,padx=5)

        self.btn_edit = customtkinter.CTkButton(width=30,height=10,hover_color='#00E5EE',image=self.icon_edit,border_spacing=4,text_color='black',font=customtkinter.CTkFont(size=12, weight="bold"),
            master=self,  corner_radius=5, text='Edit',fg_color="#00F5FF",command=lambda folder_path=self.folder_path: self.edit_tem(folder_path=folder_path))
        self.btn_edit.grid(row=10, column=1,sticky="ew",pady=5,padx=5)


        if self.record_detail:
            self.label_upload_time = customtkinter.CTkLabel(self, height=30,fg_color='transparent',text_color=config['text_color'], text='Upload at:', font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        justify='left',anchor='w')
            self.label_upload_time.grid(row=2, column=0, sticky="w",pady=2,padx=8)

            self.upload_time_content = customtkinter.CTkLabel(self,width=20,fg_color='transparent',text_color=config['text_color'], text=self.upload_timestamp, font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        justify='right',anchor='e')
            self.upload_time_content.grid(row=2, column=1,columnspan=2, sticky="e",pady=2,padx=5)

    def show_detail(self,folder_path):
        data = {}
        json_paths =  glob.glob(str(folder_path) + "/*.json")
        if json_paths:
            with open(json_paths[0],'r',encoding='utf-8') as f:
                data = json.load(f)
            self.master.show_more_detail(data=data)

    def edit_tem(self,folder_path):
        data = {}
        json_paths = glob.glob(str(folder_path) + "/*.json")
        if json_paths:
            with open(json_paths[0],'r',encoding='utf-8') as f:
                data = json.load(f)
            self.master.show_edit_window(data=data)
                

    def update_runtime(self,current_runtime):
        self.runtime_content.configure(text=f'{current_runtime}/{self.runtime}')

    def item_folder_delete(self,folder_path):
        res = tkinter.messagebox.askyesno("Delete", "Are you sure delete it permanently?")
        if not res:
            return
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                with open(os.path.join(os.path.dirname(folder_path),'located_detail.json'),'r+',encoding='utf-8') as jsonfile:
                    located_detail=json.load(jsonfile)
                    jsonfile.truncate(0)
                    jsonfile.seek(0)
                    located_detail.pop(os.path.basename(folder_path))

                    json.dump(located_detail, jsonfile, indent = 4)
            self.grid_forget()

        except Exception as e:  
            pass