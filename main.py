import requests
import os 
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

weather_api_key = os.environ['OW_API_KEY']

loc_params ={
    "q":"Poznań",
    "appid":weather_api_key
}

location = requests.get("http://api.openweathermap.org/geo/1.0/direct?", params=loc_params)
location.raise_for_status()

loc_data = location.json()

loc_lat = loc_data[0]["lat"]
loc_long = loc_data[0]["lon"]

weather_params ={
    "lat":loc_lat,
    "lon":loc_long,
    "units":"metric",
    "cnt":4,
    "appid":weather_api_key
}

weather = requests.get("https://api.openweathermap.org/data/2.5/forecast?", params=weather_params)
weather.raise_for_status()

weather_data = weather.json()

time_shift = weather_data["city"]["timezone"]//3600

conditions_list = []
rain_time = []

for i in range(weather_data["cnt"]):
    conditions = weather_data["list"][i]["weather"][0]["main"].lower()
    date = weather_data["list"][i]["dt_txt"].split(" ")
    date_hour = date[1].split(":")
    time_shifted = str(int(date_hour[0])+time_shift)+":"+date_hour[1]+":"+date_hour[2]
    if conditions == "rain":
        conditions_list.append(conditions)
        rain_time.append(time_shifted)
    else:
        conditions_list.append(conditions)

if "rain" in conditions_list:
    message = client.messages.create(
        body=f"Today you might expect rain at {', '.join(rain_time)}.",
        from_="placeholder for actual number",
        to="placeholder for actual number",

    )

