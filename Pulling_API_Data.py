#Get setup a dotenv file
import os
import requests
from dotenv import load_dotenv


#Getting API keys 
load_dotenv()
API_KEY_NASA = os.getenv("API_KEY_NASA")
API_KEY_NOAA = os.getenv("API_KEY_NOAA")

#API key can be found by Going to the NASA data website and applying for one.
respones = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY_NASA}')

#There are a lot of status codes that can be returned. Here are the biggest ones we may encounter
#For the full list see this link: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# 200 => OK 
# 400 => bad Request
# 404 => Not Found
print(respones.status_code)
