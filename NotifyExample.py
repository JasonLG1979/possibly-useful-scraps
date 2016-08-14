
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from SimpleDBusNotifications import *

class NotifyExample:
    def __init__(self):
        self.notification = None
        self.supports_actions = False
        self.on_init()

    def on_init(self):
        def on_init_finish(caps):
            self.supports_actions = 'actions' in caps
            self.notification.connect('g-signal', self.g_signal_handler)
            self.set_notification()

        self.notification = SimpleDBusNotifications.async_init('Puppies vs Kittens', on_init_finish)

    def g_signal_handler(self, notification, sender_name, signal_name, parameters):
        id, signal_value = parameters.unpack()
        if id != self.notification.id:#we only care about our notification
           return
        if signal_name == 'NotificationClosed':
            Gtk.main_quit() 

    def set_notification(self):
        if self.supports_actions:
            self.set_actions()
            summary = 'Your notification server supports actions.'
            body = 'Which do you prefer?'
            icon = 'dialog-question'
        else:
            summary = 'Your notification server does not support actions.' 
            body = 'I guess we will never know if you prefer puppies or kittens.'
            icon = 'dialog-error'
        self.notification.new(summary, body, icon)

    def set_actions(self):
        self.notification.add_action('action-id-puppies', 
                                     'Puppies',
                                     self.puppies_cb,
        )

        self.notification.add_action('action-id-kittens',
                                     'Kittens',
                                     self.kittens_cb,
        )

    def puppies_cb(self):
        print('You like puppies...')

    def kittens_cb(self):
        print('You like kittens...')

if __name__ == '__main__':
    app = NotifyExample()
    Gtk.main()
