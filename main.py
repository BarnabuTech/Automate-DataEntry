import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the Excel file
excel_file = "C:\\test\\test.xlsx"
data = pd.read_excel(excel_file)

# Set up the WebDriver
service = Service('C:\\chromedriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Log in to the Django admin
admin_login_url = "http://your.url/" #Replace with your Django admin URL
driver.get(admin_login_url)

# Login credentials
email = "your@gmail.com" #Replace with actual Gmail account
password = "yourpassword" #Replace with actual password

# Wait for the email input field to be present before interacting
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password_input = driver.find_element(By.NAME, "password")

email_input.send_keys(email)
password_input.send_keys(password)

# Submit the login form
password_input.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(3)

# Loop through the rows in the Excel data
for index, row in data.iterrows():
    # Navigate to the Django admin 'add' page for your model
    driver.get("http://your.url/") #Add your actuall Django admin URL

    # Wait for the page to load
    time.sleep(2)

    # Fill in the form using the data from the Excel row
    driver.find_element(By.NAME, 'first_name').send_keys(row['first_name'])
    driver.find_element(By.NAME, 'last_name').send_keys(row['last_name'])
    driver.find_element(By.NAME, 'gender').send_keys(row['gender'])
    driver.find_element(By.NAME, 'year_of_birth').send_keys(str(row['year_of_birth']))
    driver.find_element(By.NAME, 'phone_number').send_keys(row['phone_number'])

    # Interact with the Select2 nationality dropdown
    try:
        # Find and click the span element that opens the dropdown
        dropdown_trigger = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection'))
        )
        dropdown_trigger.click()

        # Wait for the input inside the dropdown to become visible
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        )
        
        # Type 'Kenyan' and press Enter
        search_input.send_keys('Kenyan')
        time.sleep(1)  # Wait for options to load
        search_input.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"Error selecting nationality: {e}")
        continue

    # Select the preferred mode of communication (default is 'sms')
    preferred_mode_select = driver.find_element(By.NAME, 'preferred_mode_of_communication')
    preferred_mode_select.send_keys('sms')

    # Submit the form
    driver.find_element(By.NAME, '_save').click()

    # Wait a bit before proceeding to the next entry
    time.sleep(3)

# Close the browser when done
driver.quit()

print("Data entry completed!")
