
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")


def main():
    app.run(port=8129, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
