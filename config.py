import itertools

FLICKR_ID = "7558628@N02"
FLICKR_API_KEY = "117a79cd3ae4d8b0533ac65fa38aec83"

MENU_ITEMS = { 
    'albums': [
        { 'id': 72157684245616056, 'title': 'Macro',            'slug': 'macro'     },
        { 'id': 72157690781846976, 'title': 'Made with iPhone', 'slug': 'mobile'    },
        { 'id': 72157684095730415, 'title': 'Gouttes',          'slug': 'gouttes'   },
        { 'id': 72157634866476750, 'title': 'Origami',          'slug': 'origami'   },
        { 'id': 72157710589315476, 'title': 'Paysages urbains', 'slug': 'urban'     },
        { 'id': 72157673653825028, 'title': 'Best of',          'slug': 'bestof'    }
    ],
    'voyages': [
        { 'id': 72177720302530550, 'title': 'Groenland',        'slug': 'groenland'     },
        { 'id': 72177720296978358, 'title': 'Lofoten',          'slug': 'lofoten'       },
        { 'id': 72157710618231867, 'title': 'Saint Petersbourg','slug': 'stpetersbourg' },
        { 'id': 72157671913840076, 'title': 'Mongolie',         'slug': 'mongolie'      }, 
        { 'id': 72157667973587035, 'title': 'Japon',            'slug': 'japon'         },
        { 'id': 72157627209760762, 'title': 'Copenhague',       'slug': 'copenhague'    },
        { 'id': 72157627100532140, 'title': 'Pologne',          'slug': 'pologne'       },
        { 'id': 72157624521847393, 'title': 'Amsterdam',        'slug': 'amsterdam'     }, 
        { 'id': 72157621644149273, 'title': 'Stockholm',        'slug': 'stockholm'     }
    ]
}
# flat dictionary of slug/id pairs
FLICKR_ALBUMS = dict([(x['slug'], x) for x in itertools.chain(*MENU_ITEMS.values())])

PAGES = ['dof']
APPLETS = {
    'locus': {
        'title': 'Locus',
        'file': 'locus.swf',
        'width': 1050,
        'height': 710
    }, 
    'gamut': {
        'title': 'Gamut mapping',
        'file': 'gamutmapping.swf',
        'width': 960,
        'height': 510
    },
    'chromaticity': {
        'title': 'Chromaticity diagram',
        'file': 'chromaticity.swf',
        'width': 1000,
        'height': 720
    }
}