from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# For Dev TEST
# case_type = "BAIL APPLN."
# case_number = "2165"
# case_year = "2025"

#  Setup Headless Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_filing_date(case_type,case_number,case_year):
    try:
        driver2 = webdriver.Chrome(options=chrome_options)
        driver2.get("https://dhcmisc.nic.in/pcase/guiCaseWise.php")
        time.sleep(2)



    #  Fill form

        Select(driver2.find_element(By.ID, "ctype")).select_by_visible_text(case_type)
        driver2.find_element(By.ID, "regno").send_keys(case_number)
        Select(driver2.find_element(By.ID, "regyr")).select_by_visible_text(case_year)

        captcha = driver2.find_element(By.ID, "cap").text.strip()
        driver2.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr[8]/td[2]/input').send_keys(captcha)

        # Click submit using JS to avoid interception
        submit_btn = driver2.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr[12]/td[2]/input[2]')
        driver2.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        driver2.execute_script("arguments[0].click();", submit_btn)

        # Wait for filing date to load
        filing_date = WebDriverWait(driver2, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form3"]/table[1]/tbody/tr[1]/td[5]/font'))
        ).text.strip()

        registeration_date = WebDriverWait(driver2, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form3"]/table[1]/tbody/tr[3]/td[5]/font'))
        ).text.strip()







    except Exception as e:
        filing_date = "Server Error"
        registeration_date = "Server Error"

    finally:
        driver2.quit()

    return {
        "filing_date": filing_date,
        "registeration_date": registeration_date,

    }




