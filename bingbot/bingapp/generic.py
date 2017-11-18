import json
import datetime
from urllib import request


def get_urls(date=None):
    response = request.urlopen('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=100&mkt=en-US')
    response_body = response.read()
    if date:
        return (el for el in json.loads(response_body).get('images')
                if el['startdate'] == date).__next__()
    return json.loads(response_body).get('images')


def save_file(picture):
    filename = picture['url'].split('/')[-1]
    f = open(filename, 'wb')
    f.write()
    f.close()
    return filename


def get_full_url(picute):
    return 'http://www.bing.com' + picute['url']


def get_file(url):
    response = request.urlopen(url)
    return response.read()


def get_dates():
    urls = get_urls()
    return [u.get('startdate') for u in urls]
