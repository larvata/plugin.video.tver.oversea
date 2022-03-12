# builtin
import sys

# kodi
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

import requests
from urllib.parse import urlencode, parse_qsl

from utils import fetch_json


VIEW_LIST = 50
VIEW_POSTER = 51
VIEW_ICON_WALL = 52
VIEW_SHIFT = 53
VIEW_INFO_WALL = 54
VIEW_WIDE_LIST = 55

API_BASE = 'http://tver.larvata.me:5433'
API_GENRES = f'{API_BASE}/genre'
API_LIST = f'{API_BASE}/list?genre={{}}'
API_PLAYLIST = f'{API_BASE}/playlist?ref={{}}&pub={{}}'


# plugin url
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

def get_url(**kwargs):
    """
    TODO
    """
    return f'{_URL}?{urlencode(kwargs)}'


def render_genres(parent_title=''):
    resp_json = fetch_json(url=API_GENRES)
    xbmcplugin.setPluginCategory(_handle, parent_title)
    xbmcplugin.setContent(_handle, 'videos')

    for genre in resp_json:
        title = genre.get('title')
        key = genre.get('key')
        url = get_url(genre_id=key, parent_title=title)
        list_item = xbmcgui.ListItem(label=title)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle)
    xbmc.executebuiltin(f'Container.SetViewMode({VIEW_WIDE_LIST})')


def render_catgories(genre_id, parent_title=''):
    resp_json = fetch_json(url=API_LIST.format(genre_id))
    xbmcplugin.setPluginCategory(_handle, parent_title)
    xbmcplugin.setContent(_handle, 'videos')

    for item in resp_json.get('data'):
        pub = item.get('publisher_id')
        ref = item.get('reference_id')
        title = item.get('title')
        subtitle = item.get('subtitle')
        media = item.get('media')
        expire = item.get('expire')
        poster_url = item.get('images')[0].get('small')
        date = item.get('date')
        url = API_PLAYLIST.format(ref, pub)
        list_item = xbmcgui.ListItem(label=f'{title}')
        list_item.setArt({
            'poster': poster_url,
        })
        list_item.setInfo('video', {
            'plot': f'{subtitle}\n\n{date}\n{media}\n\n{expire}'
        })
        list_item.setProperty('inputstream', 'inputstream.adaptive')
        list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    TODO doc
    """
    params = dict(parse_qsl(paramstring))

    if not params:
        render_genres()
    elif 'genre_id' in params:
        render_catgories(genre_id=params.get('genre_id'), parent_title=params.get('parent_title'))
    else:
        print('else')


if __name__ == '__main__':
    router(sys.argv[2][1:])
