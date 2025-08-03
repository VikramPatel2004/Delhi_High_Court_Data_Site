from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#  Input your case details here
# case_type = "BAIL APPLN."
# case_number = "2165"
# case_year = "2025"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
def details (case_number, case_year, case_type):
    driver1 = webdriver.Chrome(options=chrome_options)


    driver1.get("https://delhihighcourt.nic.in/app/get-case-type-status")
    time.sleep(2)


    Select(driver1.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
    driver1.find_element(By.ID, "case_number").send_keys(case_number)
    Select(driver1.find_element(By.ID, "case_year")).select_by_visible_text(case_year)

    #CAPTCHA
    captcha = driver1.find_element(By.ID, "captcha-code")
    driver1.find_element(By.ID, "captchaInput").send_keys(captcha.text.strip())

    #Click Search
    try:
        search_button = driver1.find_element(By.ID, "search")
        driver1.execute_script("arguments[0].scrollIntoView(true);", search_button)
        time.sleep(1)
        driver1.execute_script("arguments[0].click();", search_button)
        time.sleep(2)
    except :
        party_name, next_Date, order_date, order_link = "Server Error", "Server Error", "Server Error", "Server Error"
        driver1.quit()
        exit()
    try:
        party_name = driver1.find_element(By.XPATH, '//*[@id="caseTable"]/tbody/tr/td[3]').text
        next_Date= driver1.find_element(By.XPATH, '//*[@id="caseTable"]/tbody/tr/td[4]').text



        order_link = WebDriverWait(driver1, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="caseTable"]/tbody/tr/td[2]/a[2]'))
        )
        driver1.execute_script("arguments[0].scrollIntoView(true);", order_link)
        time.sleep(1)
        driver1.execute_script("arguments[0].click();", order_link)
        time.sleep(2)
    except :
        party_name, next_Date, order_date, order_link = "Server Error", "Server Error", "Server Error", "Server Error"

        driver1.quit()
        exit()

    # Extract all order names, links & dates
    order_link = []
    order_date = []

    try:
        rows = driver1.find_elements(By.XPATH, '//*[@id="caseTable"]/tbody/tr')
        for i in range(1, len(rows) + 1):
            try:
                order = driver1.find_element(By.XPATH, f'//*[@id="caseTable"]/tbody/tr[{i}]/td[2]/a')
                date_data = driver1.find_element(By.XPATH, f'//*[@id="caseTable"]/tbody/tr[{i}]/td[3]')
                link = order.get_attribute('href')
                date = date_data.text.strip()


                order_link.append(link)
                order_date.append(date)
            except:
                party_name, next_Date, order_date, order_link = "Server Error", "Server Error", "Server Error", "Server Error"




    except:
        party_name = next_Date = "Server Error"
        order_link = order_date = ["Server Error"]
    finally:
        driver1.quit()
    return {
        "party_name": party_name,
        "order_dates": order_date,
        "order_links": order_link,
        "next_date": next_Date

    }






