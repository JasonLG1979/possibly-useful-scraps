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
#GLib_async:

A decorator that can be used on free functions so they will be called asynchronously.(using python threads)
