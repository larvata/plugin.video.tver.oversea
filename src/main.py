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

API_BASE = 'http://tver.larvata.me:5433/api'
# API_BASE = 'http://localhost:5433/api'
API_GENRES = f'{API_BASE}/genre?href={{}}'
API_LIST = f'{API_BASE}/list/{{}}'
API_PLAYLIST = f'{API_BASE}/playlist/{{}}/{{}}'


# plugin url
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

def get_url(**kwargs):
    """
    TODO
    """
    return f'{_URL}?{urlencode(kwargs)}'


def render(parent_title='', genre_href=''):
    resp_json = fetch_json(url=API_GENRES.format(genre_href))
    xbmcplugin.setPluginCategory(_handle, parent_title)
    xbmcplugin.setContent(_handle, 'videos')

    is_list = True
    for genre in resp_json:
        title = genre.get('title')
        href = genre.get('href')
        genre_type = genre.get('type')
        list_item = xbmcgui.ListItem(label=title)

        url = None
        if genre_type == 'catchup':
            is_list = False
            pub = genre.get('publisher_id')
            ref = genre.get('reference_id')
            title = genre.get('title')
            subtitle = genre.get('subtitle')
            media = genre.get('media')
            expire = genre.get('expire')
            poster_url = genre.get('images')[0].get('image')
            date = genre.get('date')
            url = API_PLAYLIST.format(pub, ref)
            list_item = xbmcgui.ListItem(label=f'{title}')
            list_item.setArt({
                'poster': poster_url,
            })
            list_item.setInfo('video', {
                'plot': f'{date}\n{expire}\n{media}\n\n{subtitle}'
            })
            list_item.setProperty('inputstream', 'inputstream.adaptive')
            list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        elif genre_type == 'special':
            url = get_url(genre_href=href, parent_title=title)
        else:
            # toplevel
            url = get_url(genre_href=href, parent_title=title)
        # elif genre_type == 'section':
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_list)

    if is_list:
        xbmc.executebuiltin(f'Container.SetViewMode({VIEW_WIDE_LIST})')
    else:
        xbmc.executebuiltin(f'Container.SetViewMode({VIEW_INFO_WALL})')
    xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    TODO doc
    """
    params = dict(parse_qsl(paramstring))
    render(genre_href=params.get('genre_href', ''), parent_title=params.get('parent_title'))


if __name__ == '__main__':
    router(sys.argv[2][1:])
