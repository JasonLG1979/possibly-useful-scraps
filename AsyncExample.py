
import time
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from SimpleDBusNotifications import *
from GLib_async import *

class GLibAsyncDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='GLib_async Demo')
        self.ui_loop_timer_id = 0
        self.time_sec = 0
        self.init_ui()
        self.init_notifications()

    def init_ui(self):
        self.set_border_width(10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.label = Gtk.Label()
        vbox.pack_start(self.label, True, True, 0)
        self.label.set_label('00:00')
        self.button = Gtk.Button.new_with_label('Reset Clock')
        self.button.connect('clicked', self.reset_clock)
        vbox.pack_start(self.button, True, True, 0)
        self.create_ui_loop()

    def init_notifications(self):
        def on_init_finish(caps):
            self.async_sleep()

        self.notification = SimpleDBusNotifications.async_init('GLib_async Demo', on_init_finish)

    def update_time(self):
        self.time_sec += 1
        self.label.set_label(self.format_time(self.time_sec))
        return True

    def reset_clock(self, *ignore):
        # The display clock is totally independent of async_sleep
        # It continues to tick away even though async_sleep spends
        # most of it's time sleeping unless you reset it... 
        self.destroy_ui_loop()
        self.create_ui_loop()

    def format_time(self, milliseconds):
        s, ms = divmod(milliseconds, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h:
            return '{:02d}:{:02d}:{:02d}:{:03d}'.format(h,m,s,ms)
        else:
            return '{:02d}:{:02d}:{:03d}'.format(m,s, ms)

    def async_sleep(self):
        def wake_back_up(result, error):
            if error:
                print(error)
                return
            self.send_wake_notification(result)

        @GLib_async_func(on_done=wake_back_up, PRIORITY=GLib.PRIORITY_LOW)
        def go_to_sleep(sleep_time):
            # If this sleep were done in the main thread
            # the clock would stop.
            went_to_sleep = time.time()
            time.sleep(sleep_time)
            woke_up = time.time()
            return '{:6.3f}'.format(round(woke_up - went_to_sleep, 3))

        go_to_sleep(random.uniform(5.0, 10.0))

    def create_ui_loop(self):
        if not self.ui_loop_timer_id:
            self.ui_loop_timer_id = GLib.timeout_add(1, self.update_time)

    def destroy_ui_loop(self):
        if self.ui_loop_timer_id:
            GLib.source_remove(self.ui_loop_timer_id)
            self.ui_loop_timer_id = 0
            self.time_sec = 0
            self.label.set_label('00:00')

    def send_wake_notification(self, secs):
        summary = 'Just Woke Back Up.'
        body = 'Slept for about {} seconds.'.format(secs)
        icon = 'dialog-information'
        self.notification.new(summary, body, icon)
        self.async_sleep()

if __name__ == '__main__':
    win = GLibAsyncDemo()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
