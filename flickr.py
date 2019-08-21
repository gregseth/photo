from flask import session

from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen

import sys
import json
import random

from config import *

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
    result = get_json({
        **QUERY,
        'method': 'flickr.people.getPublicPhotos',
        'extras': 'url_o',
        'per_page': 500 # TODO get more
    })

    return [p['id'] for p in result['photos']['photo']]

def get_album_photos(album_id):
    result = get_json({
        **QUERY,
        'method': 'flickr.photosets.getPhotos',
        'photoset_id': album_id,
        'per_page': 500 # TODO get more
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
    
    return [p['source'] for p in result['sizes']['size'] if p['label'] == 'Original'][0]


def load_album(album):  
    if not 'album' in session or session['album'] != album:
        session['album'] = album

        print('ALBUM ID: {}'.format(album), file=sys.stderr)
        if album == 'all' or not album in FLICKR_ALBUMS:
            with open('static/flickr.lst') as lst:
                session['photos'] = [int(l.rstrip('\n')) for l in lst]
        else:
            session['photos'] = get_album_photos(FLICKR_ALBUMS[album])


def get_next(album, image_id):
    piclist = session['photos']
    if album == 'all':
        return random.choice(piclist)
    return piclist[(piclist.index(image_id)+1) % len(piclist)]
