from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#  Input credentials
# case_type = "BAIL APPLN."
# case_number = "2165"
# case_year = "2025"

# Setup Headless Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def judgement(case_type ,case_number, case_year):
    driver3 = webdriver.Chrome(options=chrome_options)

    #  Open Judgment Search Page
    driver3.get("https://delhihighcourt.nic.in/app/case-number")
    time.sleep(2)





    # Fill the form
    try:
        Select(driver3.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
        driver3.find_element(By.ID, "case_number").send_keys(case_number)
        Select(driver3.find_element(By.ID, "year")).select_by_visible_text(case_year)

        # Get visible CAPTCHA text
        captcha = driver3.find_element(By.ID, "captcha-code").text.strip()
        driver3.find_element(By.ID, "captchaInput").send_keys(captcha)

        # Submit using JS click
        submit_btn = driver3.find_element(By.ID, "search")
        driver3.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        driver3.execute_script("arguments[0].click();", submit_btn)

        # Wait for result table or PDF link to appear
        WebDriverWait(driver3, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".pdf")]'))
        )

        # Get the first PDF link
        pdf_link_element = driver3.find_element(By.XPATH, '//a[contains(@href, ".pdf")]')
        pdf_link = pdf_link_element.get_attribute("href")



    except :
        pdf_link = "Server Error"

    finally:
        driver3.quit()
    return {"Judgment PDF": pdf_link}

def get_case_list():
    driver3 = webdriver.Chrome(options=chrome_options)
    driver3.get("https://delhihighcourt.nic.in/app/case-number")
    time.sleep(2)
    case_type_options = driver3.find_elements(By.XPATH, '//*[@id="case_type"]/option')
    case_list = []
    for option in case_type_options:
        item = option.text
        case_list.append(item)
    return case_list
