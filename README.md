#possibly-useful-scraps
A collection of possibly useful scraps so far containing a few PyGObject scripts.

#SimpleDBusNotifications:

Very simple DBus Notifications with hint and actions support.
It uses the default timeout and each subsequent
notification replaces the previous.
Although both Initialization and the Notify method call are asynchronous,
It is up to the application to decide/handle the synchronousity
of the actions callbacks. They will by default be called synchronously
in the main thread.

see the [wiki](https://github.com/JasonLG1979/possibly-useful-scraps/wiki/SimpleDBusNotifications) for documentation.

#GLib_async:

A decorator that can be used on free functions so they will be called asynchronously.(using python threads)

#GLib_idle:
GLib.idle_add decorator.

Turns:
```python
    def called_from_an_outside_thread(self, arg1, arg2, kwarg1=1, kwarg2=2):
        GLib.idle_add(lambda: self.do_in_main_thread(arg1, arg2, kwarg1=1, kwarg2=2)))
```

Into:
```python
    @GLib_idle
    def do_in_main_thread(arg1, arg2, kwarg1=1, kwarg2=2):
        #do awesome stuff
```

#GObject_signal_block:

Stops a signal handler from recursively calling it's self.

<i>Example:</i>
```python
    self.my_signal_handler = self.obj.connect('my-signal', self.on_my_signal, 'my-signal')

    @GObject_signal_block
    def on_my_signal(self, obj, signal, signal_name):
        #do stuff that would cause obj to emit 'my-signal' again
```

