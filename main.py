from bs4 import BeautifulSoup
import requests


URL = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
request = requests.get(URL)

if request.status_code != 200:
    print(request.status_code)
    exit()

main_soup = BeautifulSoup(request.text,"lxml")

locations = main_soup.select('div.row.list-cuaca-provinsi.md-margin-bottom-10 > div')

for location in locations:
    request_location_page = requests.get(f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg{location.select_one('a')['href']}")
    location_title = location.select_one('a').text
    location_soup = BeautifulSoup(request_location_page.text,"lxml")
    cities = location_soup.select_one('#TabPaneCuaca1 > div > table')

    for city_name in cities.select('tr > td:nth-child(1) > a'):
        print(city_name) 
    break
