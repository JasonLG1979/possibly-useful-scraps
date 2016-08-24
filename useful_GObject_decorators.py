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

#GLib_async and GLib_async_queue decorators inspired by 
#<https://gist.github.com/diosmosis/1132418> (Author name and License unknown),
#and <https://github.com/pithos/pithos/blob/master/pithos/gobject_worker.py>
#gobject_worker.py Copyright (C) 2010-2012 Kevin Mehall <km@kevinmehall.net>
#License GNU General Public License version 3.

import threading
import queue
import traceback
from gi.repository import GObject, GLib

__all__ = ['GLib_async', 'GLib_idle', 'GObject_block_signal', 'GLib_async_queue']

def GLib_async(on_success=None, on_failure=None, priority=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            def in_thread(args):
                priority, f, args, kwargs, on_success, on_failure = args
                try:
                    result = f(*args, **kwargs)
                    if on_success is not None and result is not None:
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

def GLib_idle(priority=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            GLib.idle_add(lambda: f(*args, **kwargs), priority=priority)
        return run
    return wrapper

def GObject_block_signal(signal_name):
    def wrapper(f):
        def run(self, obj, signal):
            signal_id, detail = GObject.signal_parse_name(signal_name, obj, False)
            handler_id = GObject.signal_handler_find(obj, GObject.SignalMatchType.DETAIL, signal_id, detail)
            with obj.handler_block(handler_id):
                f(self, obj, signal)
        return run
    return wrapper

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = queue.PriorityQueue()
        self.fifo_priority = 0
        self.daemon = True
        self.start()
        
    def run(self):
        while True:
            priority, _, f, args, kwargs, on_success, on_failure = self.queue.get()
            try:
                result = f(*args, **kwargs)
                if on_success is not None and result is not None:
                    GLib.idle_add(on_success, result, priority=priority)
            except Exception as e:
                if on_failure is not None:
                    e.traceback = traceback.format_exc()
                    error = 'Unhandled exception in GLib_async_queue call:\n{}'.format(e.traceback)
                    GLib.idle_add(on_failure, error, priority=priority)

    def queue_task(self, priority, f, args, kwargs, on_success, on_failure):
        self.fifo_priority += 1
        self.queue.put((priority, self.fifo_priority, f, args, kwargs, on_success, on_failure))

worker = Worker()

def GLib_async_queue(on_success=None, on_failure=None, priority=GLib.PRIORITY_DEFAULT_IDLE):
    def wrapper(f):
        def run(*args, **kwargs):
            worker.queue_task(priority, f, args, kwargs, on_success, on_failure)
        return run
    return wrapper
    
