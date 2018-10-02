from flask import Flask
from flask import session
from flask import render_template
from flask import redirect

import random

from flickr import load_album, get_next, get_url, get_exif
from config import ALBUMS

app = Flask(__name__)
app.secret_key = '8b98f9bacab5fbbf2576a90b55863c6e8868691dc44fcf99237c989edd6dde67'


@app.route('/<album>/<int:image_id>')
def show_index(album, image_id):
    #print('REQUEST ALBUM: {} // REQEST IMAGE: {}'.format(album, image_id))
    if album is None:
        album = 'all'
    load_album(album)

    # print(session['photos'], file=sys.stderr)

    if image_id not in session['photos']:
        image_id = random.choice(session['photos'])

    image = {}
    image['id'] = image_id
    image['next'] = get_next(album, image_id)
    image['url'] = get_url(image_id)
    image['album'] = album
    image['exif'] = get_exif(image_id)
    return render_template('page.html', image=image) 

def redirect_random(album='all'):
    load_album(album)
    img_id = random.choice(session['photos'])
    #print(img_id)
    return redirect('{}/{}'.format(album, img_id))


@app.route('/<album>/')
def album(album):
    #print('REQUEST ALBUM: '+album)
    if album == 'dof':
        return render_template('dof.html')
    album = album if album in ALBUMS else 'all'
    return redirect_random(album)


@app.errorhandler(404)
@app.route('/')
def default(error=None):
    return redirect_random()



if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)

