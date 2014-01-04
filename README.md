SubNotify
=========

Sublime Text notification plugin (Windows|OSX|Linux)


# Features

- Growl support for OSX http://growl.info/
- Growl support for Windows http://www.growlforwindows.com/gfw/
- UNTESTED: Growl support for Linux http://mattn.github.io/growl-for-linux/
- Native windows taskbar bubble notifications
- OSX Notification Support via terminal-notifier

# Planned

- Native Windows

# Considering

- OSD for Ubuntu
- Notification Center OSX

# Usage

```python
class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": False})
```

Sound only works on Ubuntu and Windows currently.  There is some issue with calling sound in the Sublime environment.  A workaround will probably be provided in the future.

# Dependancies

- Growl support: SubNotify already includes gntp
- Windows Native Bubble Notifications: https://github.com/facelessuser/Pywin32

# Included 3rd Party Libraries

- gntp https://github.com/kfdm/gntp/
