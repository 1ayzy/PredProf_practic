from flask import Flask, render_template
from main import get_dates, get_date_info

app = Flask(__name__)

@app.route("/")
def base():
    dates = get_dates().json()["message"]
    return render_template("base.html", dates_count = len(dates), dates = dates)

def main():
    app.run(port=8129, host='127.0.0.1', debug=True)

if __name__ == '__main__':
    main()
