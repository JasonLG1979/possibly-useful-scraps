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

def GLib_async(on_success=None, on_failure=None, priority=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            def in_thread(args):
                priority, f, args, kwargs, on_success, on_failure = args
                try:
                    result = f(*args, **kwargs)
                    if on_success is not None:
                        GLib.idle_add(on_success, result, priority=priority)
                except Exception as e:
                    if on_failure is not None:
                        e.traceback = traceback.format_exc()
                        error = 'Unhandled exception in GLib_async call:\n{}'.format(e.traceback)
                        GLib.idle_add(on_failure, error, priority=priority)

            args = priority, f, args, kwargs, on_success, on_failure
            thread = threading.Thread(target=in_thread, args=(args,))
            thread.daemon = True
            thread.start()
        return run
    return wrapper
