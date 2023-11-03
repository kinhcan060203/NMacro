import os
import json
import socket
import threading
import customtkinter
from PIL import Image
from time import sleep
from uuid import uuid4
from tkinter import ttk
import tkinter.messagebox
from urllib.parse import unquote
from tkinter import *
from PIL import Image
from selenium.webdriver.common.by import By
from tracking.tracking import NMacro
from datetime import datetime
from config import *

class Record(customtkinter.CTkFrame):
    def __init__(self, master):
        super(Record, self).__init__(master=master)
        self.master = master
        image_path = os.path.join(os.path.dirname(  
            os.path.realpath(__file__)), "test_images")
        self.wolf_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "cute_wolf.png")), size=(15, 15))


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.tab_bar = customtkinter.CTkFrame(master=self, height=26, fg_color=config['unactive_tab'],corner_radius=0)
        self.bottom_border_tab_bar = customtkinter.CTkFrame(master=self, height=6, fg_color=config['tab_active'],corner_radius=0)
        
        self.tab_bar.grid(row=0,column=0, sticky="nsew")
        self.bottom_border_tab_bar.grid(row=1,column=0, sticky="new")

        self.item_handle = {}
        self.tab_bar_list = {}
        self.TreeView_list = {}
        self.pare_child_handle = {}

        scrollableFrame = customtkinter.CTkScrollableFrame(self,fg_color='white',corner_radius=0)
        scrollableFrame.grid_columnconfigure(0,weight=1)
        scrollableFrame.grid(row=2, column=0, sticky="nsew")

        self.href_default = 'https://fap.fpt.edu.vn/'
        self.thread_handle={}
        self.threading_activate(name = 'socket_activate',target=self.socket_activate)
    
    def start_record(self):
        with open('file_1.txt','w',encoding='utf-8') as f:
            pass
        self.stop_record = False
        self.iid=0
        self.parent_iid = {}
        self.thread_handle={}
        self.tab_bar_list = {}
        self.TreeView_list = {}
        self.item_handle = {}
        self.profile_directory=''
        self.pare_child_handle = {'root':[]}
        self.is_from_socket=False
        self.NMacro = NMacro.start_driver(self)
        if not self.NMacro:
            return
        self.profile_directory = self.NMacro.profile_directory
        self.parent_iid['#1.'+self.NMacro.driver.current_window_handle] = 0
        self.insert_tab_treeView('#1.'+self.NMacro.driver.current_window_handle)
        self.imwrite_action(text="start")
        self.threading_activate(target=self.check_windowns)
        self.threading_activate(target=self.check_is_from_socket)

    def check_is_from_socket(self):
        while True:
            sleep(1)
            if self.is_from_socket:
                sleep(1)
                self.is_from_socket = False
            elif self.stop_record:
                break

    def stop_record_event(self):
        try:
            self.stop_record = True
            external_data = {'profile_user':self.profile_directory}
            self.master.stop_record_event(external_data)
            self.imwrite_action('end')
            self.NMacro.driver.quit()
            self.NMacro = None
        except Exception as e:
            self.NMacro = None
            pass

    def imwrite_action(self, text):
        with open('file_1.txt', 'a',encoding='utf-8') as f:
            f.write(text+'\n')

    def insert_tab_treeView(self,current_window_handle):    

        scrollableFrame = customtkinter.CTkScrollableFrame(self,fg_color='white',corner_radius=0)
        scrollableFrame.grid_columnconfigure(0,weight=1)
        self.TreeView_list[current_window_handle] = scrollableFrame
        new_tab = customtkinter.CTkButton(
            master=self.tab_bar,  corner_radius=0, width=100, height=24,
            text='tab '+str(len(self.TreeView_list)),font=('Helvetica',12,'bold'),text_color='#FFFFFF',anchor='center',
            command=lambda current_window_handle=current_window_handle: self.show_eventsTreeview(current_window_handle))
        
        self.tab_bar_list[current_window_handle] = new_tab
        self.tab_bar_list[current_window_handle].grid(row=0, column=len(self.TreeView_list))
        self.show_eventsTreeview(current_window_handle)


    def create_childView(self,current_window_handle,iid,text):
        padx=4
        fg_color_childView = '#33CCFF'
        if iid not in self.pare_child_handle:
            padx = 34
            fg_color_childView = '#33FFFF'

        childView =customtkinter.CTkFrame(master=self.TreeView_list[current_window_handle],corner_radius=0,fg_color=fg_color_childView)
        content = customtkinter.CTkLabel(master=childView,image=self.wolf_icon,compound='left', text=text,fg_color='transparent',text_color='black',corner_radius=0,anchor='w')

        childView.bind('<Button>',command=lambda e,iid=iid,childView = childView: self.click_childView(iid=iid,childView=childView))
        childView.bind('<Enter>',command=lambda e,iid=iid,childView = childView: self.enter_childView(iid=iid,childView=childView))
        childView.bind('<Leave>',command=lambda e,iid=iid,childView = childView: self.leave_childView(iid=iid,childView=childView))
        content.bind('<Button>',command=lambda e,iid=iid,childView = childView: self.click_childView(iid=iid,childView=childView))
        content.bind('<Enter>',command=lambda e,iid=iid,childView = childView: self.enter_childView(iid=iid,childView=childView))
        content.bind('<Leave>',command=lambda e,iid=iid,childView = childView: self.leave_childView(iid=iid,childView=childView))
        content.grid(column=1,row=0,padx=padx,sticky='w',pady=5)

        return childView
    
    def enter_childView(self,iid,childView):
        if iid in self.pare_child_handle:
            childView.configure(fg_color='#00BFFF')
        else:
            childView.configure(fg_color='#00F5FF') 

    def leave_childView(self,iid,childView):
        if iid in self.pare_child_handle:
            childView.configure(fg_color='#33CCFF')
        else:
            childView.configure(fg_color='#33FFFF') 
        
    def click_childView(self,iid,childView):
        pass


    def insert_childView(self,current_window_handle,parent_iid, iid, text):
        if iid in self.item_handle:
            return None
        if parent_iid not in self.pare_child_handle:
            return
        text = ' '*3+text
        childView=self.create_childView(current_window_handle=current_window_handle,iid=iid,text=text)
        self.item_handle[iid] = childView
        childView.grid(column=0,row=iid,sticky='ew')

    def insert_event(self, current_window_handle , parent , iid , url , action , record=True):
        try:
            if iid not in self.pare_child_handle:
                self.insert_childView(current_window_handle,parent, iid, text=action['TEXT'])
            else:
                self.insert_childView(current_window_handle,parent, iid, text=url)

            if record:
                id = list(self.parent_iid.keys()).index(current_window_handle)+1
                self.imwrite_action(f'#{id}|{url}|{action}')
        except Exception as e:
            print(e,'insert_event')
        self.show_eventsTreeview(current_window_handle)



    def socket_activate(self):
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 5000
        s.bind(('127.0.0.1', port))
        print("socket binded to %s" % (port))
        s.listen(5)
        FORMAT = 'utf-8'
        while True:
            try:
                conn, addr = s.accept()
                data = conn.recv(4096).decode()
                data = '[' + unquote(data.split('\n')[-1], encoding=FORMAT)+']'
                data = json.loads(data)
                if not data:
                    conn.send('Faild data!'.encode(FORMAT))
                    continue
                if data[0].get("ACTION",None):
                    self.is_from_socket = True
                self.preprocess_event(data[0])
                self.prepare_event_and_insert(data=data[0])
                conn.send('Connection successful!'.encode(FORMAT))
                conn.close()

            except Exception as e:
                print(e,"socket")


    def check_windowns(self):
        ACTION = {'TAG_NAME': '', 'ID': '', 'CLASS_NAME': '', 'NAME': '', 'VALUE': '', 'CONTENT': '', 'EVENT': 'changeURL','TEXT': ''}
        while True:
            if self.stop_record:
                return
            try:

                window_id, is_from_gg = self.NMacro.handle_script(script_id='myscript')
                if window_id:

                    if not self.is_from_socket:
                        url = self.NMacro.driver.current_url
                        ACTION['TEXT'] = f'Thay đổi tới đường link: {url}'
                        data ={'URL':url,'ACTION':ACTION,'WINDOW_ID':window_id}
                        self.prepare_event_and_insert(data=data)
                    self.is_from_socket = False
                    if is_from_gg:
                        self.threading_activate(target=self.google_account_manager,args=(window_id,))
                    
                if len(self.parent_iid)<len(self.NMacro.driver.window_handles):
                    window_id = self.NMacro.new_tab(href_default=self.href_default)
                    ACTION['TEXT'] = f'Thay đổi tới đường link: {self.href_default}'
                    data ={'URL':self.href_default,'ACTION':ACTION,'WINDOW_ID':window_id}
                    if window_id:
                        self.parent_iid[window_id]=0
                        self.imwrite_action(text=f"newTab {window_id.split('.')[0]}")
                        self.insert_tab_treeView(current_window_handle=window_id)
                        self.prepare_event_and_insert(data=data)
                        self.is_from_socket=False
            except Exception as e:
                self.threading_activate(target = self.stop_record_event)
                return
        
    def preprocess_event(self, data):
        window_id = data['WINDOW_ID']
        window_handle = window_id.split('.')[1]
        if window_handle!=self.NMacro.driver.current_window_handle:
            self.NMacro.switch_tab(window_handle=window_handle)
        url = data.get('URL', '')
        action = data.get('ACTION', '')
        current_url = data.get('CURRENT_URL', '')
        if url:
            self.NMacro.driver.get(url)
        elif action['EVENT']=='click':
            if self.NMacro.driver.current_url != current_url:
                data['URL'] = self.NMacro.driver.current_url


    def prepare_event_and_insert(self, data=None):
        
        if data:
            window_handle =data['WINDOW_ID']
            parent = self.parent_iid[window_handle]
            self.iid+=1
            url = data.get('URL','')
            action = data.get('ACTION','')
            
            if url:
                self.insert_event(window_handle,parent, self.iid,url,data['ACTION'],record=False)
                self.iid+=1
                self.pare_child_handle[self.iid] = []
                self.pare_child_handle['root'].append(self.iid)
                self.parent_iid[window_handle] = self.iid
                self.insert_event(window_handle,'root', self.iid,url, data['ACTION'])

            elif action:
                self.pare_child_handle[parent].append(self.iid)
                self.insert_event(window_handle,parent, self.iid,url,data['ACTION'])

    def google_account_manager(self,window_id=''):
        while 'accounts.google.com' in self.NMacro.driver.current_url:
            try:
                elements = self.NMacro.driver.find_elements(By.XPATH, '//*[@data_unique="my_id"]')
                for element in elements:
                    data = track_data_unique_gg_account(driver=self.NMacro.driver,element=element,window_id=window_id)
                    if not data:
                        break
                    self.preprocess_event(data=data)
                    self.prepare_event_and_insert(data=data)

                    self.NMacro.driver.execute_script("arguments[0].setAttribute('data_unique',arguments[1])",element, '')
            except:
                pass

    def reset(self):
        self.show_eventsTreeview(current_window_handle='@')
        self.tab_bar_list={}
        self.TreeView_list={}


    def show_eventsTreeview(self,current_window_handle):
        for id in self.TreeView_list:
            if id == current_window_handle:
                self.tab_bar_list[id].configure(fg_color=config['tab_active'], hover_color=config['tab_active'])
                self.TreeView_list[id].grid(row=2, column=0, sticky="nsew")
            elif current_window_handle=='@':
                self.TreeView_list[id].grid_forget()
                self.tab_bar_list[id].grid_forget()
            else:
                self.TreeView_list[id].grid_forget()
                self.tab_bar_list[id].configure(fg_color=config['unactive_tab'], hover_color=config['unactive_hover_tab'])


    def threading_activate(self,target,args=(),name=''):
        if not name:
            name = uuid4()
        self.thread_handle[name] = threading.Thread(target=target,args=args)
        self.thread_handle[name].daemon = True
        self.thread_handle[name].start()



def get_info_element(element,attribute_name):
    result = element.get_attribute(attribute_name)
    return result if result else ''

def track_data_unique_gg_account(driver,element, window_id):
    
    TAG_NAME = element.tag_name
    ID = get_info_element(element,"id")
    CLASS_NAME = get_info_element(element,"class")
    NAME = get_info_element(element,"name")
    VALUE = get_info_element(element,"value")
    CONTENT = VALUE
    TEXT = ''
    EVENT = ''
    URL=''
    if TAG_NAME=='input':
        TEXT = 'Nhập '+ get_info_element(element,"type")+': ' + VALUE
        EVENT = 'input'
    elif TAG_NAME=='a':
        VALUE = get_info_element(element,"href")
        TEXT = 'Nhấn link: ' + VALUE
        EVENT = 'click'
        URL = VALUE
    elif TAG_NAME=='button':
        tag_span = element.find_element(By.TAG_NAME, 'span')
        TEXT = 'Nhấn nút: ' + tag_span.text
        EVENT = 'click'
    elif TAG_NAME == 'li':
        EVENT = 'click'
        all_child = element.find_elements(By.XPATH, '*')
        for child in all_child:
            CONTENT= get_info_element(child,"data-identifier")
            if '@' in CONTENT:
                TEXT += CONTENT
                break
    else:
        return False

    data={'URL':URL,
          'ACTION':{'TAG_NAME': TAG_NAME, 'ID': ID, 'CLASS_NAME': CLASS_NAME, 'NAME': NAME, 'VALUE': VALUE, 'CONTENT': CONTENT, 'EVENT': EVENT, 'TEXT': TEXT},
          'WINDOW_ID':window_id,
          'CURRENT_URL':driver.current_url} 

    return data