# -*- coding: utf-8 -*-

'''
    Copyright (C) 2015 lamdba

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


import re,unicodedata

def movie(title):
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def tv(title):
    title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def live(title):
    title = title.upper()
    title = re.sub('USA| US | UK| AU|APAC|EUROPE', '', title)
    title = re.sub('CENIMA', 'CINEMA', title)
    title = re.sub('&TV', 'AND TV', title)
    title = title.strip()
    return title

def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        t = ''
        for i in title:
            c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))
            c = c.encode("ascii","ignore").strip()
            if i == ' ': c = i
            t += c

        return t.encode("utf-8")
    except:
        return title