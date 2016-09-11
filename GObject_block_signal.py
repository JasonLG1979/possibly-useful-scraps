#
# Copyright (C) 2016 Jason Gray <jasonlevigray3@gmail.com>
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from gi.repository import GObject

def GObject_block_signal(signal_name):
    def wrapper(f):
        def run(self, obj, signal):
            signal_id, detail = GObject.signal_parse_name(signal_name, obj, False)
            handler_id = GObject.signal_handler_find(obj,
                                                     GObject.SignalMatchType.DETAIL,
                                                     signal_id,
                                                     detail,
                                                     None,
                                                     None,
                                                     None,
            )

            with obj.handler_block(handler_id):
                f(self, obj, signal)
        return run
    return wrapper
