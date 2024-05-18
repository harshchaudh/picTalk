import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import unittest
from app import create_app, db
from app.config import TestingConfig
from selenium import webdriver
import multiprocessing
from db_utilities import populate_db

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
        self.driver.get(localHost)  

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()


    def test1(self):
        time.sleep(1)
        self.assertEqual(self.driver.current_url, localHost)

if __name__ == "__main__":
    unittest.main(verbosity=2)
