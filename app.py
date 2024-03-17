#!/usr/bin/env python3
import sys
import random
import io

from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import abort
from flask import request
from flask import Response
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from flickr import load_album, get_url, get_exif, get_album_photos, FLICKR_URL_TEMPLATE
from config import MENU_ITEMS, FLICKR_ALBUMS, PAGES, APPLETS
import photo_stats

app = Flask(__name__)
app.secret_key = '8b98f9bacab5fbbf2576a90b55863c6e8868691dc44fcf99237c989edd6dde67'

matplotlib.use('Agg')

@app.route('/random')
def redirect_random(album='all'):
    picture_list = load_album(album)
    image_id = random.choice(picture_list)
    print('RANDOMLY PICKED IMAGE: {}'.format(image_id))
    return redirect('photo/{}'.format(image_id))


@app.route('/photo/<int:image_id>')
def show_index(image_id):
    print('REQUEST IMAGE: {}'.format(image_id))
    album = 'all'
    if 'album' in session:
        album = session['album']
    picture_list = load_album(album)
    print('LOADED ALBUM: {} = {}'.format(album, picture_list))

    if image_id not in picture_list:
        print('ERR: image {} not in session album {}.'.format(image_id, session['album']))
        image_id = random.choice(picture_list)
        return redirect('photo/{}'.format(image_id))

    next_image_id = picture_list[(picture_list.index(image_id)+1) % len(picture_list)]

    image = {
        'id': image_id,
        'next': next_image_id,
        'url': get_url(image_id),
        'exif': get_exif(image_id)
    }
    title = 'photographie' if album == 'all' else FLICKR_ALBUMS[album]['title']
    return render_template('single.tpl.html', image=image, menus=MENU_ITEMS, title=title)

@app.route('/album/<album>')
def album(album):
    print('REQUEST ALBUM: '+album)

    if album in FLICKR_ALBUMS:
        session['album'] = album
        photos = []
        album_photos = get_album_photos(FLICKR_ALBUMS[album]['id'])

        background_photo = random.choice(album_photos)
        background_photo['size'] = 'b'
        background = {
            'url': FLICKR_URL_TEMPLATE.format(**background_photo),
            'next': None
        }

        for i in album_photos:
            i['size'] = 'q'
            photos.append({
                'id': i['id'],
                'thumb': FLICKR_URL_TEMPLATE.format(**i)
            })

        return render_template('gallery.tpl.html', image=background, photos=photos, menus=MENU_ITEMS, title=FLICKR_ALBUMS[album]['title'])
    abort(404)

@app.route('/<page>')
def page(page):
    if page in PAGES:
        return render_template('{}.html'.format(page))
    abort(404)

@app.route('/applet/<name>')
def applet(name):
    if name in APPLETS:
        return render_template('applet.tpl.html', applet=APPLETS[name])
    abort(404)

@app.route('/cpce/plot', methods=['POST'])
def cpce_api_plot():
    # summary format:
    # { "marks": [[]], "picture_id": [], "voter_id": [], "rank": [],"range":{"min":0,"max":30} }
    summary = request.json
    fig = photo_stats.do_plot(summary['marks'], summary['rank'], summary['range']['min'], summary['range']['max'])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.errorhandler(404)
@app.route('/')
def default(error=None):
    session['album'] = 'all'
    picture_list = load_album('all')
    return redirect('/photo/{}'.format(picture_list[0]))


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)

