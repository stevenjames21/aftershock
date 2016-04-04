# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys,urllib

from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import views
from resources.lib.sources import sources

class channels:
    def __init__(self):
        self.list = []

    def get(self):
        try :
            self.list.extend(sources().getLiveSources())
            self.list = sorted(self.list, key=lambda k: k['name'])
            self.channelDirectory(self.list)
        except :
            client.printException('')
            pass

    def channelDirectory(self, items):
        if items == None or len(items) == 0: return

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart = control.addonFanart()
        sysaddon = sys.argv[0]


        for i in items:
            try:
                label = "%s" % (i['name'])
                sysname = urllib.quote_plus(i['name'])

                poster, banner = i['poster'], i['poster']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster

                url = i['url']

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'banner': banner})
                except: pass

                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setProperty('Video', 'true')
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems([], replaceItems=True)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            except:
                pass

        control.content(int(sys.argv[1]), 'video')
        control.directory(int(sys.argv[1]), cacheToDisc=False)
        views.setView('movies', {'skin.confluence': 500})