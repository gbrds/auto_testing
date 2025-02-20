"""
Programm opens google.com ; rejects cookies ; locates searchbar and searches for pregiven search ;
bypasses reCAPTCHA ; clicks on three first results ; and navigates to the next 2 pages

How to run: download and run in comand promt: python3 google_search_click.py
"""

import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load existing Chrome profile
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/home/juss/.config/google-chrome")  # Change to your profile path: helps to awoid reCAPTCHA

# Initialize WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# Open Google Homepage
driver.get("https://www.google.com")

# Handle the cookie pop-up
try:
    reject_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//div[contains(text(), "Keeldu kõigist")]]')))
    reject_button.click()
    print("Rejected cookies.")
except:
    print("No cookie pop-up detected.")

# Locate Search Box & Enter Query
search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
search_query = "Selenium Python automation"
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# Wait for Search Results
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))

# Click on Search Results
for i in range(3):  # Click on first 3 results
    search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3")))
    if i >= len(search_results):
        break
    print(f"Clicking on result {i + 1}: {search_results[i].text}")
    search_results[i].click()
    driver.back()

# Handle Pagination (Next Page)
for page in range(2):  # Navigate through 2 pages
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Järgmine")))
        next_button.click()
        print(f"Moving to page {page + 2}")
    except:
        print("No more pages found.")
        break

# Close Browser
driver.quit()
