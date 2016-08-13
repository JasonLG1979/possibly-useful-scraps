#possibly-useful-scraps
A collection of possibly useful scraps so far containing a couple PyGObject scripts.
#SimpleDBusNotifications:

Very simple DBus Notifications with hint and actions support.
It uses the default timeout and each subsequent
notification replaces the previous.
Although both Initialization and the Notify method call are asynchronous,
It is up to the application to decide/handle the synchronousity
of the actions callbacks. They will by default be called synchronously
in the main thread.

<i>Example:</i>
```python
class Notify:
    def __init__(self, parent):
    self.parent = parent
    self.notification = None
    self.supports_actions = False
    self.on_init()

    def on_init(self):
        def on_init_finish(caps):
            self.supports_actions = 'actions' in caps
            self.parent.connect('some-bool-signal', self.set_notification)

        self.notification = SimpleDBusNotifications.async_init('My Awesome App', on_init_finish)

    def set_notification(self, obj, signal_value_bool):
        if self.supports_actions:
            self.set_actions(signal_value_bool)
        summary = 'The Signal Value was {}!!!'.format(signal_value_bool) 
        body = 'Blah, blah, blah...'
        icon = 'dialog-information' # icon name or a path to an image
        self.notification.new(summary, body, icon)

    def set_actions(self, signal_value_bool):
        self.notification.clear_actions()
        if signal_value_bool:
            self.notification.add_action('action-id-True', 
                                         'Print True',
                                         self.true_cb,
            )

        else:
            self.notification.add_action('action-id-False',
                                         'Print False',
                                         self.false_cb,
            )

    def true_cb(self):
        print('True')

    def false_cb(self):
        print('False')
```
#GObjectAsync:

A decorator that can be used on free functions so they will be called asynchronously.(using python threads)

<i>Example:</i>

```python
    def do_async_stuff(self, input_string):
        def on_async_done(result, error):
            # Do stuff with the result and handle errors in the main thread.
            if error:
                print(error)
            elif result:
                print(result)

        @async_function(on_done=on_async_done)
        def do_expensive_stuff_in_thread(input_string):
            # Pretend to do expensive stuff...
            time.sleep(10)
            stuff = input_string + ' Done in a different thread.'
            return stuff

        do_expensive_stuff_in_thread(input_string)
```
