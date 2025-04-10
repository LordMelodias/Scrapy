from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("http://quotes.toscrape.com")

data = []

while True:
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    
    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, 'text').text
        author = quote.find_element(By.CLASS_NAME, 'author').text
        data.append({"text": text, "author": author})
        # print(data)
    # 5. Check if "Next" button exists
    try:
        print("try")
        # Wait until the "Next" button is clickable
        # next_button = driver.find_element(By.CLASS_NAME, "next")
        # Look for the first <li> element that has the class next, and then get its child <a> element, which is the link for the next page
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()  # Click "Next" button to go to the next page
        print("it go")
    except Exception as e:
        print("No more pages. Exiting...")
        break  # Exit if no "Next" button found (last page)

# Save to JSON
json.dump(data, open("quotes1.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)

# Save to CSV
csv.writer(open("quotes2.csv", "w", newline="", encoding="utf-8")).writerows([["text", "author"]] + [[d["text"], d["author"]] for d in data])

driver.quit()