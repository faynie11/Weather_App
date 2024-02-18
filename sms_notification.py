from configparser import ConfigParser
import requests
from twilio.rest import Client
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']
account_sid = #Here provide sid from Twillio
auth_token = #Here provide token from Twillio
# for SMS notification for Kraków

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
weather_params = {
    "lat": 50.064651,
    "lon": 19.944981,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
wea_data = response.json()

will_rain = False
for hour_data in wea_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today in Kraków!🌧️",
        from_='+12132933923',
        to='+48530561407'
    )
    print(message.status)
