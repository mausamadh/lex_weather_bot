import json

import logging
from botocore.vendored import requests
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def unix_to_date(timestamp,timezone):
    time= int(timestamp)+ int(timezone)
    value = datetime.datetime.fromtimestamp(time)
    my_date = f"{value:%Y-%m-%d %H:%M:%S}"
    return my_date

def pascal_to_atm(pascal):
    atm = pascal / 101325
    return atm

def weather_information(cityName):
    my_api = "47f27f0ce614fe72a7adc915548c5e9f"
    url = "http://api.openweathermap.org/data/2.5/weather?q="+cityName+"&APPID="+my_api+"&units=metric"

    api_result = requests.get(url)
    result_json = api_result.json()
    # weather_result contains informations like temperature , min-temp , max-temp , feels-like temp , pressure , sea level , ground level , visibility
    weather_result = result_json["main"]
    temperature = weather_result["temp"]
    pressure = weather_result["pressure"]
    humidity = weather_result["humidity"]
    weather_description = result_json["weather"][0]["description"]

    timezone = result_json['timezone']

    #time details it includes sunrise time sunset time in unix time system and country
    timedetails = result_json['sys']
    sunrise_time = unix_to_date(timedetails['sunrise'],timezone)
    sunset_time = unix_to_date(timedetails['sunset'],timezone)


    return {
        "temperature": temperature,
        "humidity":humidity,
        "pressure":pressure,
        "weather_description": weather_description,
        "sunrise_time":sunrise_time,
        "sunset_time":sunset_time
    }


def lambda_handler(event, context):
    logger.debug(event)

    city = event["currentIntent"]["slots"]["city"]
    # city = event['city']

    result = weather_information(city)

    return {
        "sessionAttributes":event["sessionAttributes"],
        'dialogAction':{
            'type':'Close',
            'fulfillmentState':'Fulfilled',
            'message':{
                'contentType':'PlainText',
                'content':"The "+city+" has Temprature "+str(result["temperature"])+" degree celcius. \n The Pressure is "+str(result['pressure']) +\
                "Pa \n weather description is "+result['weather_description']+" The sunrising time is "+ str(result['sunrise_time'])+" Humidity is "+str(result['humidity'])+" Percentage"
            }
        }
    }
