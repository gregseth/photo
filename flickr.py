from flask import session

from urllib.parse import quote_plus
from urllib.request import urlopen

import sys
import json
import random

from config import *

YQ_URL = "https://query.yahooapis.com/v1/public/yql?format=json&env={}&q=". \
    format(quote_plus("store://datatables.org/alltableswithkeys"))

def get_json(query):
    flickr_query = quote_plus(query)
    with urlopen(YQ_URL + flickr_query) as data:
        return json.loads(data.read().decode())

def get_json_result(fields, table, condition, debug=False):
    query = "SELECT {} FROM {} WHERE api_key='{}' AND {}". \
        format(fields, table, FLICKR_API_KEY, condition)

    return get_json(query)

def get_user_photos(user_id):
    result = get_json_result(
        "*", 
        "flickr.people.publicphotos(0, 5000)", 
        "user_id='{}' AND extras='url_o'".format(user_id)
    )

    image_ids = []
    for item in result['query']['results']['photo']:
        image_ids.append(item['id'])

    return image_ids

def get_album_photos(album_id):
    result = get_json_result(
        "id", 
        "flickr.photosets.photos(0, 5000)", 
        "photoset_id='{}' ORDER BY id DESC".format(album_id)
    )

    image_ids = []
    for item in result['query']['results']['photo']:
        image_ids.append(int(item['id']))

    return image_ids

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

    result = get_json_result(
        "exif.tag, exif.raw", 
        "flickr.photos.exif", 
        "photo_id='{}' AND exif.tag IN ('{}')".
            format(photo_id, "', '".join(fields))
    )
    # print(result, file=sys.stderr)

    # filling with retrieved data
    try:
        for item in result['query']['results']['photo']:
            exif[item['exif']['tag']] = item['exif']['raw']
        
        # treating special cases
        if exif['LensModel'] == '?' and exif['Lens'] != '?':
            exif['LensModel'] = exif['Lens']
    except TypeError:
        exif = None #pass # exif filled with '?'

    return exif


def get_url(photo_id):
    result = get_json_result(
        "source", 
        "flickr.photos.sizes", 
        "photo_id='{}' AND label='Original'".format(photo_id)
    )
    # print(result, file=sys.stderr)
    return result['query']['results']['size']['source']


def load_album(album):  
    if not 'album' in session or session['album'] != album:
        session['album'] = album
        #print('ALBUM ID: {}'.format(album), file=sys.stderr)
        if album == 'all':
            with open('static/flickr.lst') as lst:
                session['photos'] = [int(l.rstrip('\n')) for l in lst]
        elif album == 'macro':
            session['photos'] = get_album_photos(72157684245616056)
        elif album == 'mobile':
            session['photos'] = get_album_photos(72157690781846976)


def get_next(album, image_id):
    piclist = session['photos']
    if album == 'all':
        return random.choice(piclist)
    return piclist[piclist.index(image_id)+1 % len(piclist)]
