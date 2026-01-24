import requests
from bs4 import BeautifulSoup
import json 
import os

FDC_API_KEY = os.getenv("FDC_API_KEY")

if not FDC_API_KEY:
    raise RuntimeError("API key not set!")

request = requests.get("https://folio.kanttiinit.fi/en/area/1")
html = request.text
soup = BeautifulSoup(html, "html.parser")

restaurants = soup.find_all("li", attrs={"class":"restaurant"}) # Tags
restaurant_dict = {}

for restaurant in restaurants:
    name = restaurant.find("h3").get_text(strip=True)
    menu_ul = restaurant.find("ul")

    if not menu_ul:
        restaurant_dict[name] = []
        continue
    items = []

    for li in menu_ul.find_all("li"):
        items.append(li.get_text(strip=True))
    restaurant_dict[name] = items

fdc_request = requests.get(
    f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={FDC_API_KEY}",
    params = {
        "query": "cheddar cheese",
        "pageNumber" : "1",
        "numberOfResultsPerPage" : "10",
        "pageSize" : "1",
    }
)
fdc_request.raise_for_status()
fdc_data = fdc_request.json()
print(fdc_data["foods"][0]["foodNutrients"][0])
#print(json.dumps(fdc_data, indent=4))

