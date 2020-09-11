template_file = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            * {
                text-align: center;
            }

            .movie-container div {
                padding: 10px;
                margin: 30px auto;
                background: rgb(245, 245, 245);
                border-radius: 7px;
                max-width: 700px;
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
        <div class="movie-container">
            {% for movie in stripped_movies %}
            <div class="movie">
                <h1 class="title orange">{{ movie.title }}</h1>
                <h2 class="date orange">{{ movie.release_data}} </h2>
                <img src="http://image.tmdb.org/t/p/w300{{ movie.poster_path }}"/>
                <p>{{ movie.overview }}</p>
                <small>Original language: {{ movie.original_language }}</small>
            </div>
            {% endfor %}
        </div>
        <p>{{quote}}</p>
    </body>
</html>
"""
