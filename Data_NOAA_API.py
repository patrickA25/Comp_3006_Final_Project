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

#Getting API Key from .env file
load_dotenv()
API_KEY_NOAA = os.getenv("API_KEY_NOAA")

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
            self.API_call = f'''https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&limit=1000&units=metric&stationid=GHCND:{self.location}&startdate={self.year}-03-01&enddate={self.year}-05-31'''
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
    
def main():
    test_data_pull = NOAA_Data(2018,'USW00003167','Winter')
    test_data_pull.explor_graph()
    
if __name__ == '__main__':
    main()