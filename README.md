#possibly-useful-scraps
A collection of possibly useful scraps so far containing a few PyGObject scripts.

#SimpleDBusNotifications:

see the [wiki](https://github.com/JasonLG1979/possibly-useful-scraps/wiki/SimpleDBusNotifications) for documentation.

#GLib_async:

A decorator that can be used on free functions so they will be called asynchronously, Both to the main thread and to themselves.

#GLib_async_queue:

A single worker thread that runs asynchronous to the main thread that uses a hybrid FIFO/Priority based queue. Tasks can be asigned a Priority via the optional priority kwarg. (GLib.PRIORITY_DEFAULT_IDLE is the deafult priority) Tasks will be excuted in the order of priority, tasks with the same priority will be excuted FIFO.

An example output of [GLib_async_queue_test.py](https://github.com/JasonLG1979/possibly-useful-scraps/blob/master/GLib_async_queue_test.py)

```bash
High priority: Call order 2, return order 1.
High priority: Call order 3, return order 2.
Default priority: Call order 4, return order 3.
Default priority: Call order 6, return order 4.
Low priority: Call order 1, return order 5.
Low priority: Call order 5, return order 6.
```

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

