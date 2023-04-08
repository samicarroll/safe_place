import secrets
import datetime
import megapersonals
import skip_the_games
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from flask import Flask, render_template, request, redirect, session
from flask import flash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def setup():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)


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
    with open('static/keywords.txt', 'r') as f:
        keywords = f.read().splitlines()
    return keywords


@app.route("/search", methods=["GET", "POST"])
def search():
    websites = {
        "mega-personals": "MegaPersonals",
        "skip_the_games": "Skip The Games",
    }
    keywords = get_keywords()
    results = []
    excel_files = []

    if request.method == "POST":
        print("POST request received")  # Debugging print statement
        selected_websites = request.form.getlist("websites")
        selected_keywords = request.form.getlist("keywords")
        print(f"Selected websites: {selected_websites}")  # Debugging print statement
        print(f"Selected keywords: {selected_keywords}")  # Debugging print statement
        if selected_websites and selected_keywords:  # Only proceed if both are selected
            for website in selected_websites:
                if website == "mega-personals":
                    import megapersonals
                    results.extend(megapersonals.run(selected_keywords))
                    excel_files.append(f'megapersonals_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "skip_the_games":
                    import skip_the_games
                    results.extend(skip_the_games.run(selected_keywords))
                    excel_files.append(f'skip_the_games_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')

    if request.method == "POST" and results:
        flash("Web scraping complete")
    return render_template("search.html", websites=websites, keywords=keywords, results=results,
                           excel_files=excel_files)


def run_scrapers(websites, keywords):
    results = []

    if "mega-personals" in websites:
        # Call the function from your megapersonals script
        # Make sure to import your megapersonals module at the beginning of your main Flask app file
        mega_results = megapersonals.run(keywords)
        results.extend(mega_results)

    if "skip_the_games" in websites:
        # Call the function from your skip_the_games script
        # Make sure to import your skip_the_games module at the beginning of your main Flask app file
        stg_results = skip_the_games.run(keywords)
        results.extend(stg_results)

    return results


@app.route('/search-results', methods=['POST'])
def search_results():
    selected_websites = request.form.getlist('websites[]')
    selected_keywords = request.form.getlist('keywords[]')

    # Run the scraping functions based on the selected websites and keywords
    results = run_scrapers(selected_websites, selected_keywords)

    return render_template('search.html', results=results)


if __name__ == '__main__':
    from waitress import serve

    app.run()
