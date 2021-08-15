import collections, datetime, json, logging, matplotlib.pyplot as plt, numpy as np, os, requests, statistics
from dotenv import load_dotenv

# Debug setup
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

# API Key
load_dotenv()
#API_KEY_INSIGHT = os.getenv("API_KEY_INSIGHT")
API_URL_CURIOSITY = os.getenv("CURIOSITY_API")

class MarsData:
    def __init__(self):
        self.data = []
        self._process_data()

    # Data processing function
    def _process_data(self):
        mars_record = collections.namedtuple('mars_record', 'id, terrestrial_date, sol, season, min_temp, max_temp, ave_temp, atmo_opacity, pressure, sunrise, sunset, daylight')
        a = 0
        #logging.info('Calling Curiosity')
        curiosity_response = requests.get(f'{API_URL_CURIOSITY}')
        curiosity_response.raise_for_status()
        curiosity_JSON = json.loads(curiosity_response.text) # Loads as a dictionary with 2 key; description and soles
        sol_data = curiosity_JSON['soles']
        ave_min = statistics.mean([int(sol['min_temp']) for sol in sol_data if sol['min_temp'] != '--'])
        ave_max = statistics.mean([int(sol['max_temp']) for sol in sol_data if sol['max_temp'] != '--'])
        ave_pressure = statistics.mean([int(sol['pressure']) for sol in sol_data if sol['pressure'] != '--'])
        
        for sol in sol_data:
            if sol['min_temp'] == '--': # Fill in
                sol['min_temp'] = ave_min
            if sol['max_temp'] == '--':
                sol['max_temp'] = ave_max
            if sol['pressure'] == '--':
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
            self.data.append(mars_record(sol['id'], earth_date_datetime, int(sol['sol']), sol['season'], int(sol['min_temp']), int(sol['max_temp']), int((int(sol['min_temp'])+int(sol['max_temp']))/2), sol['atmo_opacity'], int(sol['pressure']), sunrise_datetime, sunset_datetime, daylight))

cData = MarsData()
#for data in cData.data:
#    print(data)

min_temps = [data.min_temp for data in cData.data]
max_temps = [data.max_temp for data in cData.data]
ave_temps = [data.ave_temp for data in cData.data]

daylight_per_season = [statistics.mean([data.daylight for data in cData.data if data.season == f'Month {i}']) for i in range(1, 13)]
print(daylight_per_season)

sol = [data.sol for data in cData.data]
season = [data.season for data in cData.data]

fig, axs = plt.subplots(1, 2)
ax1, ax2 = axs
ax1.plot(sol, max_temps, label='max')
ax1.plot(sol, ave_temps, label='ave')
ax1.plot(sol, min_temps, label='min')
ax1.set_xlabel('Sol')
ax1.set_ylabel('Temperature (C)')
ax1.legend(loc='best')

seasons = [f'Month {i}' for i in range(1, 13)]
ax2.bar(seasons, daylight_per_season, label='Average Daylight')
ax2.set_ylim([11,13])
ax2.set_xlabel('Season')
ax2.set_ylabel('Average Daylight (hours)')

#plt.plot(sol, min_temps)
ax2.legend(loc='best')
plt.xticks(rotation=45)
plt.show()


# InSight URL
#insightResponse = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={API_KEY_INSIGHT}&feedtype=json&ver=1.0')
#curiosityResponse = requests.get(f'{API_URL_CURIOSITY}')
#curiosityResponse.raise_for_status()
#curiosityData = json.loads(curiosityResponse.text)

#for i in range(0, len(curiosityData['soles'])):
#    print(curiosityData['soles'][i]['min_temp'])
#min_temps = [curiosityData['soles'][i]['min_temp'] for i in range(0, len(curiosityData['soles']))]
#max_temps = [curiosityData['soles'][i]['max_temp'] for i in range(0, len(curiosityData['soles']))]

#print(min_temps)
#print(max_temps)

"""     def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter == len(self.data):
            raise StopIteration
        else:
            mars_data = MarsData(self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5], self.data[6], self.data[7], self.data[8])
            self._iter += 1
            return mars_data """

        # For testing purposes
"""         with open('curiosity_data.txt', 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE)
            for entry in sol_data:
                data = [a, entry['terrestrial_date'], entry['sol'], entry['season'], entry['min_temp'], entry['max_temp'], entry['pressure'], entry['sunrise'], entry['sunset']]
                writer.writerow(data)
                a+=1 """
