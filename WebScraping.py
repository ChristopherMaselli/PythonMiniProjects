import requests
from bs4 import BeautifulSoup  # Makes webscraping of the page very easy
import pandas as pd

page = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=40.76769000000007&lon=-73.97058999999996')

soup = BeautifulSoup(page.content, 'html.parser')
week = soup.find(id='seven-day-forecast-body')
items = week.find_all(class_='tombstone-container')

# print(soup)
# print(soup.find_all('a'))

# print(items[0])

# print(items[0].find(class_='period-name').get_text())
# print(items[0].find(class_='short-desc').get_text())
# print(items[0].find(class_='temp').get_text())

period_names = [item.find(class_='period-name').get_text() for item in items]
print(period_names)

short_descriptions = [
    item.find(class_='short-desc').get_text() for item in items]
print(short_descriptions)

temperatures = [
    item.find(class_='temp').get_text() for item in items]
print(temperatures)

weather_stuff = pd.DataFrame(
    {'period': period_names,
     'short_descriptions': short_descriptions,
     'temperatures': temperatures,
     })

print(weather_stuff)

weather_stuff.to_csv('weather.csv')
