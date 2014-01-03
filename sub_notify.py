import sys
from os.path import join, exists
from os import makedirs
import sublime
import sublime_plugin
import SubNotify.icons as icons

notify = None
PLUGIN_SETTINGS = "sub_notify.sublime-settings"
SUB_NOTIFY_READY = False


######################
# Logging
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
class SubNotifyInfoCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg="", sound=False):
        notify.info(title, msg, sound)


class SubNotifyWarningCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg="", sound=False):
        notify.warning(title, msg, sound)


class SubNotifyErrorCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg="", sound=False):
        notify.error(title, msg, sound)


class SubNotifyTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command("sub_notify_info", {"title": "SubNotify", "msg": "Debug test popup!"})


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
        __import__("gntp")
    except ImportError:
        sys.path.insert(0, join(sublime.packages_path(), "SubNotify", "modules"))
    from SubNotify.lib import notify


def plugin_loaded():
    global SUB_NOTIFY_READY

    # Ensure gntp can be found if not already in the path
    load_notify()

    # # Create icon folder for systems that need a icon from path
    # user = join(sublime.packages_path(), "User", "SubNotify")
    # if not exists(user):
    #     makedirs(user)

    # Setup Notify
    notify.setup_notifications("Sublime Text", icons.notify_png.GetData())

    # Try to enable notification systems
    notify.enable_growl(get_settings().get("enable_growl", False))

    # Annouce that subnotify is ready
    SUB_NOTIFY_READY = True
    sublime.run_command("sub_notify_is_ready")

    if get_settings().get("debug", False):
        sublime.set_timeout(lambda: sublime.run_command("sub_notify_test"), 3000)
