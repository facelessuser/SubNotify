# User Guide

## Using SubNotify in a Plugin

sub_notify
: 
    Command that displays the notification for Sublime Text.

    **Parameters**:

    Parameter | Type    | Description
    --------- | ------- | -----------
    `title`     | string  | Required notification title.
    `msg`       | string  | Required notification message.
    `sound`     | boolean | Optional parameter to enable a audible alert. Default is `False`.
    `level`     | string  | Optional parameter to specify the notification level.  Available options are: `info`, `warning`, `error`.  Default is `info`.


    **Example**

    ```python
    class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
        def run(self):
            sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": False})
    ```

## Tips and Tricks for Developers

Often when I use SubNotify with a plugin, I make its use optional.  Depending on the situation, you can have notifications fall back to either status bar notification or a Sublime Text dialog, but regardless of the fallback option, the approach is the same.

I usually start by first creating a dummy Notify object for when SubNotify is not available.  This way I can reference the same methods to check for availability regardless of whether SubNotify is installed or not.

```python
import sublime
try:
    from SubNotify.sub_notify import SubNotifyIsReadyCommand as Notify
except Exception:
    class Notify(object):
        """Notify fallback."""

        @classmethod
        def is_ready(cls):
            """Return false to effectively disable SubNotify."""

            return False
```

Then I create common notification methods that call either the SubNotify command (if enabled) or the fallback.  Notice that for the given plugin I check the users preference via that plugin's settings file and check if SubNotify is ready (in the case it is not installed, the dummy object will return `False`).

```python
def notify(msg):
    """Notify msg."""

    settings = sublime.load_settings("reg_replace.sublime-settings")
    if settings.get("use_sub_notify", False) and Notify.is_ready():
        sublime.run_command("sub_notify", {"title": "RegReplace", "msg": msg})
    else:
        sublime.status_message(msg)


def error(msg):
    """Error msg."""

    settings = sublime.load_settings("reg_replace.sublime-settings")
    if settings.get("use_sub_notify", False) and Notify.is_ready():
        sublime.run_command("sub_notify", {"title": "RegReplace", "msg": msg, "level": "error"})
    else:
        sublime.error_message("RegReplace:\n%s" % msg)
```

That's it.  There are a number of approaches you can take.  This is just one.


## Using Growl

To enable growl, first make sure Growl is installed on your system:

- Growl support for macOS: http://growl.info/.
- Growl support for Windows: http://www.growlforwindows.com/gfw/.
- Growl support for Linux: http://mattn.github.io/growl-for-linux/.

Next, in the settings file, enable the following setting:

```js
    // Attempt to enable growl if available
    "enable_growl": true,
```

## Windows Taskbar Notifications

No additional setup is needed.  Just make sure Growl is disabled in SubNotify via the settings file: `sub_notify.sublime-settings`.

```js
    // Attempt to enable growl if available
    "enable_growl": false,
```

## Ubuntu OSD

Ensure you have `notify-send` installed on your system.  It should be accessible via the command line.  Make sure Growl is disabled in SubNotify via the settings file: `sub_notify.sublime-settings`.

```js
    // Attempt to enable growl if available
    "enable_growl": false,
```

## Mac Notification Center

Ensure you have [terminal-notifier][terminal-notifier] installed.  The recommended way is to install via Ruby gem, but there are other ways; see the [repository][terminal-notifier] for more info.

You will have to update the terminal notifier path in the settings file as the internal default is set to the old ruby gem path for the version that was available at the time this documentation was written.  If you choose to install via another method, the path will also be different. The path should be defined as the absolute path to terminal-notifier.

```javascript
    // terminal-notifier path for Notification Center
    // Internal default when this is not defined is:
    // /Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier
    // This assumes installed with gem
     "terminal_notifier_path": "/Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier"
```

Make sure Growl is disabled in SubNotify via the settings file: `sub_notify.sublime-settings`.

```js
    // Attempt to enable growl if available
    "enable_growl": false,
```

--8<-- "refs.md"
