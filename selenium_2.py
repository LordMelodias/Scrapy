from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("http://quotes.toscrape.com")

quotes = driver.find_elements(By.CLASS_NAME, 'quote')
print(quotes)
data = []

for quote in quotes:
    text = quote.find_element(By.CLASS_NAME, 'text').text
    author = quote.find_element(By.CLASS_NAME, 'author').text
    data.append({"text": text, "author": author})
    print(data)

# Save to JSON
json.dump(data, open("quotes.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)

# Save to CSV
csv.writer(open("quotes.csv", "w", newline="", encoding="utf-8")).writerows([["text", "author"]] + [[d["text"], d["author"]] for d in data])

driver.quit()