from logging import error
import os
import argparse
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
    def __init__(self, year , location , season , explore ):
        self.year = str(year)
        self.location = str(location)
        self.season = str(season)
        self.explore = explore
        self.__build_API_Call()
        self.__extracting_data()

        if self.explore == True:
            self.explor_graph()
        
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
    def output_min_array(self):
        return self.min_array
    def output_max_array(self):
        return self.max_array
    def api_return_value(self):
        return self.r.status_code
    def output_date_array(self):
        return self.date_array
# Mars-related classes
class Curiosity_Data():

    def __init__(self, year, season, explore):
        self.explore = explore
        self.year = year
        self.season = season
        self.curiosity_data = []

        self.__retrieve_data()
        self.__process_data()
        
        if self.explore == True:
            self.__explore_data()

    def __retrieve_data(self):  # Data retrieval from API

        #logging.info('Calling Curiosity')
        self.curiosity_response = requests.get(f'{API_URL_CURIOSITY}') # API link contained in the .env file
        self.curiosity_response.raise_for_status()
        curiosity_JSON = json.loads(self.curiosity_response.text) # Loads as a dictionary with 2 key; description and soles
        self.sol_data = curiosity_JSON['soles'] # The other dictionary entry is 'description' which isn't useful for the sake of out data intake and analysis

    def __process_data(self):
        
        season_dict = {'Winter': {'first': '12-01', 'last': '02-28'}, 'Spring': {'first': '03-01', 'last': '05-31'}, 'Summer': {'first': '06-01', 'last': '08-31'}, 'Fall': {'first': '07-01', 'last': '11-30'}} # Season dictionary with start and end dats
        first_day_dt = datetime.date.fromisoformat(str(str(self.year) + '-' + season_dict[self.season]['first'])) # For data filtering
        last_day_dt = datetime.date.fromisoformat(str(str(self.year + 1) + '-' + season_dict[self.season]['last']) if self.season == 'Winter' else str(str(self.year) + '-' + season_dict[self.season]['last']))

        mars_record = collection.namedtuple('mars_record', 'earth_date, sol, season, min_temp, max_temp, ave_temp, atmo_opacity, pressure, sunrise, sunset, daylight')
        ave_min = statistics.mean([int(sol['min_temp']) for sol in self.sol_data if sol['min_temp'] != '--']) # To fill in missing data we're taking the average of the selected season
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
            
            daylight = (datetime.datetime.combine(datetime.date.today(), sunset_datetime) - datetime.datetime.combine(datetime.date.today(), sunrise_datetime)).total_seconds() / 3600 # Calculating daylight in hours

            if first_day_dt <= earth_date_datetime <= last_day_dt: # Filter by date/season
                self.curiosity_data.append(mars_record(earth_date_datetime, int(sol['sol']), sol['season'], int(sol['min_temp']), int(sol['max_temp']), int((int(sol['min_temp'])+int(sol['max_temp']))/2), sol['atmo_opacity'], int(sol['pressure']), sunrise_datetime, sunset_datetime, daylight))
    
    def __explore_data(self):
        self.min_temps = [data.min_temp for data in self.curiosity_data]
        self.max_temps = [data.max_temp for data in self.curiosity_data]
        self.ave_temps = [data.ave_temp for data in self.curiosity_data]
        self.sol = [data.sol for data in self.curiosity_data]
        seasons = list(set([data.season for data in self.curiosity_data]))
        self.daylight_per_season = [statistics.mean([data.daylight for data in self.curiosity_data if data.season == seasons[i]]) for i in range(0, len(seasons))]


        fig, axs = plt.subplots(1, 2)
        ax1, ax2 = axs
        ax1.plot(self.sol, self.max_temps, label='max')
        ax1.plot(self.sol, self.ave_temps, label='ave')
        ax1.plot(self.sol, self.min_temps, label='min')
        ax1.set_title('Temperatures for the Seasons (C)')
        ax1.set_xlabel('Sol (martian day)')
        ax1.set_ylabel('Temperature (C)')


        ax2.bar(seasons, self.daylight_per_season)
        ax2.set_ylim([11,13]) # 11 to 13 hours becuase Mars current tilt (and Curiosity's location) makes for fairly consistent daylight hours across the year (https://www.jpl.nasa.gov/images/changes-in-tilt-of-mars-axis)
        ax2.bar_label(ax2.bar(seasons, self.daylight_per_season, label='Average Daylight'))
        ax2.set_xlabel('Season')
        ax2.set_ylabel('Average Daylight (hours)')
        ax2.set_title('Average Daylight per Season (hours)')

        ax1.legend(loc='best')
        ax2.legend(loc='best')
        #plt.xticks(rotation=45)
        plt.show()

# Merged Data Sets
class Root_Two_Report(): # All humans are vermin in the eyes of Morbo...
    def __init__(self, earth_data, mars_data, export, plot):
        
        earth_datetime = [datetime.date.fromisoformat(str(date)) for date in earth_data.date_array]
        
        self.export = export
        self.plot = plot
        self.earth_data = zip(earth_datetime, earth_data.min_array, earth_data.max_array)
        self.mars_data = mars_data
        self.earth_mars_data = collection.defaultdict(dict)
        self.__merge_data()

        if self.export == True:
            self.__export_data()
        
        if self.plot == True:
            self.__plot_data()

    def __merge_data(self):

        for data in self.earth_data:
            self.earth_mars_data[data[0]]['earth_min'] = data[1]
            self.earth_mars_data[data[0]]['earth_max'] = data[2]
            self.earth_mars_data[data[0]]['earth_avg'] = (data[1] + data[2])/2

        for data in self.mars_data.curiosity_data:
            self.earth_mars_data[data.earth_date]['mars_min'] = data.min_temp
            self.earth_mars_data[data.earth_date]['mars_max'] = data.max_temp
            self.earth_mars_data[data.earth_date]['mars_avg'] = data.ave_temp

        self.earth_dates = [key for key in self.earth_mars_data.keys()]
        mars_avg_max = statistics.mean([int(data.max_temp) for data in self.mars_data.curiosity_data]) # Calculating an average to fill empty data in the earth_mars_data dictionary

        self.earth_data = [self.earth_mars_data[date]['earth_min'] for date in self.earth_dates]
        self.mars_data = []
        for date in self.earth_dates:
            try:
                self.mars_data.append(self.earth_mars_data[date]['mars_max'])
            except KeyError:
                self.mars_data.append(mars_avg_max)

    def __export_data(self):
        field_names = ['date', 'earth_min', 'earth_max', 'earth_avg', 'mars_min', 'mars_max', 'mars_avg']

        with open('Root2Report.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, field_names)
            writer.writeheader()
            for key, value in sorted(self.earth_mars_data.items()):
                row = {'date': key}
                row.update(value)
                writer.writerow(row)

    def __plot_data(self):
        # Need some ideas on this

        fig, ax1 = plt.subplots()
        ax1.fill_between(self.earth_dates, self.earth_data, self.mars_data)
        ax1.set_label('Temperature Difference Between Earth Minimums and Mars Maximums')
        ax1.set_xlabel('Earth Date')
        ax1.set_ylabel('Temperature (C)')
        #fig.tight_layout()
        plt.show()


def main():    
    #adding command line arguments
    parser = argparse.ArgumentParser(prog='Weather informaiton gather', 
                                    description='''Comparing weather data from a city on Earth to weather data from Mars.You will need
                                    to secelct a Season, year and a city to compare data from. A full list is cities and years are given
                                    for each respective argument.''')

    parser.add_argument("year",type = str, metavar = "<year>", help = "Please chose one of the following 2017,2018,2019,2020,2021",
                        choices = ["2017","2018","2019","2020","2021"])

    parser.add_argument('-c',dest = 'e_location',metavar = '<Earth City>',
                        type = str, default = "LA",
                        help ='''Please choise one of the following cities LA ,DN, NY, TX, FL.If a city is not selected default will be LA''',
                        choices = ["LA","DN","NY","TX","FL"])

    parser.add_argument('-s',dest = 'season',metavar = '<Earth Season>',
                        type = str, default = "Spring",
                        help = "Please chose one of the following seasons Spring, Summer, Fall Winter. If a sesason is not selected defualt is Spring",
                        choices = ["Spring","Summer","Fall","Winter"])
    
    parser.add_argument('-e',dest= 'explore_graph',action='store_true',
                        help = "If you would like to see the exploratory graphs")

    parser.add_argument('-w',dest= 'write_csv', action='store_true',
                        help = 'If you would like to exprot a CSV')
    
    run( parser.parse_args())

def run(args):
    city_value = ""
    if args.e_location == "LA":
        #GHCND:USW00003167
        city_value = 'USW00003167'
    elif args.e_location == "DN":
        #GHCND:USC00052223
        city_value = "USC00052223"
    elif args.e_location == "NY":
        #GHCND:USW00094789
        city_value = "USW00094789"
    elif args.e_location == "TX":
        #GHCND:USW00013958
        city_value = "USW00013958"
    elif args.e_location == "FL":
        #GHCND:USW00012815
        city_value = "USW00012815"
    else:
        raise ValueError('City value not valied, please look into this.')

    #Pulling in data section
    earth_data = NOAA_Data(args.year,city_value,args.season,args.explore_graph)
    mars_data = Curiosity_Data(args.year,args.season,args.explore_graph)
    Root_Two_Report(earth_data,mars_data,args.explore_graph,args.write_csv)


if __name__=="__main__":
    main()
