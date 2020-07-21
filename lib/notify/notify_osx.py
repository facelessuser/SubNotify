"""
Notify OSX.

Copyright (c) 2013 - 2016 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
from __future__ import unicode_literals
import subprocess
import traceback
from os.path import exists
import sys

__all__ = ("get_notify", "alert", "setup", "destroy")

PY3 = (3, 0) <= sys.version_info < (4, 0)

if PY3:
    binary_type = bytes  # noqa
else:
    binary_type = str


class Options(object):
    """Notification options."""

    notify = None
    sender = "com.apple.Terminal"
    terminal_notifier = None
    app_name = ""

    @classmethod
    def clear(cls):
        """Clear."""

        cls.notify = None
        cls.sender = "com.apple.Terminal"
        cls.terminal_notifier = None
        cls.app_name = ""
        cls.icon = None


def alert(sound=None):
    """Play an alert sound for the OS."""

    # `ObjC` wrapper works fine outside of sublime, but not in
    # Resort to afplay as workaround
    subprocess.call(["afplay", "/System/Library/Sounds/Glass.aiff"])


@staticmethod
def notify_osx_fallback(title, message, sound, fallback):
    """OSX notifications fallback (just sound)."""

    # Fallback to `wxpython` notification
    fallback(title, message, sound)


@staticmethod
def notify_osx_call(title, message, sound, fallback):
    """OSX notifications."""

    try:
        assert(Options.terminal_notifier is not None and exists(Options.terminal_notifier))
        # Show Notification here
        params = [Options.terminal_notifier, "-title", Options.app_name, "-timeout", "5"]
        if message is not None:
            params += ["-message", message]
        if title is not None:
            params += ["-subtitle", title]
        if Options.sender is not None:
            params += ["-sender", Options.sender]
        if sound:
            params += ["-sound", "Glass"]
        subprocess.Popen(params)

        # if sound:
        #     # Play sound if desired
        #     alert()
    except Exception:
        print(traceback.format_exc())
        # Fallback notification
        fallback(title, message, sound)


def setup(app_name, icon, *args):
    """Setup."""

    term_notify = None
    sender = None

    if len(args) and len(args[0]) == 2:
        term_notify = args[0][0]
        sender = args[0][1]

        if term_notify is not None and isinstance(term_notify, binary_type):
            term_notify = term_notify.decode('utf-8')

        if sender is not None and isinstance(sender, binary_type):
            sender = sender.decode('utf-8')

    Options.app_name = app_name

    try:
        assert(icon is not None and exists(icon))
        Options.icon = icon
    except Exception:
        pass

    try:
        assert(term_notify is not None and exists(term_notify))
        Options.terminal_notifier = term_notify
        if sender is not None:
            Options.sender = sender
        Options.notify = notify_osx_call
    except Exception:
        print(traceback.format_exc())


def destroy():
    """Destroy."""

    Options.clear()
    Options.notify = notify_osx_fallback


def get_notify():
    """Get notification."""

    return Options.notify


Options.notify = notify_osx_fallback
