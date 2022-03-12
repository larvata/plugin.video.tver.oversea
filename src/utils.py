import requests


fetch = requests.Session()

def fetch_json(**kwargs):
    return fetch_page(**kwargs).json()


def fetch_page(url, method='GET', **kwargs):
    return fetch.request(method, url, **kwargs)

