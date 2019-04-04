import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def spider(starting_point_url, scope, depth=2):
    """

    Spider the website specified by starting URL, only following links inside provided scope.

    :param starting_point_url: in format protocol://address.tld/parameters
    :param scope: in format *.domain.name or domain.name
    :param depth: depth of spidering.
    :return: set() of found links until depth is reached
    """
    # Ignore out of scope URLs
    if not in_scope(starting_point_url, scope):
        return set()

    # If in scope, add source to result
    resulting_links = {starting_point_url}

    # If depth reached 0, return source URL
    if depth == 0:
        return resulting_links
    else:
        # Find all links on the source URL
        found_links = get_links(target_url=starting_point_url)

        # Spider all found links
        for link in found_links:
            # If found link is in scope, spider it with decremented depth
            if in_scope(link, scope):
                spidered_links = spider(link, scope, depth=depth-1)

                # Add spidered links to result set
                resulting_links = resulting_links.union(spidered_links)
            else:
                continue

        return resulting_links


def get_links(target_url):
    """

    Find all links on URL

    :param target_url: in format protocol://address.tld/parameters
    :return: set() of found links
    """

    # Try to open requested URL
    try:
        r = requests.get('{}'.format(target_url))
    except requests.exceptions.MissingSchema as ex:
        return set()

    # Parse the result
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    links = set()

    # Find all 'a' elements and store 'href' argument
    for link in soup.find_all('a'):
        link_url = link.get('href')
        links.add(link_url)

    return links


def in_scope(target_url, scope):
    """

    Test if URL is part of desired scope

    :param target_url: in format protocol://address.tld/parameters
    :param scope: in format *.domain.name or domain.name
    :return: True if in scope, False otherwise
    """
    # Check input parameters
    if target_url is None or scope is None:
        return False
    if scope == '*':
        return True

    # Count level of subdomains in scope
    subdomains = scope.split('.')
    subdomains_num = len(subdomains) if subdomains[0] != '*' else len(subdomains) - 1

    target_hostname = urlparse(target_url).hostname
    if target_hostname is None:
        return False
    return target_hostname.split('.')[-subdomains_num:] == scope.split('.')[-subdomains_num:]
