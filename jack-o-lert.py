"""
Retrieves upcoming horror movies from TMBD and sends HTML emails.

Options set with dotenv.
Template pulled in from template.py
"""

import os
import json
import requests
import smtplib
import random
import quotes
from email.message import EmailMessage
from jinja2 import Template
from datetime import date
from dotenv import load_dotenv
from template import template_file
load_dotenv()

"""
Create a .dotenv in the same directory, settings are in this format:
email_address = "me@gmail.com"
"""
email_address = os.environ.get("email_address")
target_address = os.environ.get("target_address")
app_password = os.environ.get("app_password")
smtp_address = os.environ.get("smtp_address")
api_query = os.environ.get("api_query")
contacts = os.environ.get("contacts")
current_date = date.today()
stripped_movies = []
filter_cache = []

# Get all upcoming movies in JSON.
list = requests.get(api_query).json()

def sendMail():
    """

    Format an email with Jinja2, then finish creating setting options with EmailMessage.
    Append the finished template to the email using add_alternative and send it out.

    template_file is a python file in the same directory that is imported and
    used to format our data. It looks like this:

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
    ..ETC

    """
    body_template = Template(template_file)
    body = body_template.render(stripped_movies=stripped_movies,
            current_date=current_date, quote=random.choice(quotes.quotes))

    msg = EmailMessage()
    msg["Subject"] = "Spooky movies? ;)"
    msg["From"] = email_address
    msg["To"] = target_address
    msg.add_alternative(body, subtype="html")

    with smtplib.SMTP(smtp_address, 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_address, app_password)
        smtp.send_message(msg)

def filterMetadata():
    """
    Take the filter_cache and strip out all of the unwanted
    information, resulting in a list of dictionaries, stripped_movies.
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
    Take the list and filter out everything but spooky movies. Store the
    results in filter_cache.
    """
    if (list):
        for movie in list["results"]:
            if 27 in movie["genre_ids"]:
                filter_cache.append(movie)
    else:
        print("No movies found!")
    filterMetadata()

filterGenre()
