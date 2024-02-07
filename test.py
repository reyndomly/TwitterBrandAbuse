from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

driver = webdriver.Edge()
url = 'https://twitter.com/i/flow/login'
driver.get(url)
driver.maximize_window()
sleep(5)
username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "text"))).send_keys('reyndomly')
username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "text"))).send_keys(Keys.ENTER)
username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('5141211Nobita')
username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(Keys.ENTER)
sleep(5)
driver.get('https://twitter.com/viciuosly/status/1752115270066569301')
sleep(5)
clicked = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show']/ancestor::div[@role='button']")))
clicked.click()
#clicked = driver.find_element(By.LINK_TEXT, "Show").click()
#clicked = driver.find_element((By.XPATH, "//div[@role='button'][contains(.,'Next')]")).click()
sleep(30)
driver.quit()