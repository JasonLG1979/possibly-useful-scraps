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

import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from GioNotify import GioNotify

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
        self.label2 = Gtk.Label()
        self.label2.set_use_markup(True)
        vbox.pack_start(self.label2, True, True, 0)

    def init_notifications(self):
        def on_init_finish(server_info, capabilities):
            self.supports_actions = 'actions' in capabilities
            label_text = []
            label_text.append('<b><big>Server information:</big></b>')
            for key, value in server_info.items():
                label_text.append('<small>{}: {}</small>'.format(key, value))
            label_text.append('\n<b><big>Server Capabilities:</big></b>')
            for capability in capabilities:
                label_text.append('<small>{}</small>'.format(capability))
            label_text = '\n'.join(label_text)
            self.label2.set_label(label_text)

        self.notification = GioNotify.async_init('Notifications Demo', on_init_finish)

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
        self.notification.show_new(summary, body, icon)
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
        self.notification.show_new(summary, body, icon)
        self.button.set_label('No {} Suck!!! Ask Me Again...'.format(self.selected_animal))
        self.label.set_label('Are you sure you prefer {}?'.format(self.selected_animal))

if __name__ == '__main__':
    win = NotificationsDemo()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
