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
API_GENRES = f'{API_BASE}/genre/{{}}'
API_LIST = f'{API_BASE}/list/{{}}'
API_PLAYLIST = f'{API_BASE}/playlist/{{}}'

# plugin url
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

def get_url(**kwargs):
    """
    TODO
    """
    return f'{_URL}?{urlencode(kwargs)}'


def render(parent_title='', genre_id=''):
    print(API_GENRES.format(genre_id))
    resp_json = fetch_json(url=API_GENRES.format(genre_id))
    xbmcplugin.setPluginCategory(_handle, parent_title)
    xbmcplugin.setContent(_handle, 'videos')

    is_list = True
    for result in resp_json:
        title = result.get('name')
        genre_id = result.get('id')
        result_type = result.get('type')
        list_item = xbmcgui.ListItem(label=title)

        url = None
        if result_type == 'episode':
            is_list = False
            episode_id = result.get('id')
            title = result.get('seriesTitle')
            thumbnail = result.get('thumbnail')
            details = result.get('details')
            url = API_PLAYLIST.format(episode_id)
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({
                'poster': thumbnail,
            })
            list_item.setInfo('video', {
                'plot': details
            })
            list_item.setProperty('inputstream', 'inputstream.adaptive')
            list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            xbmc.executebuiltin(f'Container.SetViewMode({VIEW_INFO_WALL})')
        else:
            # top level
            url = get_url(genre_id=genre_id, parent_title=title)
            xbmc.executebuiltin(f'Container.SetViewMode({VIEW_WIDE_LIST})')
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_list)
    xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    TODO doc
    """
    params = dict(parse_qsl(paramstring))
    render(genre_id=params.get('genre_id', ''), parent_title=params.get('parent_title'))


if __name__ == '__main__':
    router(sys.argv[2][1:])
