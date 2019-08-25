from flask import session

from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen

import sys
import json
import random

from config import FLICKR_ALBUMS, FLICKR_API_KEY, FLICKR_ID

FLICKR_API_ENDPOINT = 'https://www.flickr.com/services/rest/?'
QUERY = {
    'api_key': FLICKR_API_KEY,
    'user_id': FLICKR_ID,
    'format': 'json',
    'nojsoncallback': 1
#    'method': # mandatory
}

def get_json(query):
    """ :type query: dict representing the query string """
    flickr_query = urlencode(query)
    with urlopen(FLICKR_API_ENDPOINT + flickr_query) as rawdata:
        data = json.loads(rawdata.read().decode())
        if data['stat'] == 'ok':
            return data
        else:
            print(data['message'])

def get_user_photos():
    page = 1
    ids = []
    while "page count not reached":

        result = get_json({
            **QUERY,
            'method': 'flickr.people.getPublicPhotos',
            'page': page,
            'per_page': 500
        })
        ids += [p['id'] for p in result['photos']['photo']]
        page += 1
        if page > result['photos']['pages']:
            break
    
    return ids

def get_album_photos(album_id):
    result = get_json({
        **QUERY,
        'method': 'flickr.photosets.getPhotos',
        'photoset_id': album_id,
        'per_page': 500
    })

    return [p['id'] for p in result['photoset']['photo']]

def get_exif(photo_id):
    fields = [
        'Make', 
        'Model', 
        'LensModel',
        'Lens', 
        'FocalLength', 
        'ExposureTime',
        'FNumber', 
        'ISO'
    ]
    # initializing all tags values to '?'
    exif = dict(zip(fields, ['?']*len(fields)))

    result = get_json({
        **QUERY,
        'method': 'flickr.photos.getExif',
        'photo_id': photo_id
    })

    # filling with retrieved data
    try:
        for item in result['photo']['exif']:
            exif[item['tag']] = item['raw']['_content']
        
        # treating special cases
        if exif['LensModel'] == '?' and exif['Lens'] != '?':
            exif['LensModel'] = exif['Lens']
    except TypeError:
        exif = None #pass # exif filled with '?'

    return exif


def get_url(photo_id):
    result = get_json({
        **QUERY,
        'method': 'flickr.photos.getSizes',
        'photo_id': photo_id
    })

    #print(result)
    
    return [p['source'] for p in result['sizes']['size'] if p['label'] == 'Original'][0]


def load_album(album):
    picture_list = []

    print('LOADING ALBUM: {}'.format(album), file=sys.stderr)
    if album == 'all' or not album in FLICKR_ALBUMS:
        with open('static/flickr.lst') as lst:
            picture_list = [int(l.rstrip('\n')) for l in lst]
    else:
        picture_list = [int(id) for id in get_album_photos(FLICKR_ALBUMS[album])]

    return sorted(picture_list, key=int, reverse=True)
