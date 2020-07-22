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

When using in a plugin, it is recommended to make SubNotify usage optional. Also, it is recommended to make sound
optional as well.

Depending on the situation, you can have notifications fall back to either status bar notification or a Sublime Text
dialog, but regardless of the fallback option, the approach is the same.

You can start by first creating a dummy Notify object for when SubNotify is not available.  This way you can reference
the same methods to check for availability regardless of whether SubNotify is installed or not.

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

Then you can create common notification methods that call either the SubNotify command (if enabled) or the fallback.
Notice that for the given plugin, you can check the users preference via that plugin's settings file and check if
SubNotify is ready (in the case it is not installed, the dummy object will return `False`).

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

## Windows Taskbar Notifications

If you'd like to change the sound used, you can modify it via the following setting:

```js
    // Default sound. Must be a `.wav` file.
    "windows_audio": "C:/Windows/Media/notify.wav",
```

## Ubuntu OSD

Ensure you have `notify-send` installed on your system.  It should be accessible via the command line.

If you'd like to change/configure the sound used, you can modify it via the following settings:

```js
    // Default audio player. Must be paplay, aplay, or play.
    "linux_audio_player": "paplay",
    // Default sound. Accepted file types are dependant on the player:
    // - paplay: .wav, .mp3, or .ogg
    // - aplay: .wav or .mp3
    // - play:  .wav or .mp3
    "linux_audio": null,
```

By default, there is no audio file defined as distro audio could differ.

## Mac Notification Center

![Example macOS](docs/src/markdown/images/example-macos.png)

Ensure you have [terminal-notifier][terminal-notifier] installed.  The recommended way is via [HomeBrew](https://brew.sh/),
but there are other ways; see the [repository][terminal-notifier] for more info.

If necessary, you may have to update the terminal notifier path in the settings file if the internal default does not
match your own. If you choose to install via another method, the path may be different. The path should be defined as
the absolute path to terminal-notifier.

```javascript
    // terminal-notifier path for Notification Center
    // Internal default when this is not defined is:
    // /Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier
    // This assumes installed with gem
     "terminal_notifier_path": "/Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier"
```

If you'd like to change the sound used, you can modify it via the following setting:

```js
    // Default sound. Must be a .wav, .mp3, or .aiff file.
    "macos_audio": "/System/Library/Sounds/Glass.aiff",
```

--8<-- "refs.md"
