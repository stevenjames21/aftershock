# -*- coding: utf-8 -*-
# AftershockNow Guide
# Developed by IDev
# Forked from FTV Guide:
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import sys, xbmc
from resources.lib import gui
from resources.lib import logger
from resources.lib.strings import *

try:
    if ADDON.getSetting('xmltv.useremail') == '' :
        logger.log('NO USEREMAIL EXITING', 'main', xbmc.LOGNOTICE)
        sys.exit()
    w = gui.TVGuide()
    w.doModal()
    del w

except:
    import sys
    import traceback as tb
    (etype, value, traceback) = sys.exc_info()
    tb.print_exception(etype, value, traceback)
