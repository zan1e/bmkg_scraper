from bs4 import BeautifulSoup
import requests


URL = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
request = requests.get(URL)

if request.status_code != 200:
    print(request.status_code)
    exit()

main_soup = BeautifulSoup(request.text,"lxml")

locations = main_soup.select('div.row.list-cuaca-provinsi.md-margin-bottom-10 > div')

i = 0
for location in locations:
    request_location_page = requests.get(f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg{location.select_one('a')['href']}")
    location_title = location.select_one('a').text
    location_soup = BeautifulSoup(request_location_page.text,"lxml")
    location_table = location_soup.select_one('#TabPaneCuaca1 > div > table ')
    cities = [location_table.select('tr > td > a')]
    temp = [location_table.select('tr > td:nth-child(4)')]
    humidity = [location_table.select('tr > td:nth-child(5)')]
    date = location_soup.select_one('div.prakicu-kabkota.tab-v1 > ul > li:nth-child(1) > a').text

    print(f'{location_title} - {date}',end="\n\n")

    for i in range(len(cities[0])):
        print(cities[0][i].text)
        print(temp[0][i].text)
        print(humidity[0][i].text)
