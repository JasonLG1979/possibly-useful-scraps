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

#Inspired by <https://gist.github.com/diosmosis/1132418> (Author name and License unknown),
#and <https://github.com/pithos/pithos/blob/master/pithos/gobject_worker.py>
#gobject_worker.py Copyright (C) 2010-2012 Kevin Mehall <km@kevinmehall.net>
#License GNU General Public License version 3.

import threading
import traceback
from gi.repository import GLib

def GLib_async(on_done=None, PRIORITY=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            def in_thread(args):
                f, args, kwargs, on_done, PRIORITY = args
                result = None
                error = None
                try:
                    result = f(*args, **kwargs)
                except Exception as e:
                    e.traceback = traceback.format_exc()
                    error = 'Unhandled exception in async call:\n{}'.format(e.traceback)
                if on_done:
                    GLib.idle_add(on_done, result, error, priority=PRIORITY)

            args = f, args, kwargs, on_done, PRIORITY
            thread = threading.Thread(target=in_thread, args=(args,))
            thread.daemon = True
            thread.start()
        return run
    return wrapper
