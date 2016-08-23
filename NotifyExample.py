
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from SimpleDBusNotifications import *

class NotificationsDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Notifications Demo')
        self.supports_actions = False
        self.animal_one = ''
        self.animal_two = ''
        self.selected_animal = ''
        self.animals = ['Puppies', 'Kittens', 'Cows', 'Horses', 'Ponies', 'Dragons', 'Unicorns',
                        'Baby Seals', 'Whales', 'Dolphins', 'Sharks', 'Gold Fish', 'Manticores',
                        'Zebras', 'Lions', 'Tigers', 'Bears', 'Aardvarks', 'Panthers', 'Camels']
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
        def on_init_finish(server_info, capabilities):
            self.supports_actions = 'actions' in capabilities
            print('Server information:')
            for key, value in server_info.items():
                print(key, value)
            print('\n')
            print('Server Capabilities:')
            for capability in capabilities:
                print(capability)

        self.notification = SimpleDBusNotifications.async_init('Notifications Demo', on_init_finish)

    def set_animals(self):
        prev_animal_one = self.animal_one
        while True:
            animal = random.choice(self.animals)
            if animal != self.animal_one and animal != self.animal_two:
                self.animal_one = animal
                break

        while True:
            animal = random.choice(self.animals)
            if animal != self.animal_one and animal != self.animal_two and animal != prev_animal_one:
                self.animal_two = animal
                break

    def on_question_clicked(self, button):
        self.send_first_notification()

    def send_first_notification(self):
        if self.supports_actions:
            self.set_actions()
            summary = 'Your notification server supports actions.'
            body = 'Which do you prefer?'
            icon = 'dialog-question-symbolic'
        else:
            summary = 'Your notification server does not support actions.' 
            body = 'I guess we will never know which animals you prefer.'
            icon = 'dialog-error-symbolic'
        self.notification.new(summary, body, icon)
        if self.selected_animal:
            self.label.set_label('Well you don\'t like {}, how about one of these?'.format(self.selected_animal))
            self.button.set_label('No Those Suck To!!! Ask Me Again...')
        else:
            self.label.set_label('They will not block the main thread.')
            if self.supports_actions:
                self.button.set_label('Those Suck, Ask Me Again...')

    def set_actions(self):
        self.notification.clear_actions()
        self.set_animals()
        self.notification.add_action('action-id-animal-one', 
                                     self.animal_one,
                                     self.animal_one_cb,
        )

        self.notification.add_action('action-id-animal-two',
                                     self.animal_two,
                                     self.animal_two_cb,
        )

    def animal_one_cb(self):
        self.selected_animal = self.animal_one
        self.label.set_label('So you\'ll more than likely never see this.')
        self.you_prefer()

    def animal_two_cb(self):
        self.selected_animal = self.animal_two
        self.label.set_label('So you\'ll more than likely never see this.')
        self.you_prefer()

    def you_prefer(self):
        self.notification.clear_actions()
        summary = 'You have made your choice.'
        body = 'You prefer {}.'.format(self.selected_animal)
        icon = 'dialog-information-symbolic'
        # If notifications were not async(non-blocking)
        # you'd be able to see the label from the callbacks
        # until it unblocked.
        self.notification.new(summary, body, icon)
        self.button.set_label('No {} Suck!!! Ask Me Again...'.format(self.selected_animal))
        self.label.set_label('Are you sure you prefer {}?'.format(self.selected_animal))

if __name__ == '__main__':
    win = NotificationsDemo()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
