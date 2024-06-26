from flask import Flask, render_template
from main import get_dates, get_date_info
from database import DatabaseOperations
app = Flask(__name__)

@app.route("/")
def dates_render():
    dates = get_dates().json()["message"]
    DatabaseOperations().createAllDatesDatabase()
    DatabaseOperations().addDates(dates)
    return render_template("dates.html", dates_count = len(dates), dates = dates)
@app.route("/dates/<date>")
def date_render(date):
    date_info = get_date_info(str(date)).json()["message"]
    DatabaseOperations().createDateInfoDatabase()
    DatabaseOperations().addDateInfo(get_date_info(str(date)).json())
    count = date_info["flats_count"]["data"]
    windows_per_floor = date_info["windows_for_flat"]["data"]
    #print(*windows_per_floor)
    return render_template("date.html", date_info=date_info, windows = [[[True, 1], [True, 2]], [[False, 1], [True, 1]], [[True, 1], [False, 11]]], date=date, numbers='1, 2' , count_numbers=count, rooms_per_floor=1, windows_per_floor=" ".join(windows_per_floor))

def main():
    app.run(port=5000, host='127.0.0.1', debug=True)

if __name__ == '__main__':
    main()
