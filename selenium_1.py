from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open a website
driver.get("http://quotes.toscrape.com")

# Find all quotes on the page
quotes = driver.find_elements(By.CLASS_NAME, "quote")

for quote in quotes:
    text = quote.find_element(By.CLASS_NAME, "text").text
    author = quote.find_element(By.CLASS_NAME, "author").text
    print(f"{text} - {author}")

# Close browser
driver.quit()
