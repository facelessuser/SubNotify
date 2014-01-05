SubNotify
=========

Sublime Text notification plugin (Windows|OSX|Linux)


# Features

- Growl support for OSX http://growl.info/
- Growl support for Windows http://www.growlforwindows.com/gfw/
- Growl support for Linux http://mattn.github.io/growl-for-linux/
- Native windows taskbar bubble notifications (requires Pywin32 - https://github.com/facelessuser/Pywin32)
- OSX Notification Support via `terminal-notifier` https://github.com/alloy/terminal-notifier
- Ubuntu OSD support via `notify-send`


# Usage

```python
class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": False})
```

Sound only works on Ubuntu and Windows currently.  There is some issue with calling sound for OSX in the Sublime environment.  A workaround will probably be provided in the future.

# Growl
By default SubNotify will try and use:

- Windows: Native taskbar notifications
- OSX: Notification Center via terminal-notifier (if the correct path is provided)
- Linux (Ubuntu): OSD via `notify-send`

To enable growl, in the settings file enable the following setting:

```javascript
    // Attempt to enable growl if available
    "enable_growl": false,
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


# Included 3rd Party Libraries

- gntp https://github.com/kfdm/gntp/
