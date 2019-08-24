#!/usr/bin/env python3

from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import abort

import sys
import random

from flickr import load_album, get_next, get_url, get_exif
from config import FLICKR_ALBUMS, PAGES, APPLETS

app = Flask(__name__)
app.secret_key = '8b98f9bacab5fbbf2576a90b55863c6e8868691dc44fcf99237c989edd6dde67'

def redirect_random(album='all'):
    load_album(album)
    img_id = random.choice(session['photos'])
    #print(img_id)
    return redirect('{}/{}'.format(album, img_id))

@app.route('/<album>/<int:image_id>')
def show_index(album, image_id):
    print('REQUEST ALBUM: {} // REQEST IMAGE: {}'.format(album, image_id), file=sys.stderr)
    if album is None:
        album = 'all'
    load_album(album)

    # print(session['photos'], file=sys.stderr)

    if image_id not in session['photos']:
        image_id = random.choice(session['photos'])

    image = {
        'id': image_id,
        'next': get_next(album, image_id),
        'url': get_url(image_id),
        'album': album,
        'exif': get_exif(image_id)
    }
    return render_template('page.html', image=image) 

@app.route('/<album>/')
def album(album):
    print('REQUEST ALBUM: '+album, file=sys.stderr)
    if album in PAGES:
        return render_template('{}.html'.format(album))
    album = album if album in FLICKR_ALBUMS else 'all'
    return redirect_random(album)
@app.route('/<page>')
def page(page):
    if page in PAGES:
        return render_template('{}.html'.format(page))
    abort(404)

@app.route('/applet/<name>')
def applet(name):
    if name in APPLETS:
        return render_template('applet.html', applet=APPLETS[name])
    abort(404)
    

@app.errorhandler(404)
@app.route('/')
def default(error=None):
#    return render_template('blank.html')
    return redirect_random()


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)

