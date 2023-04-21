import secrets
import datetime
import megapersonals_ftlaudy
import megapersonals_ftmyers
import megapersonals_miami
import megapersonals_sarasota
import megapersonals_tampa
import skip_the_games_ftmyers
import skip_the_games_miami
import skip_the_games_sarasota
import os
from flask import Flask, render_template, request, redirect, session
from flask import flash
from flask import url_for
import psycopg2
from urllib.parse import urlparse
import bcrypt

elephant_sql_url = "postgres://mblijolb:kK7X41hUBnVsUNS4NTj6Fl9xdCfmkHeb@baasu.db.elephantsql.com/mblijolb"
url = urlparse(elephant_sql_url)

db_name = url.path[1:]
db_user = url.username
db_password = url.password
db_host = url.hostname
db_port = url.port


def create_db_connection():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    return conn

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

def generate_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password_hash(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to database
        conn = create_db_connection()
        cursor = conn.cursor()

        # Query database for the user's credentials
        query = "SELECT * FROM users WHERE username=%s;"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Check if the user's credentials are correct
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect("/search")
        else:
            flash("Invalid username or password. Please try again.")
            return redirect('/login')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve submitted username and password
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = create_db_connection()
        cursor = conn.cursor()

        # Insert the new user into the database
        query = "INSERT INTO users (username, password) VALUES (%s, %s);"
        cursor.execute(query, (username, hashed_password))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect the user to the login page
        return redirect(url_for('login'))
    return render_template('register.html')
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
        "mega-personals-tpa": "MegaPersonals Tampa",
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
        if selected_websites and selected_keywords:  # Only proceed if both are selected
            for website in selected_websites:
                if website == "mega-personals":
                    import megapersonals_ftmyers
                    results.extend(megapersonals_ftmyers.run(selected_keywords))
                    excel_files.append(f'megapersonals_ftmyers_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
                elif website == "mega-personals-ftlaudy":
                    import megapersonals_ftlaudy
                    results.extend(megapersonals_ftlaudy.run(selected_keywords))
                    excel_files.append(f'megapersonals_ftlaudy_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
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
                elif website == "mega-personals-tpa":
                    import megapersonals_ftlaudy
                    results.extend(megapersonals_ftlaudy.run(selected_keywords))
                    excel_files.append(
                        f'megapersonals_ftlaudy_{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.xlsx')
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
    return render_template("search.html", websites=websites, keywords=keywords, results=results,excel_files=excel_files)


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
