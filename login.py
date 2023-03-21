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


def get_keywords():
    with open('keywords.txt', 'r') as f:
        keywords = f.read().splitlines()
    return keywords


@app.route("/search", methods=["GET", "POST"])
def search():
    websites = {
        "mega-personals": "MegaPersonals",
        "skip_the_games": "Skip The Games",
        "craigslist": "Craigslist"
    }
    keywords = get_keywords()
    results = []
    if request.method == "POST":
        selected_websites = request.form.getlist("websites")
        selected_keywords = request.form.getlist("keywords")
        if selected_websites and selected_keywords:  # Only proceed if both are selected
            for website in selected_websites:
                if website == "mega-personals":
                    from templates import megapersonals
                    results.extend(megapersonals.scrap(selected_keywords))
                elif website == "skip_the_games":
                    from templates import skip_the_games
                    results.extend(skip_the_games.scrap(selected_keywords))
                elif website == "craigslist":
                    from templates import craigslist
                    results.extend(craigslist.scrap(selected_keywords))

    return render_template("search.html", websites=websites, keywords=keywords, results=results)


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
    app.run(debug=True, port=5000)

