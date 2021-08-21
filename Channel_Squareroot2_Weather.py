from logging import error
import os
import requests
import datetime
import json
import collections as collection
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import numpy as np
import statistics
import csv

# Getting API Key from .env file
load_dotenv()
API_KEY_NOAA = os.getenv("API_KEY_NOAA")
API_URL_CURIOSITY = os.getenv("CURIOSITY_API")

# Earth-related classes
class NOAA_Data():

    def __init__(self,year,location,season):
        self.year = str(year)
        self.location = str(location)
        self.season = str(season)
        self.__build_API_Call()
        self.__extracting_data()
        
    def __build_API_Call(self):
        if self.season == 'Spring':
            #Spring start =>'-3-1' Spring_end=>'-5-31'
            self.API_call = f'''https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&limit=1000&
            units=metric&stationid=GHCND:{self.location}&startdate={self.year}-03-01&enddate={self.year}-05-31'''
        elif self.season == 'Summer':
            #Spring start =>'-6-1' Spring_end=>'-8-31'
            self.API_call = f'''https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&limit=1000&units=standard&stationid=GHCND:{self.location}&startdate={self.year}-06-01&enddate={self.year}-08-31'''
        elif self.season == 'Fall':
            #Spring start =>'9-1' Spring_end=>'11-30'
            self.API_call = f'''https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&limit=1000&units=standard&stationid=GHCND:{self.location}&startdate={self.year}-09-01&enddate={self.year}-11-30'''
        elif self.season == 'Winter':
            #Spring start =>'12-1' Spring_end=>'2-28'
            self.API_call = f'''https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&limit=1000&units=standard&stationid=GHCND:{self.location}&startdate={self.year}-12-01&enddate={str(int(self.year)+1)}-02-28'''
        else:
            raise ValueError('Season not found, please check inputes.')
        self.r = requests.get(self.API_call,headers={'token':API_KEY_NOAA})
        if self.r.status_code != 200:
            raise ValueError(f'API call did not return statuse code of 200 it returned {self.r.status_code}')
        self.E_weather = json.loads(self.r.text)
    
    def __extracting_data(self):
        #Still need to make the for loop that will add the data to the named tuple
        self.temp_list_day = sorted(list(set(([item['date'][0:10] for item in self.E_weather['results'] ]))))
        self.temp_list_min = ([item['value'] for item in self.E_weather['results'] if item['datatype']=='TMAX'])
        self.temp_list_max = ([item['value'] for item in self.E_weather['results'] if item['datatype']=='TMIN'])


        self.date_array = (np.array(self.temp_list_day,dtype='datetime64'))
        self.min_array = (np.array(self.temp_list_max))
        self.max_array = (np.array(self.temp_list_min))
        self.avg_array = np.add(self.min_array,self.max_array)/2
        
    def explor_graph(self):
        plt.plot(self.date_array,self.min_array,label='Min Temp')
        plt.plot(self.date_array,self.max_array,label='Max Temp')
        plt.plot(self.date_array,self.avg_array,label ='Avg Temp')
        plt.legend()
        plt.show()
    
    def CSV_output(self):
        pass


# Mars-related classes
class Curiosity_Data():

    def __init__(self, year, season):
        self.year = year
        self.season = season
        self.curiosity_data = []

        self.__retrieve_data()
        self.__process_data()
        self.__explore_data()


    # Data processing function
    def __retrieve_data(self):  

        #logging.info('Calling Curiosity')
        self.curiosity_response = requests.get(f'{API_URL_CURIOSITY}')
        self.curiosity_response.raise_for_status()
        curiosity_JSON = json.loads(self.curiosity_response.text) # Loads as a dictionary with 2 key; description and soles
        self.sol_data = curiosity_JSON['soles']

    def __process_data(self):
        
        season_dict = {'Winter': {'first': '12-01', 'last': '02-28'}, 'Spring': {'first': '03-01', 'last': '05-31'}, 'Summer': {'first': '06-01', 'last': '08-31'}, 'Fall': {'first': '07-01', 'last': '11-30'}}
        first_day_dt = datetime.date.fromisoformat(str(str(self.year) + '-' + season_dict[self.season]['first']))
        last_day_dt = datetime.date.fromisoformat(str(str(self.year + 1) + '-' + season_dict[self.season]['last']) if self.season == 'Winter' else str(str(self.year) + '-' + season_dict[self.season]['last']))

        mars_record = collection.namedtuple('mars_record', 'earth_date, sol, season, min_temp, max_temp, ave_temp, atmo_opacity, pressure, sunrise, sunset, daylight')
        ave_min = statistics.mean([int(sol['min_temp']) for sol in self.sol_data if sol['min_temp'] != '--'])
        ave_max = statistics.mean([int(sol['max_temp']) for sol in self.sol_data if sol['max_temp'] != '--'])
        ave_pressure = statistics.mean([int(sol['pressure']) for sol in self.sol_data if sol['pressure'] != '--'])
        
        for sol in self.sol_data:
            if sol['min_temp'] == '--' or sol['max_temp'] == '--' or sol['pressure'] == '--': # It's all or nothing with these 3 attributes
                sol['min_temp'] = ave_min
                sol['max_temp'] = ave_max
                sol['pressure'] = ave_pressure

            earth_date = sol['terrestrial_date'].split('-') # Converting string to datetime.date object
            earth_date_datetime = datetime.date(int(earth_date[0]), int(earth_date[1]), int(earth_date[2]))
            
            sunrise = sol['sunrise'].split(':') # Converting string to datetime.time object
            sunrise_datetime = datetime.time(int(sunrise[0]), int(sunrise[1]))
            
            sunset = sol['sunset'].split(':') # Converting string to datetime.time object
            sunset_datetime = datetime.time(int(sunset[0]), int(sunset[1]))
            
            dateTimeA = datetime.datetime.combine(datetime.date.today(), sunset_datetime)
            dateTimeB = datetime.datetime.combine(datetime.date.today(), sunrise_datetime)
            dateTimeDifference = dateTimeA - dateTimeB
            daylight = dateTimeDifference.total_seconds() / 3600

            if first_day_dt <= earth_date_datetime <= last_day_dt: # Filter by date/season
                self.curiosity_data.append(mars_record(earth_date_datetime, int(sol['sol']), sol['season'], int(sol['min_temp']), int(sol['max_temp']), int((int(sol['min_temp'])+int(sol['max_temp']))/2), sol['atmo_opacity'], int(sol['pressure']), sunrise_datetime, sunset_datetime, daylight))
    
    def __explore_data(self):
# ~~~~~~~~~~~~~~~~~~~~~~~~~ NEED TO FINISH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.min_temps = [data.min_temp for data in self.curiosity_data]
        self.max_temps = [data.max_temp for data in self.curiosity_data]
        self.ave_temps = [data.ave_temp for data in self.curiosity_data]
# ~~~~~~~~~~~~~~~~~~~~~~~~~ NEED TO FINISH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Merged Data Sets
class Root_Two_Report(): # All humans are vermin in the eyes of Morbo...
    def __init__(self, earth_data, mars_data):
        
        earth_datetime = []
        for date in earth_data.date_array:
            earth_datetime.append(datetime.date.fromisoformat(str(date)))
        
        self.earth_data = zip(earth_datetime, earth_data.min_array, earth_data.max_array)
        self.mars_data = mars_data
        self.earth_mars_data = collection.defaultdict(dict)
        self.__merge_data()
        self.__export_data()

    def __merge_data(self):

        for data in self.earth_data:
            self.earth_mars_data[data[0]]['earth_min'] = data[1]
            self.earth_mars_data[data[0]]['earth_max'] = data[2]

        for data in self.mars_data.curiosity_data:
            self.earth_mars_data[data.earth_date]['mars_min'] = data.min_temp
            self.earth_mars_data[data.earth_date]['mars_max'] = data.max_temp

    def __export_data(self):
        field_names = ['date', 'earth_min', 'earth_max', 'mars_min', 'mars_max']

        with open('Root2Report.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, field_names)
            writer.writeheader()
            #fields = sorted(earth_mars_data.values()[0])
            for key, value in sorted(self.earth_mars_data.items()):
                row = {'date': key}
                row.update(value)
                writer.writerow(row)


cData = Curiosity_Data(2017, 'Summer')
test_data_pull = NOAA_Data(2017,'USW00003167','Summer')
#for data in cData.curiosity_data:
    #print(data.min_temp)

Root_Two_Report(test_data_pull, cData)
