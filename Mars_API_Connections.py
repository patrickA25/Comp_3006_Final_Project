import json, os, requests
from logging import currentframe
from dotenv import load_dotenv

# API Key
load_dotenv()
API_KEY_INSIGHT = os.getenv("API_KEY_INSIGHT")
API_URL_CURIOSITY = os.getenv("CURIOSITY_API")

class MarsWeather:
    def __init__(self):
        pass

class MarsWeatherData:
    def __init__(self):
        pass


# InSight URL
#insightResponse = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={API_KEY_INSIGHT}&feedtype=json&ver=1.0')

# Curiosity URL
curiosityResponse = requests.get(f'{API_URL_CURIOSITY}')
curiosityResponse.raise_for_status()
curiosityData = json.loads(curiosityResponse.text)

min_temps = [curiosityData['soles'][i]['min_temp'] for i in range(0, len(curiosityData['soles']))]
max_temps = [curiosityData['soles'][i]['max_temp'] for i in range(0, len(curiosityData['soles']))]
