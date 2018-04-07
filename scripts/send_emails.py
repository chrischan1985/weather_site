# script to send emails to all subscribed users, based on the weather conditions at the
# user's location
# To use this script: "python manage.py runscript send_emails --dir-policy each"
import smtplib
import json
from subscribe.models import User
from urllib.request import urlopen
from utils.helper import is_valid_email, is_valid_location, extract_city_state, contains


class Email:
    def __init__(self, sub, msg):
        self.sub = sub
        self.msg = msg

    def __str__(self):
        return f'Subject: {self.sub}\n\n{self.msg}'


class Weather:
    def __init__(self, location, temp_f, precip_1hr_in,
                 temp_high_avg, temp_low_avg, description):
        self.location = location
        self.temp_f = float(temp_f)
        self.precip_1hr_in = float(precip_1hr_in)
        self.temp_high_avg = float(temp_high_avg)
        self.temp_low_avg = float(temp_low_avg)
        self.description = description

    def is_nice(self):
        return (contains(self.description, 'sunny') or
                self.temp_f > (self.temp_high_avg + self.temp_low_avg) / 2.0 + 5.0)

    def is_bad(self):
        return ((self.precip_1hr_in > 0.0) or
                self.temp_f < (self.temp_high_avg + self.temp_low_avg) / 2.0 - 5.0)

    def __str__(self):
        return (f"{self.location} temp_f: {self.temp_f}, precip_1hr_in: {self.precip_1hr_in}, "
                f"temp_high_avg: {self.temp_high_avg}, "
                f"temp_low_avg: {self.temp_low_avg}, description: {self.description}")


class GetWeatherException(Exception):
    pass


def get_weather(city, state):
    url_now = f'http://api.wunderground.com/api/9bdafd735cb2389d/conditions/q/{state}/{city}.json'
    url_history = f'http://api.wunderground.com/api/9bdafd735cb2389d/almanac/q/{state}/{city}.json'
    try:
        f = urlopen(url_now)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        temp_f = parsed_json['current_observation']['temp_f']
        precip_1hr_in = parsed_json['current_observation']['precip_1hr_in']
        description = parsed_json['current_observation']['weather']
        f.close()
        f = urlopen(url_history)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        temp_high_avg = parsed_json['almanac']['temp_high']['normal']['F']
        temp_low_avg = parsed_json['almanac']['temp_low']['normal']['F']
    except Exception as e:
        raise GetWeatherException("GetWeatherException: could not"
                                  " retrieve whether conditions")
    else:
        location = city + ", " + state
        return Weather(location, temp_f, precip_1hr_in,
                       temp_high_avg, temp_low_avg, description)


def generate_email(location):
    city, state = extract_city_state(location)
    weather = get_weather(city, state)
    if weather.is_nice():
        subject = "It's nice out! Enjoy a discount on us."
    elif weather.is_bad():
        subject = "Not so nice out? That's okay, enjoy a discount on us."
    else:
        subject = "Enjoy a discount on us."
    message = f'I see you are in {location}. Current weather: {weather.temp_f} degrees, {weather.description}.'
    return Email(subject, message)


def send_email(dest, email):
    login_json = json.load(open('login.json'))
    try:
        server = smtplib.SMTP(login_json['smtp_server'])
        server.ehlo()
        server.starttls()
        server.login(login_json['user_email'], login_json['user_password'])
        server.sendmail(login_json['user_email'], dest, str(email))
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email failed to send" + str(e))


def run():
    # For each subscribed user in our database, lookup the weather at
    # their location, create a personalized email and send
    users = User.objects.all()
    for u in users:
        if not is_valid_location(u.location.name) or not is_valid_email(u.email):
            continue
        try:
            email = generate_email(u.location.name)
        except GetWeatherException as e:
            print(f'Failed to generate email. {str(e)}. Ignoring user {u.email}')
            continue
        else:
            print(email)
            send_email(u.email, email)
