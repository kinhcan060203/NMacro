from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import os
import json
import shutil

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(r"--user-data-dir=C:\Users\anhnh\AppData\Local\Google\Chrome\User Data")

def script():
    script = ''
    with open("tracking\script_embb.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n' 
    with open("tracking\script_tag_input.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    with open("tracking\script_tag_button.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    with open("tracking\script_tag_li.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    with open("tracking\script_tag_select.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    with open("tracking\script_tag_a.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    with open("tracking\script_textarea.js", "r", encoding='utf-8') as js:
        script+=js.read()+ '\n'
    
    return script



def save_profile_user(profile_dir,user_data):
    image_src = user_data['image_src']
    dir_path = os.path.join(os.path.dirname(__file__),'My Profile')
    user_dir = os.path.join(dir_path,profile_dir)
    if profile_dir in os.listdir(dir_path):
        with open(os.path.join(user_dir,'user_data.json'),'r',encoding='utf-8') as f:
            pre_image_src = json.load(f)['image_src']
            if pre_image_src != image_src:
                shutil.rmtree(user_dir)
            else:
                return False
    
                    
    os.mkdir(user_dir)
    with open(os.path.join(user_dir,'user_data.json'),'w',encoding='utf-8') as f:
        json.dump(user_data,f,indent=4)

    response = requests.get(image_src)
    with open(os.path.join(user_dir,'image.png'), "wb") as f:
        f.write(response.content)
    return True


class NMacro():

    def __init__(self,master):
        self.master = master
        self.href_init='https://www.google.com/'
        self.window_list = []
        self.script = script()
        self.profile_directory = ''
        try:
            self.driver.get('chrome://version/')
            self.profile_directory = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, '//td[@id="profile_path"]'))).text.split('\\')[-1]
        except Exception as e:
            pass

        self.switch_tab(
            window_handle=self.driver.current_window_handle, href_default=self.href_init,is_init=True)
    @classmethod
    def start_driver(cls,master):
        try:
            cls.driver = webdriver.Chrome(options=options) 
        except Exception as e:
            return None
        return cls(master)
    
    def switch_tab(self, window_handle, href_default='',is_init=False):
        if window_handle not in self.window_list:
            self.window_list.append(window_handle)
        self.driver.switch_to.window(window_handle)
        if href_default:
            self.driver.get(href_default)

            if is_init and self.profile_directory:
                try:
                    profile_wrapper = self.driver.find_element(By.XPATH, '//a[@class="gb_d gb_xa gb_A"]')
                    content = profile_wrapper.get_attribute('aria-label')
                    image_src = profile_wrapper.find_element(By.TAG_NAME,'img').get_attribute('src')
                    if image_src and content:
                        name_user, email_user = content.split(':')[1].split('\n')
                        user_data = {
                            'user_name':name_user.strip(),
                            'email_user':email_user.strip(),
                            'image_src':image_src
                        }
                        save_profile_user(self.profile_directory,user_data=user_data)
                except Exception as e:
                    pass
    def execute_script_sel(self):
        window_handle = self.driver.current_window_handle
        index_window  = f'#{self.driver.window_handles.index(window_handle)+1}.{window_handle}'
        let_window = f'let window="{index_window}"'
        script=let_window+'\n'+self.script
     
        self.driver.execute_script(script)

        return index_window


    def new_tab(self,href_default=''):
        window_handles = self.driver.window_handles
        for window in window_handles:
            if window not in self.window_list:
                self.switch_tab(window_handle=window,href_default=href_default)
                window_id = self.execute_script_sel()
                return window_id
        return None
            
    def handle_script(self,script_id=''):
        if script_id:
            try:
                self.driver.find_element(By.ID, script_id)
            except Exception as e:
                window_id = self.execute_script_sel()
                if 'accounts.google.com' in self.driver.current_url:
                    return window_id, 1
                return window_id,0
        return 0,0
    





