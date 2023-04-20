import secrets
import datetime
import megapersonals
import skip_the_games
import os
from selenium import webdriver
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
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chromedriver_binary = "/Applications/Google Chrome.app/Contents/MacOS/chromedriver"


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
        megapersonals.run(keywords)
    if "skip_the_games" in websites:
        # Call the function from your skip_the_games script
        # Make sure to import your skip_the_games module at the beginning of your main Flask app file
        skip_the_games.run(keywords)

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
