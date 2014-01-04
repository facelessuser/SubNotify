import sys
from os.path import join, exists
from os import makedirs
import sublime
import sublime_plugin
try:
    from Pywin32.setup import win32setup
except:
    win32setup = lambda: log("Pywin32 not installed")

notify = None
PLUGIN_SETTINGS = "sub_notify.sublime-settings"
SUB_NOTIFY_READY = False


######################
# Settings
######################
def get_settings():
    return sublime.load_settings(PLUGIN_SETTINGS)


######################
# Logging
######################
def log(msg, status=False):
    string = str(msg)
    print("SubNotify: %s" % string)
    if status:
        sublime.status_message(string)


def debug_log(s):
    if get_settings().get("debug", False):
        log(s)


######################
# Commands
######################
class SubNotifyCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg="", sound=False, level="info"):
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
    def run(self):
        sublime.run_command("sub_notify", {"title": "SubNotify", "msg": "Debug test popup!", "sound": True})


class SubNotifyIsReadyCommand(sublime_plugin.ApplicationCommand):
    @classmethod
    def is_ready(cls):
        return SUB_NOTIFY_READY

    def run(self):
        ready = SubNotifyIsReadyCommand.is_ready()
        if ready:
            log("Ready for messages!")


######################
# Setup
######################
def load_notify():
    global notify
    try:
        import gntp
    except ImportError:
        sys.path.insert(0, join(sublime.packages_path(), "SubNotify", "modules"))

    win32setup()

    from SubNotify.lib import notify


def enable_notifications():
    settings = get_settings()

    notify.enable_growl(settings.get("enable_growl", False))

    # Setup reload
    settings.clear_on_change('reload')
    settings.add_on_change('reload', enable_notifications)


def plugin_loaded():
    global SUB_NOTIFY_READY

    # Ensure gntp can be found if not already in the path
    load_notify()

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
