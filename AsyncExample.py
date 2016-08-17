
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
        self.set_default_size(350, -1)
        self.set_resizable(False)
        self.set_border_width(10)
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.set_title('Async Demo')
        self.headerbar.set_subtitle('00:00:00')
        self.set_titlebar(self.headerbar)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        self.button = Gtk.Button.new_with_label('Start Clock')
        self.button.connect('clicked', self.clock_toggle)
        vbox.pack_start(self.button, False, False, 0)
        self.notification = SimpleDBusNotifications.async_init('Async Demo', self.init_notifications_finish)

    def init_notifications_finish(self, caps):         
        self.async_sleep()
        self.clock_toggle()

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

    def clock_toggle(self, *ignore): 
        if self.ui_loop_timer_id:
            GLib.source_remove(self.ui_loop_timer_id)
            self.ui_loop_timer_id = 0
            self.time_sec = 0
            self.headerbar.set_subtitle('00:00:00')
            self.button.set_label('Start Clock')
        else:
            self.ui_loop_timer_id = GLib.timeout_add(1000, self.update_time)
            self.button.set_label('Stop Clock')

    def async_sleep(self):
        # When the work is done the callback recieves
        # the result or error in the main thread.
        def wake_back_up(result, error):
            if error:
                print(error)
                return
            self.send_wake_notification(result)

                    # async callback      # priority at which the main thread is re-entered
        @GLib_async(on_done=wake_back_up, PRIORITY=GLib.PRIORITY_LOW)
        # Work done in seperate thread.
        def go_to_sleep(sleep_time):
            went_to_sleep = time.time()
            time.sleep(sleep_time)
            woke_up = time.time()
            return round(woke_up - went_to_sleep)

        go_to_sleep(random.randint(5, 15))

    def send_wake_notification(self, secs):
        summary = 'Just Woke Back Up.'
        body = 'Slept for about {} seconds that time.'.format(secs)
        icon = 'dialog-information-symbolic'
        self.notification.new(summary, body, icon)
        self.async_sleep()

if __name__ == '__main__':
    win = GLibAsyncDemo()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
