import requests, os
from twilio.rest import Client


#initialize global variables
#input relevant twilio SID/TOKEN/NUMBER, send to number, openweathermap API and LAT/LONG
SID = os.getenv('TWILIO_SID')
TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_NUM = os.getenv('TWILIO_NUM')
PERSONAL_NUM = os.getenv('PERSONAL_NUM')
API_KEY = os.getenv('WEATHER_API')
LAT = 37
LON = 116
RAIN = False
PARAMETERS = {
    'lat': LAT,
    'lon': LON,
    'exclude': 'current,minutely,daily',
    'appid': API_KEY,
}
RESPONSE = requests.get(url='http://api.openweathermap.org/data/2.5/onecall', params=PARAMETERS)


#post response relevant data
RESPONSE.raise_for_status()
print(RESPONSE.raise_for_status)
DATA = RESPONSE.json()
WEATHER_SLICE = DATA['hourly'][:12]
WEATHER_STATUS = DATA['hourly'][0]['weather'][0]['main']


#determine id code
for items in WEATHER_SLICE:
    id_code = DATA['hourly'][0]['weather'][0]['id']
    if int(id_code) < 700:
        RAIN = True


#if it will rain then send message to designated number.
if RAIN:
    client = Client(SID, TOKEN)
    message = client.messages \
        .create(
            body=f'Don\'t forget your umbrella! Expect: {WEATHER_STATUS}',
            from_=TWILIO_NUM,
            to=PERSONAL_NUM)
    print(message.status)