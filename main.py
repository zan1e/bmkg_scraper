from bs4 import BeautifulSoup
import requests
import concurrent.futures
import time

URL = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
request = requests.get(URL)

if request.status_code != 200:
    print(request.status_code)
    exit()


main_soup = BeautifulSoup(request.text,"lxml")

locations = main_soup.select('div.row.list-cuaca-provinsi.md-margin-bottom-10 > div')

def scrape_location_data(location):
    request_location_page = requests.get(f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg{location.select_one('a')['href']}")
    location_title = location.select_one('a').text
    location_soup = BeautifulSoup(request_location_page.text,"lxml")
    location_table = location_soup.select_one('#TabPaneCuaca1 > div > table ')
    cities = [location_table.select('tr > td > a')]
    temperatures = [location_table.select('tr > td:nth-child(4)')]
    humidities = [location_table.select('tr > td:nth-child(5)')]
    date = location_soup.select_one('div.prakicu-kabkota.tab-v1 > ul > li:nth-child(1) > a').text

    return {
            'location' : location_title,
            'date' : date,
            'cities' : [{
                    'city_name' : cities[0][_].text,
                    'temperature' : temperatures[0][_].text,
                    'humidity': humidities[0][_].text
                } for _ in range(len(cities[0]))]
            }


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(scrape_location_data,location) for location in locations]
    for future in concurrent.futures.as_completed(results):
        print(future.result())
