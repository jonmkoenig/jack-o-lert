"""
This script pulls down all the upcoming movies, sorts them based on genre, 
strips out unwanted information and emails it to {you}
"""

import os
import json
import requests
import smtplib
from email.message import EmailMessage
from jinja2 import Template 
from datetime import date
from dotenv import load_dotenv
load_dotenv()

"""
Create a .dotenv in the same directory and settings in this format:
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
    """
    body_template = Template("""
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    .movie-container {
                        display: flex;
                        flex-direction: column;
                    }

                    .movie-container div {
                        padding: 10px;
                        margin: 7px 2px;
                    }

                    h1, h2 {
                        text-align: center;
                    }

                    .orange {
                        color: orange;
                    }

                    .title {
                        margin: 0px;
                    }

                    .date {
                        margin-top: 2px;
                    }
                </style>
            </head>
            <body>
                <h1>Hey, look! It's time for our spooky movie newsletter!</h1>
                <div class="movie-container">
                    {% for movie in stripped_movies %}
                    <div class="movie">
                    <h1 class="title orange">{{ movie.title }}</h1>
                    <h2 class="date orange">{{ movie.release_data}} </h2>
                    <p>{{ movie.overview }}</p>
                    <small>Original language: {{ movie.original_language }}</small>
                    </div>
                    {% endfor %}
                </div>
                <p>Psst.. Jon talks about you so much, I think he loves you! <3</p>
            </body>
        </html>
    """)
    body = body_template.render(stripped_movies=stripped_movies, current_date=current_date)

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
                "release_data": movie["release_date"]
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