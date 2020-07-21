"""
SubNotify.

Copyright (c) 2013 - 2016 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import os
import sublime
import sublime_plugin
from .lib import notify

PLUGIN_SETTINGS = "sub_notify.sublime-settings"
SUB_NOTIFY_READY = False


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


def get_icon_files():
    """Get icon files."""

    settings = get_settings()
    png_name = 'SublimeText@2x.png' if settings.get('large_icons', True) else 'SublimeText.png'
    graphics = os.path.join(sublime.packages_path(), "SubNotify", "graphics")
    png_path = os.path.join(graphics, png_name)
    ico_path = os.path.join(graphics, "SublimeBubble.ico")

    return png_path, ico_path


def plugin_loaded():
    """Setup plugin."""

    global SUB_NOTIFY_READY

    # Create icon folder for systems that need a icon from path
    png_path, ico_path = get_icon_files()

    # Setup Notify
    notify.setup_notifications(
        "Sublime Text",
        png_path,
        ico_path,
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

    # Announce that SubNotify is ready
    SUB_NOTIFY_READY = True
    sublime.run_command("sub_notify_is_ready")

    if get_settings().get("debug", False):
        sublime.set_timeout(lambda: sublime.run_command("sub_notify_test"), 3000)


def plugin_unloaded():
    """Tear down plugin."""

    notify.destroy_notifications()
