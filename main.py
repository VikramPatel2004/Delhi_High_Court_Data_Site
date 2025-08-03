from flask import Flask, render_template, request
from status import details
from judgement import judgement, get_case_list
from filing_date import get_filing_date
from datetime import datetime
import sqlite3
import os

app = Flask(__name__, instance_relative_config=True)


# os.makedirs(app.instance_path, exist_ok=True)

# DB path
DB_PATH = os.path.join(app.instance_path, 'case.db')

# ------------------ Create Fresh Table If Needed ------------------
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS case_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             party_name TEXT,
#             filing_date TEXT,
#             registration_date TEXT,
#             order_links TEXT,
#             judgement_link TEXT,
#             hearing_date TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# init_db()

# ------------------ Log to DB ------------------
def log_case_data(party_name, filing_date, reg_date, order_dates, order_links, judgment_link, hearing_date):
    combined_links = [f"{date}: {link}" for date, link in zip(order_dates, order_links)]
    formatted_links = '\n'.join(combined_links)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO case_logs (
            party_name, filing_date, registration_date,
            order_links, judgement_link, hearing_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        party_name,
        filing_date,
        reg_date,
        formatted_links,
        judgment_link,
        hearing_date
    ))
    conn.commit()
    conn.close()

# ------------------ Home Route ------------------
@app.route("/", methods=["GET", "POST"])
def home():
    case_list = get_case_list()
    if request.method == "POST":

        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        case_year = request.form.get("case_year")
        try:
            response1 = details(case_number, case_year, case_type)
        except Exception as e:
            print(" Error:", e)
            error_msg = "Something went wrong while fetching case details. Please try again."
            return render_template("home.html", case_list=case_list, current_year=datetime.now().year, error=error_msg)

        response2 = judgement(case_type, case_number, case_year)
        filing_data = get_filing_date(case_type, case_number, case_year)

        party_name = response1["party_name"]
        order_date = response1["order_dates"]
        order_link = response1["order_links"]
        next_date = response1["next_date"]
        judgement_link = response2["Judgment PDF"]
        filing_date = filing_data["filing_date"]
        registration_date = filing_data["registeration_date"]

        zipped_orders = zip(order_date, order_link)

        log_case_data(
            party_name=party_name,
            filing_date=filing_date,
            reg_date=registration_date,
            order_dates=order_date,
            order_links=order_link,
            judgment_link=judgement_link,
            hearing_date=next_date
        )

        return render_template(
            "result.html",
            party_name=party_name,
            filing_date=filing_date,
            registeration_date=registration_date,
            order_date=order_date,
            order_link=order_link,
            next_date=next_date,
            judgement_link=judgement_link,
            zipped_orders=zipped_orders
        )


    return render_template("home.html", case_list=case_list, current_year=datetime.now().year)


if __name__ == "__main__":
    app.run(debug=True)
