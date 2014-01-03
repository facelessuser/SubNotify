SubNotify
=========

Sublime Text notification plugin


# Features

- Growl support for OSX http://growl.info/
- Growl support for Windows http://www.growlforwindows.com/gfw/
- UNTESTED: Growl support for Linux http://mattn.github.io/growl-for-linux/

# Planned

- Native Windows

# Considering

- OSD for Ubuntu
- Notification Center OSX

# Usage

```python
class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command("sub_notify_info", {"title": "SubNotify", "msg": "Debug test popup!", "sound": False})
```

Sound only works on Ubuntu and Windows currently.  There is some issue with calling sound in the Sublime environment.  A workaround will probably be provided in the future.

# 3rd Party Libraries

- GNTP https://github.com/kfdm/gntp/
