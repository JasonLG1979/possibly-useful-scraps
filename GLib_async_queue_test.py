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

import time
import random
from GLib_async_queue import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class QueueTest(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Queue Test')
        self.call_order_counter = 0
        self.return_order_counter = 0
        self.complete_message = []
        self.set_default_size(500, -1)
        self.set_resizable(False)
        self.set_border_width(10)
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.set_title('Queue Test')
        self.headerbar.set_subtitle('00:00:00')
        self.set_titlebar(self.headerbar)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        self.button = Gtk.Button.new_with_label('Get Queue Test Results')
        self.button.connect('clicked', self.async_queue_test)
        vbox.pack_start(self.button, False, False, 0)
        self.label = Gtk.Label()
        vbox.pack_start(self.label, True, True, 0)
        self.time_sec = 0
        GLib.timeout_add(1000, self.update_time)

    def async_queue_test(self, *ignore):
        self.button.set_sensitive(False)
        self.call_order_counter = 0
        self.return_order_counter = 0
        self.label.set_label('')
        self.complete_message = []

        def get_message(result):
            priority, order_called, time_slept = result
            self.return_order_counter += 1
            self.complete_message.append('{} priority: Call order {}, '
                                         'return order {}. Slept for {} secs'.format(priority,
                                                                                     order_called,
                                                                                     self.return_order_counter,
                                                                                     time_slept),
            )

            label_text = '\n'.join(self.complete_message)
            self.label.set_label(label_text)
            if self.return_order_counter == self.call_order_counter:
                self.button.set_sensitive(True)

        def get_error(error):
            self.label.set_label(error)

        @GLib_async_queue(on_success=get_message, on_failure=get_error, priority=GLib.PRIORITY_HIGH)
        def high(order_called, sleep_time):
            went_to_sleep = time.time()
            time.sleep(sleep_time)
            time_slept = round(time.time() - went_to_sleep, 3)
            return 'High', order_called, time_slept

        @GLib_async_queue(on_success=get_message, on_failure=get_error, priority=GLib.PRIORITY_DEFAULT)
        def default(order_called, sleep_time):
            went_to_sleep = time.time()
            time.sleep(sleep_time)
            time_slept = round(time.time() - went_to_sleep, 3)
            return 'Default', order_called, time_slept

        @GLib_async_queue(on_success=get_message, on_failure=get_error, priority=GLib.PRIORITY_LOW)
        def low(order_called, sleep_time):
            went_to_sleep = time.time()
            time.sleep(sleep_time)
            time_slept = round(time.time() - went_to_sleep, 3)
            return 'Low', order_called, time_slept

        for i in range(random.randint(2, 24)):
            random_call = random.choice([high, default, low])
            self.call_order_counter += 1
            random_call(self.call_order_counter, random.uniform(0.1, 1.0))

    def update_time(self):
        self.time_sec += 1
        time_int = self.time_sec
        s = time_int % 60
        time_int //= 60
        m = time_int % 60
        time_int //= 60
        h = time_int
        self.headerbar.set_subtitle('{:02d}:{:02d}:{:02d}'.format(h, m, s))
        return True

if __name__ == '__main__':
    win = QueueTest()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
