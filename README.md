# Final Project Proposal

## Group Members
* Patrick Ayers
* Zackary Larson

## Analysis Objective
Compare contrast between climate patterns on Earth & Mars. Earth orbits the Sun at distance of 94 million miles away in what's considered the "goldilocks zone" of the Solar System; in other words, not too hot and not too cold and therefore can support biological life. Mars on the other hand, is 155 million miles away, and among other geological factors (such as an incredibly thin atmostphere and absense of a magnetic field), is quite barren compared to Earth. 

This project will use the Insight dataset provided by NASA which features API connectivity along with a flat file of Earth weather data, where both sets will be compared and contrasted with the assistance of visual diagrams and aggregate figures.

### Feature Summary:
* Selct a major city from a list along with a season and compare weather data to the weather on Mars during the same season
* Using NASA API to bring in data, and show some creat graphs
* Earth data brought in from flat file

## Dataypes that will be utilized
* Dataset 1 -> Mars Insight Weather API
  * https://mars.nasa.gov/insight/weather/

* Dataset 2 -> Earth Weather flat file (PENDING: Deciding on exact data set)
  * https://www.weather.gov/documentation/services-web-api

## Protenal packages we will explore
* dotenv module - for storing API keys, and other personal information in a hidden\\
.env file.

* Request module - For pulling data from NASA website.

* Datetime module for managing dates and times 

* Marstiming - an open source library for calculating Mars time:
  * https://marstiming.readthedocs.io/en/latest/_modules/marstiming.html
