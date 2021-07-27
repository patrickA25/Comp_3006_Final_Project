#Get setup a dotenv file

import requests
#https://github.com/theskumar/python-dotenv

#API key can be found by Going to the NASA data website and applying for one.
respones = requests.get("https://api.nasa.gov/planetary/apod?api_key=API_KEY")

#There are a lot of status codes that can be returned. Here are the biggest ones we may encounter
#For the full list see this link: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# 200 => OK 
# 400 => bad Request
# 404 => Not Found
print(respones.status_code)
