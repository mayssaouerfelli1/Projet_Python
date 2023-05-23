from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import requests

def index(request):
    url = "https://www.jumia.com.tn/smartphones/"
    res = requests.get(url)
    src = res.content
    soup = bs(src, "html.parser")
    list = []

    nom = soup.find_all("h3", {"class": "name"})
    prix = soup.find_all("div", {"class": "prc"})
    image = soup.find_all("img", {"class": "img"})

    for compteur in range(len(nom)):
        list.append({
            'name': nom[compteur].text,
            'price': prix[compteur].text,
            'image': image[compteur].get('data-src')
        })

    marques = []
    for product in list:
        brand = product['name'].split(' ')[0]
        if brand not in marques:
            marques.append(brand)

    selected_brand = request.GET.get('brand')
    selected_max_price = request.GET.get('maxPrice')
    selected_min_price = request.GET.get('minPrice')

    filtered_products = []
    for product in list:
        brand = product['name'].split(' ')[0]
        price = float(product['price'].split(' ')[0].replace(',', ''))
        if (
            (not selected_brand or brand == selected_brand) and
            (not selected_max_price or price <= float(selected_max_price)) and
            (not selected_min_price or price >= float(selected_min_price))
        ):
            filtered_products.append(product)

    return render(request, 'home.html', {
        'products': filtered_products,
        'brands': marques,
        'selected_brand': selected_brand,
        'selected_max_price': selected_max_price,
        'selected_min_price': selected_min_price
    })
