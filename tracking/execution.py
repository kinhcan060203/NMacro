from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import threading
import json

def create_option(profile_user):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(r"--user-data-dir=C:\Users\anhnh\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f'--profile-directory={profile_user}')
    
    return options




class Execution():
    def __init__(self,profile_user,is_test=False):
        self.profile_user=profile_user
        self.options = create_option(self.profile_user)
        self.options.add_argument('--headless') if not is_test else None
        self.driver = None
    def start_driver(self):
        self.driver =  webdriver.Chrome(options=self.options)
        self.parent_iid = {}
        self.parent_iid['#1'] = self.driver.current_window_handle
        self.running = True 


    def new_tab(self,window_id):
        self.driver.execute_script('''window.open("http://bings.com","_blank");''')
        window = self.driver.window_handles[-1]
        self.driver.switch_to.window(window)
        self.parent_iid[window_id] = window
    def close_tab(self,window_id):
        element = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        element.send_keys(Keys.CONTROL + 'w')

    def end_session(self):
        self.running = False 
        self.driver.quit()

    def execute_cmd(self,command,time_sleep=0):
        sleep(time_sleep)
        if command=='end' or not command:
            self.end_session()
            return
        
        if command=='start':
            self.start_driver()
            return 
        
        if len(command.split())==2:
            command = command.split()
            if command[0]=='newTab':
                self.new_tab(window_id=command[1]) 
            elif command[0]=='closeTab':
                self.close_tab(window_id=command[1]) 
 
            return 

        window_handle , url , action = command.split("|")
        action = json.loads('['+action.replace("'",'"')+']')[0]
        TAG_NAME=action['TAG_NAME']
        ID=action['ID']
        CLASS_NAME=action['CLASS_NAME']
        NAME=action['NAME']
        VALUE=action['VALUE']
        CONTENT=action['CONTENT']
        EVENT=action['EVENT']
        if window_handle:
            window = self.parent_iid[window_handle]
            self.driver.switch_to.window(window)

        if EVENT=='changeURL':
            self.driver.get(url)
            return 
            
        
        if TAG_NAME=='a':
            element=None
            try:
                element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.LINK_TEXT, CONTENT)))
                
            except Exception as e:
                element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, f'//a[@href="{VALUE}"]')))
                
            self.driver.execute_script("arguments[0].setAttribute('target',arguments[1])",element, '_self')
            element.click()
            return
        
        for KEY in ['ID','NAME','CLASS_NAME','VALUE']:
            if action[KEY]:
                if EVENT=='click':
                    self.handle_click(tag_name=TAG_NAME,key=KEY,value=action[KEY])
                elif EVENT=='input':
                    self.handle_input(tag_name=TAG_NAME,key=KEY,value=action[KEY],text=VALUE)
                if TAG_NAME=='select' and VALUE:
                    self.handle_select(value=VALUE)
                return

            
    def handle_select(self,value):
        element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//select/option[@value="{value}"]')))
        element.click()
        return True
    
        
    def handle_input(self,tag_name,key,value,text):

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//{tag_name}[@{key}="{value}"]')))
        element.send_keys(text)
        return True

        
    def handle_click(self, tag_name,key,value):
  
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//{tag_name}[@{key}="{value}"]')))
        element.click()
        return True
   
        

   