from bs4 import BeautifulSoup
import requests


URL = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
request = requests.get(URL)

if request.status_code != 200:
    print(request.status_code)
    exit()

soup = BeautifulSoup(request.text,"lxml")

locations = soup.select('div.row.list-cuaca-provinsi.md-margin-bottom-10 > div')

for location in locations:
    request_location_page = requests.get(f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg{location.select_one('a')['href']}")
    print(location.select_one('a').text,end=" : ")
    print(request_location_page.status_code)

