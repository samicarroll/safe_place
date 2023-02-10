import secrets

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # check if the username and password match
    if username == 'dhs' and password == 'pass':
        session['username'] = username
        return redirect("/search")
    else:
        return redirect('/login')


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        selected_websites = request.form.get("websites")
        results = None
        if selected_websites == "megapersonals":
            results = megapersonals.scrap()
        elif selected_websites == "skip_the_games":
            results = skip_the_games.scrap()
        elif selected_websites == "craigslist":
            results = craigslist.scrap()
        elif selected_websites == "all":
            results = megapersonals.scrap() + skip_the_games.scrap() + craigslist.scrap()

    return render_template("search.html", results=results)


@app.route('/megapersonals')
def megapersonals():
    if 'username' in session:
        return render_template('megapersonals.html')
    else:
        return redirect('/login')


@app.route('/skip_the_games')
def skip_the_games():
    if 'username' in session:
        return render_template('skip_the_games.html')
    else:
        return redirect('/login')


@app.route('/craigslist')
def craigslist():
    if 'username' in session:
        return render_template('craiglist.py')
    else:
        return redirect('/login')


@app.route('/scraper')
def scraper():
    if 'username' in session:
        # do scraping here using BeautifulSoup, pandas and openpyxl
        return 'Search Page'
    else:
        return print("Error, please enter correct credentials")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
