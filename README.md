# Final Project Proposal

## Group Members
* Patrick Ayers
* Zackary Larson

## Analysis Objective
Compare contrast between climate patterns on Earth & Mars. Earth orbits the Sun at distance of 94 million miles away in what's considered the "goldilocks zone" of the Solar System; in other words, not too hot and not too cold and therefore can support biological life. Mars on the other hand, is 155 million miles away, and among other geological factors (such as an incredibly thin atmostphere and absense of a magnetic field), is quite barren compared to Earth. 

This project will use the Curiosity dataset provided by NASA which features API connectivity along with an API connection to the NOAA Earth Weather data set to compare and contrast the temperature data between the two planets.

### Feature Summary:
* Selct a major city from a list along with a season and compare weather data to the weather on Mars during the same season
* Using NASA and NOAA APIs to bring in data, and show some creat graphs

## Dataypes that will be utilized
* Dataset 1 -> Mars Curiosity API: Weather data collected by the Curiosity rover. Includes temperature, atmospheric, and pressure data
  * https://mars.nasa.gov/msl/weather/
  * https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json

* Dataset 2 -> NOAA Weather API: Weather data collected for various cities across the planet. Incluedes temperature data
  * https://www.weather.gov/documentation/services-web-api

## Packages
* dotenv module - for storing API keys, and other personal information in a hidden\\
.env file.

* Request module - For pulling data from NASA website.

* Datetime module for managing dates and times 

## Dependencies
* logging
* os
* csv
* requests
* argparse
* datetime
* json
* itertools
* statistics
* collection
* matplotlib.pyplot
* dotenv
* numpy
* unittest

## Station Locations to be used:
* Los Angeles, CA US
* * Station_ID => GHCND:USW00003167
* Austin, TX
* * Station_ID => GHCND:USW00013958
* Orlando, FL US
* *  Station_ID => GHCND:USW00012815

## How to use
The arguements passed into the command line include specifying a City, Season, Year, and then whether to export raw data or to generate a plot of the data.

Sample line for Florida, Summer 2020, exporting the data (-w) and generating a plot (-e)
python3 Channel_Squareroot2_Weather.py 2020 -c FL -s Summer -w -e

## Conclusion
A difference of 60 million miles results in significant temperature drops on the surface of Mars. At the surface, Mars can be almost 100C below Earth. In summary, due to the extremely cold (and dry) climate, Mars is going to remain off peoples vacation destination list for a very long time.

