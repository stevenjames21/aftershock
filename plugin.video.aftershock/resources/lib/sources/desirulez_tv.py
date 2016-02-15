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


import re,urllib,urlparse,random, datetime

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import metacache
from resources.lib import resolvers

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.desirulez.net'
        self.base_link_2 = 'http://www.desirulez.me'
        self.base_link_3 = 'http://www.desirulez.net'
        self.search_link = '/feed/?s=%s&submit=Search'

        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = ''
        self.now = datetime.datetime.now()


        self.star_plus_link = 'forumdisplay.php?f=42'
        self.zee_tv_link = 'forumdisplay.php?f=73'
        self.set_link = 'forumdisplay.php?f=63'
        self.life_ok_link = 'forumdisplay.php?f=1375'
        self.sahara_one_link = 'forumdisplay.php?f=134'
        self.star_jalsha_link = 'forumdisplay.php?f=667'
        self.colors_link = 'forumdisplay.php?f=176'
        self.sony_sab_link = 'forumdisplay.php?f=254'
        self.star_pravah_link = 'forumdisplay.php?f=1138'
        self.mtv_india_link = 'forumdisplay.php?f=339'
        self.channel_v_link = 'forumdisplay.php?f=633'
        self.utv_bindass_link = 'forumdisplay.php?f=504'
        self.utv_stars_link = 'forumdisplay.php?f=1274'
        self.hungama_link = 'forumdisplay.php?f=472'
        self.cartoon_network_link = 'forumdisplay.php?f=509'
        self.and_tv_link = 'forumdisplay.php?f=3138'
        self.colors_bangla_link = 'forumdisplay.php?f=2117'

        self.list = []

    def get_shows(self, name, url):
        try:
            result = ''
            shows = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.source('%s/%s' % (base_link,url))
                except: result = ''
                if 'forumtitle' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "h2", attrs = {"class" : "forumtitle"})

            for item in result:
                title = ''
                url = ''
                title = client.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})

                if not title:
                    title = client.parseDOM(item, "a", attrs = {"class":"title"})
                    if title:
                        title = title[0]
                    else :
                        title = client.parseDOM(item, "a")

                if type(title) is list and len(title) > 0:
                    title = str(title[0])
                url = client.parseDOM(item, "a", ret="href")

                if not url:
                    url = client.parseDOM(item, "a", attrs = {"class":"title"}, ret="href")

                if type(url) is list and len(url) > 0:
                    url = str(url[0])

                if not 'Past Shows' in title:
                    # name , title, poster, imdb, tmdb, tvdb, tvrage, year, poster, banner, fanart, duration
                    shows.append({'name':title, 'channel':name, 'title':title, 'url':url, 'poster': '0', 'banner': '0', 'fanart': '0', 'next': '0', 'tvrage':'0','year':'0','duration':'0','provider':'desirulez_tv'})
            return shows
        except:
            return

    def get_episodes(self, title, url):
        try :
            episodes = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            tvshowurl = url
            for base_link in links:
                try:
                    result = client.source(base_link + '/' + url)
                except: result = ''
                if 'threadtitle' in result: break

            rawResult = result.decode('iso-8859-1').encode('utf-8')


            result = client.parseDOM(rawResult, "h3", attrs = {"class" : "title threadtitle_unread"})
            result += client.parseDOM(rawResult, "h3", attrs = {"class" : "threadtitle"})

            for item in result:
                name = client.parseDOM(item, "a", attrs = {"class":"title"})
                name += client.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
                if type(name) is list:
                    name = name[0]
                url = client.parseDOM(item, "a", ret="href")
                if type(url) is list:
                    url = url[0]
                if "Online" not in name: continue
                name = name.replace(title, '').replace('Online','').replace('Watch','').replace('Video','')
                name = name.strip()
                episodes.append({'tvshowtitle':title, 'title':name, 'name':name,'url' : url, 'provider':'desirulez_tv', 'tvshowurl':tvshowurl})

            next = client.parseDOM(rawResult, "span", attrs={"class":"prev_next"})
            next = client.parseDOM(next, "a", attrs={"rel":"next"}, ret="href")[0]
            episodes[0].update({'next':next})
            return episodes
        except:
            client.printException('desirulez_tv.get_episodes(title=%s, url=%s)' % (title, url))
            return
    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            quality = ''
            sources = []

            result = ''
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try: result = client.source(base_link + '/' + url)
                except: result = ''
                if 'blockquote' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            ### DIRTY Implementation
            import BeautifulSoup
            soup = BeautifulSoup.BeautifulSoup(result).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]

            for e in soup.findAll('br'):
                e.extract()
            if soup.has_key('div'):
                soup = soup.findChild('div', recursive=False)
            urls = []
            quality = 'SD'
            for child in soup.findChildren():
                if (child.getText() == '') or ((child.name == 'font' or child.name == 'a') and re.search('DesiRulez', str(child.getText()),re.IGNORECASE)):
                    continue
                elif (child.name == 'font') and re.search('Links|Online|Link',str(child.getText()),re.IGNORECASE):
                    if len(urls) > 0:
                        tmpHost = host.lower()
                        indx = host.find('[')
                        if indx > 0 :
                            tmpHost = tmpHost[:indx-1]
                        url = "##".join(urls)
                        sources.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'DesiRulez','url':url})
                        urls = []
                    host = child.getText()
                    if '720p HD' in host:
                        quality = 'HD'
                    elif 'DVD' in host:
                        quality = 'SD'
                    host = host.replace('Online','').replace('Links','').replace('Link','').replace('Quality','').replace('Watch','').replace('-','').replace('Download','').replace('  ','').replace('720p HD','').replace('DVD','').strip()
                elif (child.name =='a') and not child.getText() == 'registration':
                    urls.append(str(child['href']))

            if len(urls) > 0:
                url = "##".join(urls)
                sources.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'DesiRulez', 'url': url})
            return sources
        except:
            client.printException('desirulez_tv.get_sources')
            return sources


    def resolve(self, url):
        try:
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                links.append(resolvers.request(item))
            url = links
            return url
        except:
            return



