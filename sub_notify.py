"""
SubNotify.

Copyright (c) 2013 - 2016 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import os
import sublime
import sublime_plugin
from .lib import notify
from .lib.notify.util import which

LINUX_PLAYERS = ["paplay", "aplay", "play"]
NOTIFY_EXT = {
    "afplay": ['.wav', '.mp3', '.aiff'],
    "windows": ['.wav'],
    "paplay": ['.wav', '.mp3', '.ogg'],
    "aplay": ['.wav', '.mp3'],
    "play": ['.wav', '.mp3'],
}
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

    global SUB_NOTIFY_READY

    SUB_NOTIFY_READY = False

    notify.destroy_notifications()

    # Create icon folder for systems that need a icon from path
    png, icon, icns = get_icon_files()

    if notify._PLATFORM == "windows":
        img = icon
    elif notify._PLATFORM == "macos":
        img = icns
    else:
        img = png

    player, audio = get_sound_settings()

    # Set up notifications
    notifier = get_settings().get(
        "terminal_notifier_path",
        "/usr/local/bin/terminal-notifier"
    )
    if (
        os.path.isdir(notifier) and
        notifier.endswith('.app') and
        os.path.exists(os.path.join(notifier, 'Contents/MacOS/terminal-notifier'))
    ):
        notifier = os.path.join(notifier, 'Contents/MacOS/terminal-notifier')

    notify.setup_notifications(
        "Sublime Text (SubNotify)",
        img,
        term_notify=notifier,
        sender=None,
        sound=audio,
        sound_player=player
    )

    # Announce that SubNotify is ready
    SUB_NOTIFY_READY = True
    sublime.run_command("sub_notify_is_ready")

    settings = get_settings()

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
    png = os.path.join(graphics, png_name)
    icon = os.path.join(graphics, "SublimeText.ico")
    icns = None
    if notify._PLATFORM == "macos":
        icns = os.path.join(
            os.path.dirname(sublime.executable_path()), "..", "Resources", "Sublime Text.icns"
        )
        if not os.path.exists(icns):
            icns = None

    if not os.path.exists(png):
        png = None

    if not os.path.exists(icon):
        icon = None

    return png, icon, icns


def get_sound_settings():
    """Get sound settings."""

    if notify._PLATFORM == "windows":
        player = 'windows'
        audio = get_settings().get('windows_audio', 'C:/Windows/Media/notify.wav')
        if not audio or not os.path.exists(audio) or os.path.splitext(audio)[1].lower() not in NOTIFY_EXT[player]:
            audio = None
    elif notify._PLATFORM == "macos":
        player = 'afplay'
        audio = get_settings().get('macos_audio', '/System/Library/Sounds/Glass.aiff')
        if not audio or not os.path.exists(audio) or os.path.splitext(audio)[1].lower() not in NOTIFY_EXT[player]:
            audio = None
    else:
        player = get_settings().get('linux_audio_player', 'paplay')
        if not player or not which(player) or player not in LINUX_PLAYERS:
            player = None
        player_key = os.path.basename(player) if player else None
        audio = get_settings().get('linux_audio', None)
        if (
            not player_key or
            not audio or
            not os.path.exists(audio) or
            os.path.splitext(audio)[1].lower() not in NOTIFY_EXT[player_key]
        ):
            audio = None
    return player, audio


def plugin_loaded():
    """Setup plugin."""

    # Try to enable notification systems
    enable_notifications()

    if get_settings().get("debug", False):
        sublime.set_timeout(lambda: sublime.run_command("sub_notify_test"), 3000)


def plugin_unloaded():
    """Tear down plugin."""

    global SUB_NOTIFY_READY
    SUB_NOTIFY_READY = False
    notify.destroy_notifications()
