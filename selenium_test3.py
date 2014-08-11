from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def test_users_grid():

  driver = webdriver.Firefox()
  #driver = self.driver
  driver.get("http://localhost:8000/users_jqueryui/")
  search_input = driver.find_element_by_id("input1")
  search_input.send_keys('Sean')
  driver.find_element_by_id("search_btn1").click()
  time.sleep(5)
  # self.assertIn("Django", driver.title)
  # self.assertIn("shu", driver.title)



if __name__ == "__main__":
    test_users_grid()
