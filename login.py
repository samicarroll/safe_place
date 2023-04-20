import secrets
import datetime
import megapersonals_ftmyers
import megapersonals_miami
import megapersonals_sarasota
import skip_the_games_ftmyers
import skip_the_games_miami
import skip_the_games_sarasota
import os
from flask import Flask, render_template, request, redirect, session
from flask import flash


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


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
    with open(resource_path('static/keywords.txt')) as f:
        keywords = f.read().splitlines()
    return keywords


@app.route("/search", methods=["GET", "POST"])
def search():
    websites = {
        "mega-personals": "MegaPersonals",
        "mega-personals-mia": "MegaPersonals Miami",
        "mega-personals-sota": "MegaPersonals Sarasota",
        "skip_the_games_ftmyers": "Skip The Games Fort Myers",
        "skip_the_games_miami": "Skip the Games Miami",
        "skip_the_games_sarasota": "Skip the Games Sarasota",
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
                    import megapersonals_ftmyers
                    results.extend(megapersonals_ftmyers.run(selected_keywords))
                    excel_files.append(f'megapersonals_ftmyers_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "mega-personals-mia":
                    import megapersonals_miami
                    results.extend(megapersonals_miami.run(selected_keywords))
                    excel_files.append(f'megapersonals_mia_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "mega-personals-sota":
                    import megapersonals_sarasota
                    results.extend(megapersonals_sarasota.run(selected_keywords))
                    excel_files.append(f'megapersonals_sarasota_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "skip_the_games_ftmyers":
                    import skip_the_games_ftmyers
                    results.extend(skip_the_games_ftmyers.run(selected_keywords))
                    excel_files.append(f'skip_the_games_ftmyers{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "skip_the_games_miami":
                    import skip_the_games_miami
                    results.extend(skip_the_games_miami.run(selected_keywords))
                    excel_files.append(f'skip_the_games_miami{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "skip_the_games_sarasota":
                    import skip_the_games_sarasota
                    results.extend(skip_the_games_sarasota.run(selected_keywords))
                    excel_files.append(f'skip_the_games_sarasota{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')



    if request.method == "POST" and results:
        flash("Web scraping complete")
    return render_template("search.html", websites=websites, keywords=keywords, results=results,
                           excel_files=excel_files)


def run_scrapers(websites, keywords):
    results = []
    if "mega-personals" in websites:
        # Call the function from your megapersonals ftmyers script
        # Make sure to import your megapersonals module at the beginning of your main Flask app file
        megapersonals_ftmyers.run(keywords)
    if "mega-personals-mia" in websites:
        # Call the function from your megapersonals miami script
        # Make sure to import your megapersonals module at the beginning of your main Flask app file
        megapersonals_miami.run(keywords)
    if "mega-personals-sota" in websites:
        # Call the function from your megapersonals sarasota script
        # Make sure to import your megapersonals module at the beginning of your main Flask app file
        megapersonals_sarasota.run(keywords)
    if "skip_the_games_ftmyers" in websites:
        # Call the function from your skip_the_games_ftmyers script
        # Make sure to import your skip_the_games module at the beginning of your main Flask app file
        skip_the_games_ftmyers.run(keywords)
    if "skip_the_games_miami" in websites:
        # Call the function from your skip_the_games_miami script
        # Make sure to import your skip_the_games module at the beginning of your main Flask app file
        skip_the_games_miami.run(keywords)
    if "skip_the_games_sarasota" in websites:
        # Call the function from your skip_the_games_sarasota script
        # Make sure to import your skip_the_games module at the beginning of your main Flask app file
        skip_the_games_sarasota.run(keywords)

    return results


@app.route('/search-results', methods=['POST'])
def search_results():
    selected_websites = request.form.getlist('websites[]')
    selected_keywords = request.form.getlist('keywords[]')

    # Run the scraping functions based on the selected websites and keywords
    results = run_scrapers(selected_websites, selected_keywords)

    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run()
