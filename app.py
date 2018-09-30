from flask import Flask
from flask import render_template
from flask import session

from urllib.parse import quote_plus
from urllib.request import urlopen

import sys
import json
import random

app = Flask(__name__)
app.secret_key = '8b98f9bacab5fbbf2576a90b55863c6e8868691dc44fcf99237c989edd6dde67'

YQ_URL = "https://query.yahooapis.com/v1/public/yql?format=json&env={}&q=". \
    format(quote_plus("store://datatables.org/alltableswithkeys"))
    

FLICKR_ID = "7558628@N02"
FLICKR_API_KEY = "117a79cd3ae4d8b0533ac65fa38aec83"
ALBUMS = ['macro', 'mobile', 'all']

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
        "user_id='{}' AND extras='url_o'".format(user_id))

    image_ids = []
    for item in result.query.results.photo:
        image_ids.append(item.id)

    return image_ids

def get_album_photos(album_id):
    result = get_json_result(
        "id", 
        "flickr.people.publicphotos(0, 5000)", 
        "photoset_id='{}' ORDER BY id DESC".format(album_id))

    image_ids = []
    for item in result.query.results.photo:
        image_ids.append(item.id)

    return image_ids

def get_exif(photo_id):
    fields = [
        'Make', 'Model', 'LensModel',
        'Lens', 'FocalLength', 'ExposureTime',
        'FNumber', 'ISO'
    ]
    # initializing all tags values to '?'
    exif = dict(zip(fields, ['?']*len(fields)))

    result = get_json_result(
        "exif.tag, exif.raw", 
        "flickr.photos.exif", 
        "photo_id='{}' AND exif.tag IN ('{}')".
        format(photo_id, "', '".join(fields))
    )
    print(result, file=sys.stderr)

    # filling with retrieved data
    for item in result['query']['results']['photo']:
        exif[item['exif']['tag']] = item['exif']['raw']

    # treating special cases
    if exif['LensModel'] == '?' and exif['Lens'] != '?':
        exif['LensModel'] = exif['Lens']

    return exif


def get_url(photo_id):
    result = get_json_result(
        "source", 
        "flickr.photos.sizes", 
        "photo_id='{}' AND label='Original'".format(photo_id))
    print(result, file=sys.stderr)
    return result['query']['results']['size']['source']

def load_album(album):  
    with open('static/flickr.lst') as lst:
        session['photos'] = [l.rstrip('\n') for l in lst]

def get_next(album, image_id):
    if album == 'all':
        return random.choice(session['photos'])
    return session['photos'][session['photos'].index(image_id)+1%len(session['photos'])]

@app.route('/<album>/<int:image_id>')
def show_index(album, image_id):
    if album is None:
        album = 'all'
    load_album(album)

    if image_id not in session['photos']:
        image_id = random.choice(session['photos'])

    image = {}
    image['id'] = image_id
    image['next'] = get_next(album, image_id)
    image['url'] = get_url(image_id)
    image['album'] = album
    image['exif'] = get_exif(image_id)
    return render_template('page.html', image=image) 

@app.route('/')
def default():
    return 'It works!'


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)

