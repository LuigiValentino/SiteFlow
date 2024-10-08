import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def generate_sitemap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    
    sitemap = []
    base_url = url
    
    for link in links:
        full_url = urljoin(base_url, link['href'])
        if base_url in full_url:
            sitemap.append(full_url)

    return {'nodes': sitemap}
