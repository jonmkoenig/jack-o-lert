### SETUP

Start by cloning the repository.

```sh
git clone https://github.com/jonmkoenig/jack-o-lert
```

Move to the jack-o-lert directory and create a virtual environment.

```sh
python3 -m venv venv
```

Activate the virtual environment.

```sh
source venv/bin/activate
```

Finally, install the project dependencies.

```sh
pip install -r requirements.txt
```

We are using [python-dotenv](https://pypi.org/project/python-dotenv/), so create a .env file and populate it with your own email settings.

```sh
# SMTP address of the server you are sending from.
smtp_address = "smtp_address"

# Sending address.
email_address = "email_address"

# Subject of the email.
subject = "subject"

# Receiving address.
target_address = "target_address"

# App password for accounts with 2FA.
app_password = "app_password"
```

If you want to send the email to multiple people you can use a comma separated list instead.

```sh
target_address = "freddy@gmail.com", "jason@gmail.com"
```

Lastly, modify jack-o-lert.py to make some API calls and change template.py to better suit your data.

### EXAMPLE

In my example, I make an API call to retrieve a list of movies, parse the information by running it through two functions to keep only the information that I need, and then use a [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/templates/) template to format that information and make it look a little better.
