import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import unittest
from app import create_app, db
from app.config import TestingConfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from db_utilities import populate_db

localHost= 'http://localhost:5000/'
class BasicSeleniumTests(unittest.TestCase):

    def setUp(self):
        testApp = create_app(TestingConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        populate_db()


        self.driver = webdriver.Chrome() 
        self.driver.get(localHost)  

    def tearDown(self):
        self.driver.quit()

    def test_page_title(self):
        # Check if the page title contains "Example Domain"
        self.assertIn("Example Domain", self.driver.title)

    def test_search(self):
        # Example of interacting with the web page
        driver = self.driver
        search_box = driver.find_element_by_name("q")  # Adjust the selector based on your web app
        search_box.send_keys("Selenium WebDriver")
        search_box.send_keys(Keys.RETURN)
        self.assertIn("Selenium WebDriver", driver.title)

if __name__ == "__main__":
    unittest.main(verbosity=2)
