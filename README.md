# Delhi_High_Court_Data_Scraper

Court Choosen : Delhi High Court

A web automation tool that extracts court orders from Delhi High Court website. It supports pagination, handles CAPTCHA.


📌 Features

✅ Scrapes court orders from Delhi High Court

🔁 Handles pagination to extract multiple orders

🧩 CAPTCHA strategy : I dont have to use any external service to solve captcha because this website captcha strategy is very easy

they use security code as captcha and shows some random no. as image for user to enter .That security code is available in sorce
html So i Just scrape it from There.

🧱 Tech Stack

Language: Python 3.10

Libraries/Tools/Module: "requests", selenium webdriver, 'flask', jinja template etc

CI/CD: GitHub Actions

🚀 Setup Instructions

##create virtual environment 
python -m venv venv 
##Activate virtual environment 
source venv/bin/activate # On Windows: venv\Scripts\activate 
##Install requirements 
pip install -r requirements.txt

## For clone
git clone https://github.com/VikramPatel2004/Delhi_High_Court_Data_Site.git


Run

python main.py

🔧 Prerequisites

Python 3.10+

GitHub account (to fork/clone)
