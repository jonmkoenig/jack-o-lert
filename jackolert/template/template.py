"""
This is a Jinja2 template file, we will inject our variables and then send this out with smtplib.
"""

template_string = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            * {
                text-align: center;
            }

            .movie {
                padding: 10px;
                margin: 30px auto;
                background: rgb(245, 245, 245);
                border-radius: 7px;
                max-width: 700px;
            }

            .title {
                margin-top: 20px;
            }
            
            .date {
                margin-top: 0px;
            }
            
            #intro {
                margin: 65px auto
            }
        </style>
    </head>
    <body>
    <h1 id="intro">New spooky movies! >:D</h1>
        <div class="movie-container">
            {% for movie in data %}
            <div class="movie">
                <h2 class="title">{{ movie.title }}</h2>
                <h3 class="date">{{ movie.release_data}}</h3>
                <img src="http://image.tmdb.org/t/p/w300{{ movie.poster_path }}"/>
                <p>{{ movie.overview }}</p>
                <p>Language: {{ movie.original_language }}</p>
            </div>
            {% endfor %}
        </div>
    </body>
</html>
"""
