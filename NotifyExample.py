import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from SimpleDBusNotifications import *

class NotificationsDemo(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Notifications Demo')
        self.supports_actions = False
        self.cute_animals = ''
        self.init_notifications()
        self.init_ui()

    def init_ui(self):
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.label = Gtk.Label()
        vbox.pack_start(self.label, True, True, 0)
        self.label.set_label('Notifications are Asynchronous.')
        self.button = Gtk.Button.new_with_label('Ask the most import of all questions...')
        self.button.connect('clicked', self.on_question_clicked)
        vbox.pack_start(self.button, True, True, 0)

    def init_notifications(self):
        def on_init_finish(caps):
            self.supports_actions = 'actions' in caps

        self.notification = SimpleDBusNotifications.async_init('Notifications Demo', on_init_finish)

    def on_question_clicked(self, button):
        self.send_first_notification()

    def send_first_notification(self):
        if self.supports_actions:
            self.set_actions()
            summary = 'Your notification server supports actions.'
            body = 'Which do you prefer?'
            icon = 'dialog-question'
        else:
            summary = 'Your notification server does not support actions.' 
            body = 'I guess we will never know if you prefer Puppies or Kittens.'
            icon = 'dialog-error'
        self.notification.new(summary, body, icon)
        if self.cute_animals:
            self.label.set_label('You preferred {} last time.'.format(self.cute_animals))
        else:
            self.label.set_label('They will not block the main thread.')

    def set_actions(self):
        self.notification.clear_actions()
        self.notification.add_action('action-id-puppies', 
                                     'Puppies',
                                     self.puppies_cb,
        )

        self.notification.add_action('action-id-kittens',
                                     'Kittens',
                                     self.kittens_cb,
        )

    def puppies_cb(self):
        self.cute_animals = 'Puppies'
        self.label.set_label('So you\'ll more than likely never see this.')
        self.you_prefer()

    def kittens_cb(self):
        self.cute_animals = 'Kittens'
        self.label.set_label('So you\'ll more than likely never see this.')
        self.you_prefer()

    def you_prefer(self):
        self.notification.clear_actions()
        summary = 'You have made your choice.'
        body = 'You prefer {}.'.format(self.cute_animals)
        icon = 'dialog-information'
        self.notification.new(summary, body, icon)
        self.button.set_label('Ask Again...')
        self.label.set_label('Are you sure you prefer {}?'.format(self.cute_animals))

if __name__ == '__main__':
    win = NotificationsDemo()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
