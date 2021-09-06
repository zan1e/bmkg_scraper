from bs4 import BeautifulSoup
import requests


URL = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
request = requests.get(URL)

if request.status_code != 200:
    print(request.status_code)
    exit()

soup = BeautifulSoup(request.text,"lxml")

locations = soup.select('div.row.list-cuaca-provinsi.md-margin-bottom-10')
