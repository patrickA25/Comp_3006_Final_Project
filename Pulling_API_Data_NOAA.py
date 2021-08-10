#Get setup a dotenv file
import os
import requests
import datetime as datetime
import collections as collection
import json
from dotenv import load_dotenv

#Website to help with pulling data with API https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859

#Getting API keys 
load_dotenv()
API_KEY_NOAA = os.getenv("API_KEY_NOAA")

avg_temp_by_day = collection.namedtuple('AvgTempDay',('Location_name','Day','Avg_temp'))

#build the URL for getting data:
#Break down of URL sections
#https://www.ncdc.noaa.gov/cdo-web/api/v2/data? => static needs to be in every API call
#Datasetid=GHCND => this is the data base that the API will be calling
#datatypedi => this is that column of data that it will be returning
#limit = 1000 => the number of observation it will at most return
#units => for average temp will it be returned in F or C 
#stationid => the weather station ID value to pull data from
#start_date/end_date => start and end date of when to pull data from


r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&units=standard&stationid=GHCND:USW00023129&startdate=2015-01-01&enddate=2015-01-31', headers={'token':API_KEY_NOAA})
print(r.status_code)

d = json.loads(r.text)

dates_temp = []
temps = []
avg_temps = [item for item in d['results'] if item['datatype']=='TAVG']
dates_temp += [item['date'] for item in avg_temps]
temps += [item['value'] for item in avg_temps]

print(temps)



