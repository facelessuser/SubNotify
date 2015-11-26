"""
SubNotify.

Copyright (c) 2013 - 2015 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import sys
from os.path import join, dirname
import sublime
import sublime_plugin

PLUGIN_SETTINGS = "sub_notify.sublime-settings"
SUB_NOTIFY_READY = False

######################
# Special Imports
######################
# Ensure pywin32 is found in path
try:
    import Pywin32.setup  # noqa
except Exception:
    print("SubNotify: Pywin32 not installed")

# Ensure gntp is found in path
PACKAGE_PATH = dirname(__file__)
GNTP_PATH = join(PACKAGE_PATH, "modules")
if GNTP_PATH not in sys.path:
    sys.path.append(GNTP_PATH)

from SubNotify.lib import notify


######################
# Settings
######################
def get_settings():
    """Get plugin settings."""

    return sublime.load_settings(PLUGIN_SETTINGS)


######################
# Logging
######################
def log(msg, status=False):
    """Log messages."""

    string = str(msg)
    print("SubNotify: %s" % string)
    if status:
        sublime.status_message(string)


def debug_log(s):
    """Debug log messages."""

    if get_settings().get("debug", False):
        log(s)


######################
# Commands
######################
class SubNotifyCommand(sublime_plugin.ApplicationCommand):
    """SubNotify message command."""

    def run(self, title, msg, sound=False, level="info"):
        """Run the command."""

        if SubNotifyIsReadyCommand.is_ready():
            if level == "error":
                notify.error(title, msg, sound)
            elif level == "warning":
                notify.warning(title, msg, sound)
            else:
                notify.info(title, msg, sound)
        else:
            log("Not ready for messages yet!")


class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
    """SubNotify test command."""

    def run(self):
        """Run the command."""

        sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": True})


class SubNotifyIsReadyCommand(sublime_plugin.ApplicationCommand):
    """Command to check if command is ready."""

    @classmethod
    def is_ready(cls):
        """Check if the command is ready."""

        return SUB_NOTIFY_READY

    def run(self):
        """Run the command."""

        ready = SubNotifyIsReadyCommand.is_ready()
        if ready:
            log("Ready for messages!")


######################
# Setup
######################
def enable_notifications(notice=False):
    """Enable notifications."""

    settings = get_settings()
    notify.enable_growl(settings.get("enable_growl", False))

    # Setup reload
    settings.clear_on_change('reload')
    settings.add_on_change('reload', lambda: enable_notifications(True))

    # Show notice of reload and show message to confirm change took place
    if notice:
        sublime.run_command(
            "sub_notify",
            {
                "title": "SubNotify",
                "msg": "Settings reloaded."
            }
        )


def plugin_loaded():
    """Setup plugin."""

    global SUB_NOTIFY_READY

    # Create icon folder for systems that need a icon from path
    graphics = join(sublime.packages_path(), "SubNotify", "graphics")

    # Setup Notify
    notify.setup_notifications(
        "Sublime Text",
        join(graphics, "SublimeBubble.png"),
        join(graphics, "SublimeBubble.ico"),
        (
            get_settings().get(
                "terminal_notifier_path",
                "/Library/Ruby/Gems/2.0.0/gems/terminal-notifier-1.5.1/bin/terminal-notifier"
            ),
            "com.sublimetext.3"
        )
    )

    # Try to enable notification systems
    enable_notifications()

    # Annouce that subnotify is ready
    SUB_NOTIFY_READY = True
    sublime.run_command("sub_notify_is_ready")

    if get_settings().get("debug", False):
        sublime.set_timeout(lambda: sublime.run_command("sub_notify_test"), 3000)


def plugin_unloaded():
    """Tear down plugin."""

    notify.destroy_notifications()
