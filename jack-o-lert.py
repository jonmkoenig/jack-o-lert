"""
A template for emailing stuff with Python & Jinja2.
"""

import os
import json
import requests
import smtplib

# quotes & random are used for my example only.
import quotes
import random

from email.message import EmailMessage
from datetime import date
from dotenv import load_dotenv
current_date = date.today()

"""

Jinja2 is used to build an email later in the script, so we import Template
from jinja2.

template_file is the actual Jinja2 template that you need to create, kept in a separate file to make it
more private. It looks like this:

template_file = '''
<html>
    <body>
        <div class="main-content">
            <p>Words words</p>
            <p>{{stuff}}</p>
        </div>
    </body>
</html>
'''

"""
from jinja2 import Template
from template import template_file

load_dotenv()

"""

The script is using python-dotenv, so create a .env file and fill out the
settings below in this format:

email_address = "address@gmail.com"

"""
# SMTP address of the server you are sending from.
smtp_address = os.environ.get("smtp_address")

# Sending address.
email_address = os.environ.get("email_address")

# Subject of the email.
subject = os.environ.get("subject")

# Receiving address.
target_address = os.environ.get("target_address")

# App password for accounts with 2FA.
app_password = os.environ.get("app_password")

# These settings and variables are used for my own example and are not
# necessary to keep in your script.
api_query = os.environ.get("api_query")
stripped_movies = []
filter_cache = []

def sendMail():
    """
    Mixes the data and template together before sending out an email.
    """
    body_template = Template(template_file)
    body = body_template.render(stripped_movies=stripped_movies,
            current_date=current_date, quote=random.choice(quotes.quotes))

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = target_address
    msg.add_alternative(body, subtype="html")

    with smtplib.SMTP(smtp_address, 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_address, app_password)
        smtp.send_message(msg)

# The functions below are used for my example only.
def filterMetadata():
    """
    Strip out the unwanted information from the remaining movies and store them
    in the stripped_movies variable.
    """
    for movie in filter_cache:
        stripped_movie = {
                "title": movie["title"],
                "original_language": movie["original_language"],
                "overview": movie["overview"],
                "release_data": movie["release_date"],
                "poster_path": movie["poster_path"]
                }
        stripped_movies.append(stripped_movie)
    sendMail()

def filterGenre():
    """
    Filter the movies and store the results in the filter_cache variable.
    """
    if (list):
        for movie in list["results"]:
            if 27 in movie["genre_ids"]:
                filter_cache.append(movie)
    else:
        print("No movies found!")
    filterMetadata()

# The list variable represents our data and is used for my example only.
list = requests.get(api_query).json()

filterGenre()
