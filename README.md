#possibly-useful-scraps
A collection of possibly useful scraps so far containing a few PyGObject scripts.

#SimpleDBusNotifications:

see the [wiki](https://github.com/JasonLG1979/possibly-useful-scraps/wiki/SimpleDBusNotifications) for documentation.

#GLib_async:

A decorator that can be used on free functions so they will be called asynchronously, Both to the main thread and to themselves.

#GLib_async_queue:

Works very similar to GLib_async except where GLib_async spawns a new thread for each call GLib_async_queue has just one worker thread. So it can be said that while it operates asynchronously to the main thread all decorated functions are synchronous as a whole group and are excuted in FIFO order via a queue.

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

