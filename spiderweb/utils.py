import requests
from bs4 import BeautifulSoup


def get_links(target_url):
    try:
        r = requests.get('{}'.format(target_url))
    except requests.exceptions.MissingSchema as ex:
        return []

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = list()
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url in ['#']:
            pass
        else:
            links.append(link_url)

    return links
