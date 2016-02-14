# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 Innovate

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

import re, json

from resources.lib.libraries import client
from resources.lib.libraries import jsunpack

def resolve(url):
    try:
        result = client.source(url)
        url = re.findall('file: "(.+?)"',result)[0]
        return url
    except:
        client.printException('vidzi.resolve')
        return