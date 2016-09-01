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

#See <https://developer.gnome.org/notification-spec/> and 
#<https://github.com/JasonLG1979/possibly-useful-scraps/wiki/SimpleDBusNotifications>
#for documentation.

from gi.repository import GObject, GLib, Gio

class SimpleDBusNotifications(Gio.DBusProxy):

    __gsignals__ = {
        'ActionInvoked': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'NotificationClosed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self, **kwargs):
        super().__init__(
            g_bus_type=Gio.BusType.SESSION,
            g_interface_name='org.freedesktop.Notifications',
            g_name='org.freedesktop.Notifications',
            g_object_path='/org/freedesktop/Notifications',
            **kwargs
        )

    @classmethod
    def async_init(cls, app_name, callback):
        def on_init_finish(self, result, callback):
            self.init_finish(result)
            self.call('GetCapabilities',
                      None,
                      Gio.DBusCallFlags.NONE,
                      -1,
                      None,
                      on_GetCapabilities_finish,
                      callback,
            )

        def on_GetCapabilities_finish(self, result, callback):
            caps = self.call_finish(result).unpack()[0]
            user_data = callback, caps
            self.call('GetServerInformation',
                      None,
                      Gio.DBusCallFlags.NONE,
                      -1,
                      None,
                      on_GetServerInformation_finish,
                      user_data,
            )

        def on_GetServerInformation_finish(self, result, user_data):
            callback, caps = user_data
            info = self.call_finish(result).unpack()
            server_info = {'name': info[0],
                           'vendor': info[1],
                           'version': info[2],
                           'spec_version': info[3],
            }

            self._replace_id = 0
            self._actions = []
            self._callbacks = {}
            self._hints = {}
            self._app_name = app_name
            
            callback(server_info, caps)

        self = cls()     
        self.init_async(GLib.PRIORITY_DEFAULT, None, on_init_finish, callback)
        return self

    def show_new(self, summary, body, icon):
        def on_Notify_finish(self, result):
            self._replace_id = self.call_finish(result).unpack()[0]

        args = GLib.Variant('(susssasa{sv}i)', (self._app_name, self._replace_id,
                                                icon, summary, body,
                                                self._actions, self._hints, -1))

        self.call('Notify',
                  args,
                  Gio.DBusCallFlags.NONE,
                  -1,
                  None,
                  on_Notify_finish,
        )

    def add_action(self, action_id, label, callback):    
        self._actions += [action_id, label]
        self._callbacks[action_id] = callback

    def clear_actions(self):
        self._actions.clear()
        self._callbacks.clear()

    def set_hint(self, key, value):
        if value is None:
            if key in self._hints:
                del self._hints[key]
        else:
            self._hints[key] = value

    def do_g_signal(self, sender_name, signal_name, parameters):
        id, signal_value = parameters.unpack()
        if id != self._replace_id:
           return
        self.emit(signal_name, signal_value)
        if signal_name == 'ActionInvoked':
            self._callbacks[signal_value]()

    def __getattr__(self, name):
        # pygobject ships an override that breaks our usage
        return object.__getattr__(self, name)
