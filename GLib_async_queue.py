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
import queue
import traceback
from gi.repository import GLib

__all__ = ['GLib_async_queue']

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = queue.PriorityQueue()
        self.fifo_priority = 0
        self.daemon = True
        self.start()
        
    def run(self):
        while True:
            priority, _, f, args, kwargs, on_done = self.queue.get()
            result = None
            error = None
            try:
                result = f(*args, **kwargs)
            except Exception as e:
                e.traceback = traceback.format_exc()
                error = 'Unhandled exception in GLib_async_queue call:\n{}'.format(e.traceback)
            if on_done:
                GLib.idle_add(on_done, result, error, priority=priority)

    def queue_task(self, priority, f, args, kwargs, on_done):
        self.fifo_priority += 1
        self.queue.put((priority, self.fifo_priority, f, args, kwargs, on_done))

worker = Worker()

def GLib_async_queue(on_done=None, priority=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            worker.queue_task(priority, f, args, kwargs, on_done)
        return run
    return wrapper
