# User Guide {: .doctitle}
Configuration and usage of SubNotify.
{: .doctitle-info}

---

# Using Subnotify in a Plugin

sub_notify
: 
    Command that displays the notification for Sublime Text.

    **Parameters**:

    | Parameter | Type | Description |
    |-----------|------|-------------|
    | title | string | Required notification title. |
    | msg | string | Required notification message. |
    | sound | bool | Optional parameter to enable a audible alert. Default is `False`. |
    | level | string | Optional parameter to specify the notification level.  Available options are: `info`, `warning`, `error`.  Default is `info`. |


    # Example
    ```python
    class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
        def run(self):
            sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": False})
    ```

# Using Growl
By default SubNotify will try and use:

- Windows: Native taskbar notifications.
- OSX: Notification Center via terminal-notifier (if the correct path is provided).
- Linux (Ubuntu): OSD via `notify-send`.

To enable growl, first make sure Growl is installed on your system:

- Growl support for OSX: http://growl.info/.
- Growl support for Windows: http://www.growlforwindows.com/gfw/.
- Growl support for Linux: http://mattn.github.io/growl-for-linux/.

Next, in the settings file, enable the following setting:

```javascript
    // Attempt to enable growl if available
    "enable_growl": true,
```

# Windows Taskbar Notifications
Install Pywin32: https://github.com/facelessuser/Pywin32.  Make sure Growl is disabled in SubNotify.

# Ubuntu OSD
Ensure you have `notify-send` installed on your system.  It should be accessible via the command line.  Make sure Growl is disabled in SubNotify.

# OSX Notification Center
Ensure you have terminal-notifier installed https://github.com/alloy/terminal-notifier.  The recommended way is to install via Ruby gem.  See the repo for more info.  If the path differs from the default in listed in the settings file, define the absolute path to terminal-notifier:

```javascript
    // terminal-notifier path for Notification Center
    // Internal default when this is not defined is:
    // /Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier
    // This assumes installed with gem
     "terminal_notifier_path": "/Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier"
```
