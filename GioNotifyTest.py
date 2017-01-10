#
# Copyright (C) 2016 Jason Gray <jasonlevigray3@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE

# See <https://developer.gnome.org/notification-spec/> and
# <https://github.com/JasonLG1979/possibly-useful-scraps/wiki/GioNotify>
# for documentation.

from GioNotify import GioNotify

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, GObject, Gtk


class GioNotifyTest(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='GioNotify Test')
        self.notification = GioNotify.async_init('GioNotify Test', self.on_init_finish)
        self.supports_actions = False
        self.image_uri = None
        self.signals_message = []
        self.set_default_size(600, -1)
        self.set_resizable(False)
        self.set_border_width(10)
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.set_title('GioNotify Test')
        self.set_titlebar(self.headerbar)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        title = Gtk.Label()
        title.set_label('Notification Title:')
        vbox.pack_start(title, True, True, 0)
        self.title_entry = Gtk.Entry()
        vbox.pack_start(self.title_entry, True, True, 0)
        body = Gtk.Label()
        body.set_label('Notification body:')
        vbox.pack_start(body, True, True, 0)
        self.body_entry = Gtk.Entry()
        vbox.pack_start(self.body_entry, True, True, 0)
        self.action_label = Gtk.Label()
        choose_image_button = Gtk.Button('Select a Notification Image')
        choose_image_button.connect("clicked", self.on_file_clicked)
        vbox.pack_start(choose_image_button, True, True, 0)
        self.action_label.set_label('Action Button Label:')
        vbox.pack_start(self.action_label, True, True, 0)
        self.action_entry = Gtk.Entry()
        vbox.pack_start(self.action_entry, True, True, 0)
        show_notification_button = Gtk.Button('Show Notification')
        show_notification_button.connect("clicked", self.on_show_notification)
        vbox.pack_start(show_notification_button, True, True, 0)
        close_notification_button = Gtk.Button('Close Notification')
        close_notification_button.connect("clicked", lambda *ignore: self.notification.close())
        vbox.pack_start(close_notification_button, True, True, 0)
        self.server_info_caps = Gtk.Label()
        self.server_info_caps.set_use_markup(True)
        vbox.pack_start(self.server_info_caps, True, True, 0)
        signal = Gtk.Label()
        signal.set_use_markup(True)
        vbox.pack_start(signal, True, True, 0)
        signal.set_label('<b><big>Signals:</big></b>')
        self.signals_label = Gtk.Label()
        vbox.pack_start(self.signals_label, True, True, 0)

    def on_init_finish(self, server_info, capabilities):
        self.notification.connect('action-invoked', self.on_action_invoked)
        self.notification.connect('closed', self.on_closed)

        self.supports_actions = 'actions' in capabilities

        if not self.supports_actions:
            self.action_label.set_label('Action Buttons not supported by Notification server')
            self.action_entry.set_sensitive(False)

        label_text = []

        label_text.append('<b><big>Server information:</big></b>')
        for key, value in server_info.items():
            label_text.append('<small>{}: {}</small>'.format(key, value))

        label_text.append('\n<b><big>Server Capabilities:</big></b>')
        for capability in capabilities:
            label_text.append('<small>{}</small>'.format(capability))

        label_text = '\n'.join(label_text)

        self.server_info_caps.set_label(label_text)

    def on_show_notification(self, *ignore):
        def dummy_action_callback():
            pass

        if self.supports_actions:
            self.notification.clear_actions()
            action = self.action_entry.get_text()
            if action:
                self.notification.add_action(
                    action,
                    action,
                    dummy_action_callback,
                )

        summary = self.title_entry.get_text()
        body = self.body_entry.get_text()
        if self.image_uri:
            icon = self.image_uri
        else:
            icon = 'dialog-information-symbolic'

        self.signals_message = []
        self.signals_label.set_label('')

        self.notification.show_new(summary, body, icon)

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            'Please Choose an Image', self,
            Gtk.FileChooserAction.OPEN,
            ('_Cancel', Gtk.ResponseType.CANCEL, '_Open', Gtk.ResponseType.OK),
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.image_uri = dialog.get_uri()

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('png')
        filter_text.add_mime_type('image/png')
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name('jpg')
        filter_text.add_mime_type('image/jpg')
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name('jpeg')
        filter_text.add_mime_type('image/jpeg')
        dialog.add_filter(filter_text)

    def on_action_invoked(self, obj, action_id):
        self.signals_message.append('action invoked: {}'.format(action_id))

    def on_closed(self, obj, reason):
        self.signals_message.append('closed reason: {}'.format(reason.explanation))
        label_text = '\n'.join(self.signals_message)
        self.signals_label.set_label(label_text)

if __name__ == '__main__':
    win = GioNotifyTest()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
