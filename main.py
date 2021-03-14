"""
Template and example for serving HTML emails with Python and Jinja2.
"""

# Module imports
import requests
import smtplib
from jinja2 import Template
from email.message import EmailMessage

# This statement is importing our template file located in jack-o-lert/jackolert/template/template.py
from jackolert.template.template import *

"""
This statement is importing everything from jack-o-lert/jackolert/env.py -- this is where we keep sensitive information like your API query string 
and email addresses so that they can more easily be kept out of github with a .gitignore file. You will find a dummy file called env_dummy.py
in that directory, you should rename it to env.py and update the values before you continue.
"""
from jackolert.env import *

def main():
    """
    Defines the main program loop where all functions are called until the email is sent.
    """
    raw_api_data = requests.get(api_query).json()
    filterGenre(raw_api_data)
    filterMetadata(genre_filtered_movies)
    sendMail(final_movie_array)


def filterGenre(data):
    """
    Receives JSON and filters items out based on the 'genre_ids' field. Movies that have
    genres that we like are pushed to the 'filter_cache' array.
    """
    global genre_filtered_movies
    genre_filtered_movies = []
    if data:
        for movie in data["results"]:
            if (
                27 in movie["genre_ids"] or
                80 in movie["genre_ids"] or
                99 in movie["genre_ids"] or
                9648 in movie["genre_ids"] or
                53 in movie["genre_ids"]
            ):
                genre_filtered_movies.append(movie)
    else:
        print("No movies found!")
        exit(1)


def filterMetadata(data):
    """
    Strip out the unwanted information from the remaining movies and store them
    in the stripped_movies variable.
    """
    global final_movie_array
    final_movie_array = []
    for movie in data:
        new_item = {
                "title": movie["title"],
                "original_language": movie["original_language"],
                "overview": movie["overview"],
                "release_data": movie["release_date"],
                "poster_path": movie["poster_path"]
                }
        final_movie_array.append(new_item)


def sendMail(data):
    """
    Mixes the data and template together before sending out an email.
    """
    template = Template(template_string)
    rendered_template = template.render(data=data)

    msg = EmailMessage()
    msg["Subject"] = subject_of_email
    msg["From"] = sending_address
    msg["To"] = receiving_address
    msg.add_alternative(rendered_template, subtype="html")

    with smtplib.SMTP(smtp_address, 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sending_address, sending_address_password)
        smtp.send_message(msg)


if __name__ == "__main__":
    main()