#Get setup a dotenv file
import os
import requests
import datetime as datetime
import json
from dotenv import load_dotenv

#Website to help with pulling data with API https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859

#Getting API keys 
load_dotenv()
API_KEY_NOAA = os.getenv("API_KEY_NOAA")
Token = API_KEY_NOAA
#Station ID for Denver CO
Stat_ID = 'GHCND:USW00023129'
#GHCND => Global Histoical Climatology network Daily
dataset_id = 'GHCND'
#TAVG => average temperature
datatype_id = 'TAVG'
#number of rows returned, defualt is 25 max is 1000
limit = 100
#start and end date
year = '2015'

#build the URL for getting data:

r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid=GHCND:USW00023129&startdate='+year+'-01-01&enddate='+year+'-01-31', headers={'token':Token})
print(r.status_code)

d = json.loads(r.text)
avg_temps = [item for item in d['results'] if item['datatype']=='TAVG']
print(avg_temps)



