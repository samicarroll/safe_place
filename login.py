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
    results = []  # Initialize with empty list
    if request.method == "POST":
        selected_websites = request.form.getlist("websites")
        if "megapersonals" in selected_websites:
            from templates import megapersonals
            results.extend(megapersonals.scrap())
        if "skip_the_games" in selected_websites:
            from templates import skip_the_games
            results.extend(skip_the_games.scrap())
        if "craigslist" in selected_websites:
            from templates import craigslist
            results.extend(craigslist.scrap())
        if "all" in selected_websites:
            from templates import megapersonals
            from templates import skip_the_games
            from templates import craigslist
            results.extend(megapersonals.scrap())
            results.extend(skip_the_games.scrap())
            results.extend(craigslist.scrap())

    return render_template("search.html", results=results)


@app.route('/mega-personals')
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
    app.run(debug=True, port=5000)
