import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import unittest
from app import create_app, db
from app.config import TestingConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import multiprocessing
from tests.db_utilities import populate_db

localHost= 'http://localhost:5000/'
class BasicSeleniumTests(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        #populate_db()

        ''' for windowsless version
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=options)'''

        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(localHost)  

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()

    # Pre-defined functions
    def find(self, xpath):
        self.driver.find_element(By.XPATH, xpath)
        time.sleep(1)

    def signup(self, username = 'usernameOne', password = 'testing1'):
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, 'Create an account.').click()
        time.sleep(1)

        self.driver.find_element(By.ID, "signup-username").send_keys(username)
        self.driver.find_element(By.ID, "signup-psw").send_keys(password)
        self.driver.find_element(By.ID, "signup-pswConfirm").send_keys(password)
        self.driver.find_element(By.XPATH, "/html/body/main/div/div/div[2]/form/button").click()
    
    def login(self, username = 'usernameOne', password = 'testing1'):
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(username)
        self.driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(password)
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/form/button').click()
    
    def goHome(self):
        self.driver.find_element(By.LINK_TEXT, 'PicTalk').click()
        time.sleep(1)
    
    def goSearch(self, query):
        self.driver.find_element(By.XPATH, '//*[@id="search"]').send_keys(query)
        self.driver.find_element(By.XPATH, '//*[@id="search"]').send_keys(Keys.ENTER)
        time.sleep(1)

    def goGallery(self):
        self.driver.find_element(By.LINK_TEXT, 'Gallery').click()
        time.sleep(1)
    
    def goSubmit(self):
        self.driver.find_element(By.LINK_TEXT, 'Submit').click()
        time.sleep(1)

    def Submit(self):
        self.driver.find_element(By.XPATH, '//*[@id="file-upload"]').send_keys(os.getcwd()+"/image.jpg")

        self.driver.find_element(By.XPATH, '//*[@id="caption-text-input"]').send_keys('This is a caption for this image.')

        self.driver.find_element(By.XPATH, '//*[@id="tag-text-input"]').send_keys('TagOne')
        self.driver.find_element(By.XPATH, '//*[@id="tag-text-input"]').send_keys(Keys.ENTER)

        self.driver.find_element(By.XPATH, '//*[@id="tag-text-input"]').send_keys('TagTwo')
        self.driver.find_element(By.XPATH, '//*[@id="tag-text-input"]').send_keys(Keys.ENTER)

        self.driver.find_element(By.XPATH, '//*[@id="submit-btn"]').click()
        time.sleep(1)

    def goProfile(self):
        self.driver.find_element(By.XPATH, '/html/body/header/nav/div/div/ul/li[3]/a').click()
        time.sleep(1)
    
    def goLogout(self):
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

    # ////////////////

    def test_appLoad(self):
        time.sleep(1)
        self.assertEqual(self.driver.current_url, localHost)

    def test_page_navigation_unauthenticated(self):
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, localHost + "login")

        self.goGallery()
        self.assertEqual(self.driver.current_url, localHost + 'gallery')

        self.goHome()
        self.assertEqual(self.driver.current_url, localHost)
    
    def test_signup(self):
        self.signup()
        self.assertEqual(self.driver.current_url, localHost + 'login')

    def test_signup_login(self):
        self.signup()
        self.login()
        self.assertEqual(self.driver.current_url, localHost)
    
    def test_login(self):
        self.signup()
        self.login()
        self.goLogout()
        self.login()

        self.assertEqual(self.driver.current_url, localHost)
    
    def test_page_navigation_authenticated(self):
        self.signup()
        self.login()

        self.goSubmit()
        self.assertEqual(self.driver.current_url, localHost + 'create')

        self.goHome()
        self.assertEqual(self.driver.current_url, localHost)

        self.goGallery()
        self.assertEqual(self.driver.current_url, localHost + 'gallery')

        self.goProfile()
        self.assertEqual(self.driver.current_url, localHost + 'profile/usernameone')

        self.goLogout()
        self.assertEqual(self.driver.current_url, localHost)

    def test_submit(self): # Return to the home page.
        self.signup()
        self.login()
        self.goSubmit()
        self.Submit()

        self.assertEqual(self.driver.current_url, localHost)
    
    def test_gallery(self): # Returns to image page
        self.signup()
        self.login()
        self.goSubmit()
        self.Submit()

        self.goGallery()
        self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div/div[1]/a[1]/img').click()
        self.assertEqual(self.driver.current_url, localHost + 'image/1')

    def test_comment(self):
        self.signup()
        self.login()
        self.goSubmit()
        self.Submit()

        self.goGallery()
        self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div/div[1]/a[1]/img').click()

        self.driver.find_element(By.XPATH, '//*[@id="comment-box"]').send_keys("This is a comment!")
        self.driver.find_element(By.XPATH, '//*[@id="submit"]').send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, '//*[@id="comment-box"]').send_keys("This is another comment!")
        self.driver.find_element(By.XPATH, '//*[@id="submit"]').send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, '//*[@id="comment-box"]').send_keys("This is also a comment!")
        self.driver.find_element(By.XPATH, '//*[@id="submit"]').send_keys(Keys.ENTER)

        # checks if comments exists
        self.driver.find_element(By.XPATH, '/html/body/main/ul/li[1]')
        self.driver.find_element(By.XPATH, '/html/body/main/ul/li[2]')
        self.driver.find_element(By.XPATH, '/html/body/main/ul/li[3]')

    def test_search(self): # Returns search page, with one user
        self.signup('usernameTwo', 'testing2')
        self.goHome()
        self.signup('username', 'testing1')
        self.login('username', 'testing1')

        self.goSearch('usernameTwo')
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[1]/ul/li/a')

    def test_searchTag(self):
        self.signup()
        self.login()
        self.goSubmit()
        self.Submit()

        self.goHome()
        self.goLogout()
        self.signup('usernameTwo', 'testing2')
        self.login('usernameTwo', 'testing2')

        self.goSearch('TagOne')
        self.driver.find_element(By.XPATH, '//*[@id="tags-tab"]').click()
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[2]/ul/li/a')
        self.goSearch('TagTwo')
        self.driver.find_element(By.XPATH, '//*[@id="tags-tab"]').click()
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[2]/ul/li/a')

        # Test does not work, cannot get element.
    def test_follow(self):
        self.signup('usernameTwo', 'testing2')
        self.goHome()
        self.signup('username', 'testing1')
        self.login('username', 'testing1')

        self.goSearch('usernameTwo')
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[1]/ul/li/a').click()
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/form/button').click()
        followers = self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[2]')
        follower_count = ''.join(filter(str.isdigit, followers.text))
        self.assertEqual(follower_count, '1')

        self.goProfile()
        following = self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[3]')
        following_count = ''.join(filter(str.isdigit, following.text))
        self.assertEqual(following_count, '1')
    
    # Test does not work, cannot get element.
    def test_unfollow(self):
        self.signup('usernameTwo', 'testing2')
        self.goHome()
        self.signup('username', 'testing1')
        self.login('username', 'testing1')

        self.goSearch('usernameTwo')
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[1]/ul/li/a').click()
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/form/button').click()
        followers = self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[2]')
        
        self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/form/button').click()
        followers = self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[2]')
        follower_count = ''.join(filter(str.isdigit, followers.text))
        self.assertEqual(follower_count, '0')
        
        self.goProfile()
        following = self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[3]')
        following_count = ''.join(filter(str.isdigit, following.text))
        self.assertEqual(following_count, '0')

    # Will have to assume the following feature works.
    def test_gallery_follow(self):
        self.signup('usernameTwo', 'testing2')
        self.login('usernameTwo', 'testing2')
        self.goSubmit()
        self.Submit()

        self.goLogout()
        self.signup()
        self.login()

        self.goSearch('usernameTwo')
        self.driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[1]/ul/li[1]/a').click()
        self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/form/button').click() # Follow 'usernameTwo'
        
        self.goHome()
        self.goGallery()
        self.driver.find_element(By.XPATH, '//*[@id="pills-following-tab"]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div/div[1]/a/img')
    
    def test_edit_profile(self):
        self.signup()
        self.login()
        self.goProfile()

        self.driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div[1]/p[2]/a').click()
        time.sleep(1)
        username = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        username.clear()
        username.send_keys('editProfile')
        self.driver.find_element(By.XPATH, '//*[@id="about_me"]').send_keys("Testing about me feature!")
        self.driver.find_element(By.XPATH, '//*[@id="submit"]').click()
        time.sleep(1)

        self.assertEqual(self.driver.current_url, localHost + 'profile/editProfile')
        # About me xpath was not working.
        about_me = self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div/div/div/div[2]')
        self.assertEqual(about_me.text, "Testing about me feature!")

if __name__ == "__main__":
    unittest.main(verbosity=2)