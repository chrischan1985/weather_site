# weather_site
How to run the project:

1) First we need to sync the database with the defined models:

"python manage.py makemigrations subscribe"
"python manage.py migrate"

2) Install django-extensions

"pip install django-extensions"

3) Initialize database with top 100 most populated cities in US. These will become
 the options listed on our subscription page.

"python manage.py runscript init_db --dir-policy each"

4) To send email, first edit scripts/login.json with email login credentials. If you are
using Gmail, you have to enable "less secure app" in your gmail account first. Once that
is all done, run the following script:

"python manage.py runscript send_emails --dir-policy each"
