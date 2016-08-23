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
        self.set_default_size(350, -1)
        self.set_resizable(False)
        self.set_border_width(10)
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.set_title('Queue Test')
        self.set_titlebar(self.headerbar)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        self.button = Gtk.Button.new_with_label('Print Queue Test Results')
        self.button.connect('clicked', self.async_queue_test)
        vbox.pack_start(self.button, False, False, 0)

    def async_queue_test(self, *ignore):
        def print_message(result, error):
            priority, order_called = result
            self.return_order_counter += 1
            print('{} priority: Call order {}, return order {}.'.format(priority, order_called, self.return_order_counter))

        @GLib_async_queue(on_done=print_message, priority=GLib.PRIORITY_HIGH)
        def say_high(order_called):
            time.sleep(random.randint(1, 5))
            return 'High', order_called

        @GLib_async_queue(on_done=print_message, priority=GLib.PRIORITY_DEFAULT)
        def say_default(order_called):
            time.sleep(random.randint(1, 5))
            return 'Default', order_called

        @GLib_async_queue(on_done=print_message, priority=GLib.PRIORITY_LOW)
        def say_low(order_called):
            time.sleep(random.randint(1, 5))
            return 'Low', order_called

        def low():
            self.call_order_counter += 1
            say_low(self.call_order_counter)

        def default():
            self.call_order_counter += 1
            say_default(self.call_order_counter)

        def high():
            self.call_order_counter += 1
            say_high(self.call_order_counter)

        test_calls = [low, low, low, low, default, default, default, default, high, high, high, high]

        random.shuffle(test_calls)

        for call in test_calls:
            call()

if __name__ == '__main__':
    win = QueueTest()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
