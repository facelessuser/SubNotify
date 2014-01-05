"""
Notify

Licensed under MIT
Copyright (c) 2013 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import subprocess
from os.path import exists, join
import traceback

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"

if _PLATFORM == "windows":
    import winsound


###################################
# Platform Specific Audio Alert
###################################
if _PLATFORM == "osx":
    from ctypes import *
    import ctypes.util as util

    appkit = cdll.LoadLibrary(util.find_library('AppKit'))
    cf = cdll.LoadLibrary(util.find_library('CoreFoundation'))
    objc = cdll.LoadLibrary(util.find_library('objc'))

    kCFStringEncodingUTF8 = 0x08000100

    cf.CFStringCreateWithCString.restype = c_void_p
    cf.CFStringCreateWithCString.argtypes = [c_void_p, c_char_p, c_uint32]

    objc.objc_getClass.restype = c_void_p
    objc.sel_registerName.restype = c_void_p
    objc.objc_msgSend.restype = c_void_p
    objc.objc_msgSend.argtypes = [c_void_p, c_void_p]

    NSSound = c_void_p(objc.objc_getClass('NSSound'))
    NSAutoreleasePool = c_void_p(objc.objc_getClass('NSAutoreleasePool'))


def _nsstring(string):
    """
    Return an NSString object
    """

    return c_void_p(cf.CFStringCreateWithCString(None, string.encode('utf8'), kCFStringEncodingUTF8))


def _callmethod(obj, method, *args, **kwargs):
    """
    ObjC method call
    """

    cast_return = kwargs.get("cast_return", c_void_p)
    return cast_return(objc.objc_msgSend(obj, objc.sel_registerName(method), *args))


def play_alert(sound=None):
    """
    Play an alert sound for the OS
    """

    if _PLATFORM == "osx":
        pool = _callmethod(_callmethod(NSAutoreleasePool, "alloc"), "init")
        snd = _nsstring(sound if sound is not None else "Glass")
        soundobj = _callmethod(NSSound, "soundNamed:", snd)
        _callmethod(soundobj, "play")
        _callmethod(pool, "drain")
        del pool
    elif _PLATFORM == "windows":
        snd = sound if sound is not None else "*"
        winsound.PlaySound(snd, winsound.SND_ALIAS)
    else:
        if exists('/usr/share/sounds/gnome/default/alerts/glass.ogg'):
            subprocess.call(['/usr/bin/canberra-gtk-play', '-f', '/usr/share/sounds/gnome/default/alerts/glass.ogg'])
        else:
            subprocess.call(['/usr/bin/canberra-gtk-play', '--id', 'bell'])


###################################
# OSX Notify
###################################
NOTIFY_OSX = None
NOTIFY_OSX_SENDER = "com.apple.Terminal"
NOTIFY_OSX_TERM = None


def notify_osx_fallback(title, message, sound, fallback):
    """
    OSX notifications fallback (just sound)
    """

    # Fallback to wxpython notification
    fallback(title, message, sound)


NOTIFY_OSX = notify_osx_fallback

if _PLATFORM == "osx":
    try:
        def notify_osx_call(title, message, sound, fallback):
            """
            OSX notifications
            """

            try:
                assert(NOTIFY_OSX_TERM is not None and exists(NOTIFY_OSX_TERM))
                # Show Notification here
                params = [NOTIFY_OSX_TERM, "-title", NOTIFY_OSX_TITLE]
                if message is not None:
                    params += ["-message", message]
                if title is not None:
                    params += ["-subtitle", title]
                if NOTIFY_OSX_SENDER is not None:
                    params += ["-sender", NOTIFY_OSX_SENDER]
                    params += ["-activate", NOTIFY_OSX_SENDER]
                subprocess.call(params)

                if sound:
                    # Play sound if desired
                    play_alert()
            except:
                print(traceback.format_exc())
                # Fallback to wxpython notification
                fallback(title, message, sound)
    except:
        print(traceback.format_exc())
        notify_osx_call = None
        print("no terminal-notifier")
else:
    notify_osx_call = None
    print("no terminal-notifier")


def setup_notify_osx(app_name, term_notifier, sender):
    """
    Setup Notify OSX
    """

    global NOTIFY_OSX_SENDER
    global NOTIFY_OSX_TERM
    global NOTIFY_OSX_TITLE
    global notify_osx_call
    global NOTIFY_OSX
    NOTIFY_OSX_TITLE = app_name

    if notify_osx_call is not None:
        try:
            assert(term_notifier is not None and exists(term_notifier))
            NOTIFY_OSX_TERM = term_notifier
            if sender is not None:
                NOTIFY_OSX_SENDER = sender
        except:
            print(traceback.format_exc())
            notify_osx_call = None
    if notify_osx_call is not None:
        NOTIFY_OSX = notify_osx_call


###################################
# Ubuntu Notify OSD
###################################
NOTIFY_OSD_ICON = None
NOTIFY_OSD = None


def notify_osd_fallback(title, message, sound, fallback):
    """
    Ubuntu Notify OSD notifications fallback (just sound)
    """

    # Fallback to wxpython notification
    fallback(title, message, sound)


NOTIFY_OSD = notify_osd_fallback

if _PLATFORM == "linux":
    try:
        assert(subprocess.call(["notify-send", "--version"]) == 0)

        def notify_osd_call(title, message, sound, fallback):
            """
            Ubuntu Notify OSD notifications
            """

            try:
                params = ["notify-send", "-a", NOTIFY_OSD_APP, "-t", "3000"]
                if NOTIFY_OSD_ICON is not None:
                    params += ["-i", NOTIFY_OSD_ICON]
                if message is not None:
                    params += [title, message]
                subprocess.call(params)

                if sound:
                    # Play sound if desired
                    play_alert()
            except:
                # Fallback to wxpython notification
                fallback(title, message, sound)

    except:
        notify_osd_call = None
        print("no notify osd")
else:
    notify_osd_call = None
    print("no notify osd")


def setup_notify_osd(app_name):
    """
    Setup Notify OSD
    """

    global NOTIFY_OSD
    global NOTIFY_OSD_APP
    global notify_osd_call
    if notify_osd_call is not None:
        NOTIFY_OSD_APP = app_name
        NOTIFY_OSD = notify_osd_call


###################################
# Growl Support
###################################
GROWL_ICON = None
GROWL_ENABLED = False
GROWL = None
NOTIFY_GROWL = None


def notify_growl_fallback(note_type, title, description, sound, fallback):
        """
        Growl failed to register so create a growl notify that simply
        calls the fallback
        """

        fallback(title, description, sound)

NOTIFY_GROWL = notify_growl_fallback


try:
    import gntp.notifier

    def notify_growl_call(note_type, title, description, sound, fallback):
        """
        Send growl notification
        """

        try:
            GROWL.notify(
                noteType=note_type,
                title=title,
                description=description,
                icon=GROWL_ICON,
                sticky=False,
                priority=1
            )

            if sound:
                # Play sound if desired
                play_alert()
        except:
            # Fallback to wxpython notification
            fallback(title, description, sound)
except Exception as e:
    print(traceback.format_exc())
    notify_growl_call = None
    print("no growl")


def setup_notify_growl(app_name):
    """
    Setup growl
    """

    global GROWL
    global NOTIFY_GROWL
    global notify_growl_call
    try:
        # Init growl object
        GROWL = gntp.notifier.GrowlNotifier(
            applicationName=app_name,
            notifications=["Info", "Warning", "Error"],
            defaultNotifications=["Info", "Warning", "Error"]
        )

        GROWL.register()
    except:
        GROWL = None

    if GROWL is not None:
        NOTIFY_GROWL = notify_growl_call


def enable_growl(enable):
    """
    Enable/Disable growl
    """

    global GROWL_ENABLED
    GROWL_ENABLED = enable and has_growl()


def has_growl():
    """
    Return if growl is available
    """

    return GROWL is not None


###################################
# Windows Native Notifications
###################################
NOTIFY_WIN_ICON = None
NOTIFY_WIN = None


class WinNotifyLevel(object):
    ICON_INFORMATION = 0x01
    ICON_WARNING = 0x02
    ICON_ERROR = 0x04


def notify_win_fallback(title, message, sound, icon, fallback):
    """
    Notify win calls the fallback
    """

    fallback(title, message, sound)


NOTIFY_WIN = notify_win_fallback

if _PLATFORM == "windows":
    try:
        from win32api import *
        from win32gui import *
        import win32con

        class NotifyWin(object):
            atom_name = None
            window_handle = None

            def __init__(self, app_name, icon, tooltip=None):
                """
                Create the taskbar for the application and register it.
                Show nothing by default until called.
                """

                message_map = {
                    win32con.WM_DESTROY: self.OnDestroy,
                    win32con.WM_USER + 20: self.OnTaskbarNotify,
                }

                self.tooltip = tooltip
                self.visible = False

                # Register window class
                wc = WNDCLASS()
                self.hinst = wc.hInstance = GetModuleHandle(None)
                wc.lpszClassName = app_name
                wc.lpfnWndProc = message_map  # could also specify a wndproc.
                if NotifyWin.atom_name is not None:
                    self._destroy_window()
                    UnregisterClass(NotifyWin.atom_name, None)
                    NotifyWin.atom_name = None
                self.class_atom = RegisterClass(wc)
                NotifyWin.atom_name = self.class_atom

                self._create_window()

                self.hicon = self.get_icon(icon)

            def get_icon(self, icon):
                """
                Try to load the given icon from the path given,
                else default to generic application icon from the OS.
                """

                icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
                try:
                    hicon = LoadImage(
                        self.hinst, icon,
                        win32con.IMAGE_ICON,
                        0, 0, icon_flags
                    )
                except:
                    hicon = LoadIcon(0, win32con.IDI_APPLICATION)

                return hicon

            def show_notification(self, title, msg, sound, icon, fallback):
                """
                Attemp to show notifications.  Provide fallback for consistency
                with other notifyicatin methods.
                """

                try:
                    self._show_notification(title, msg, sound, icon)
                except:
                    print(traceback.format_exc())
                    fallback(title, msg, sound)

            def _create_window(self):
                # Create the Window.
                style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
                self.hwnd = CreateWindow(
                    self.class_atom, "Taskbar", style,
                    0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                    0, 0, self.hinst, None
                )
                NotifyWin.window_handle = self.hwnd
                UpdateWindow(self.hwnd)

            def _destroy_window(self):
                if NotifyWin.window_handle:
                    DestroyWindow(NotifyWin.window_handle)
                    NotifyWin.window_handle = None
                    self.hwnd = None

            def _show_notification(self, title, msg, sound, icon):
                """
                Call windows API to show notification
                """

                icon_level = 0
                if icon & WinNotifyLevel.ICON_INFORMATION:
                    icon_level |= NIIF_INFO
                elif icon & WinNotifyLevel.ICON_WARNING:
                    icon_level |= NIIF_WARNING
                elif icon & WinNotifyLevel.ICON_ERROR:
                    icon_level |= NIIF_ERROR
                self.show_icon()
                Shell_NotifyIcon(
                    NIM_MODIFY,
                    (
                        self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20,
                        self.hicon, "Balloon tooltip", msg, 200, title,
                        icon_level
                    )
                )

                if sound:
                    play_alert()

            def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
                """
                When recieving the dismiss code for the notification,
                hide the icon.
                """

                if lparam == 1028:
                    self.hide_icon()
                    # Noification dismissed

            def show_icon(self):
                """
                Display the taskbar icon
                """

                flags = NIF_ICON | NIF_MESSAGE
                if self.tooltip is not None:
                    flags |= NIF_TIP
                    nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, self.hicon, self.tooltip)
                else:
                    nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, self.hicon)
                if self.visible:
                    self.hide_icon()
                Shell_NotifyIcon(NIM_ADD, nid)
                self.visible = True

            def hide_icon(self):
                """
                Hide icon
                """

                if self.visible:
                    nid = (self.hwnd, 0)
                    Shell_NotifyIcon(NIM_DELETE, nid)
                self.visible = False

            def OnDestroy(self, hwnd, msg, wparam, lparam):
                """
                Remove icon and notification
                """

                self.hide_icon()
                PostQuitMessage(0)

    except:
        print(traceback.format_exc())
        NotifyWin = None
        print("no win notify")
else:
    NotifyWin = None
    print("no win notify")


def setup_noitfy_win(app_name, icon):
    """
    Setup win notify
    """

    global NOTIFY_WIN

    if NotifyWin is not None:
        NOTIFY_WIN = NotifyWin(app_name + "Taskbar", icon, app_name).show_notification


###################################
# Fallback Native Notifications
###################################
class NotifyFallback(object):
    def __init__(self, *args, **kwargs):
        """
        Init class
        """

        self.sound = kwargs.get("sound", False)

    def Show(self):
        """
        Fallback just plays an alert
        """

        if self.sound:
            play_alert()

Notify = NotifyFallback


###################################
# Setup Notifications
###################################
def set_app_icon(app_name, png=None, icon=None):
    """
    Set app icon for growl
    """

    global GROWL_ICON
    global NOTIFY_OSD_ICON
    global NOTIFY_WIN_ICON

    GROWL_ICON = None
    NOTIFY_WIN_ICON = None
    NOTIFY_OSD_ICON = None

    try:
        assert(png is not None and exists(png))
        NOTIFY_OSD_ICON = png
        with open(png, "rb") as f:
            GROWL_ICON = f.read()
    except:
        pass

    try:
        assert(icon is not None and exists(icon))
        NOTIFY_WIN_ICON = icon
    except:
        pass


def setup_notifications(app_name, png=None, icon=None, term_notify=(None, None)):
    """
    Setup notifications for all platforms
    """

    set_app_icon(app_name, png, icon)
    setup_notify_growl(app_name)
    setup_notify_osd(app_name)
    setup_notify_osx(app_name, term_notify[0], term_notify[1])
    setup_noitfy_win(app_name, NOTIFY_WIN_ICON)


###################################
# Notification Calls
###################################
def info(title, message="", sound=False):
    """
    Info notification
    """

    default_notify = lambda title, message, sound: Notify(title, message, sound=sound).Show()
    if has_growl() and GROWL_ENABLED:
        NOTIFY_GROWL("Info", title, message, sound, default_notify)
    elif _PLATFORM == "osx":
        NOTIFY_OSX(title, message, sound, default_notify)
    elif _PLATFORM == "linux":
        NOTIFY_OSD(title, message, sound, default_notify)
    elif _PLATFORM == "windows":
        NOTIFY_WIN(title, message, sound, WinNotifyLevel.ICON_INFORMATION, default_notify)
    else:
        default_notify(title, message, sound)


def error(title, message, sound=False):
    """
    Error notification
    """

    default_notify = lambda title, message, sound: Notify(title, message, sound=sound).Show()
    if has_growl() and GROWL_ENABLED:
        NOTIFY_GROWL("Error", title, message, sound, default_notify)
    elif _PLATFORM == "osx":
        NOTIFY_OSX(title, message, sound, default_notify)
    elif _PLATFORM == "linux":
        NOTIFY_OSD(title, message, sound, default_notify)
    elif _PLATFORM == "windows":
        NOTIFY_WIN(title, message, sound, WinNotifyLevel.ICON_ERROR, default_notify)
    else:
        default_notify(title, message, sound)


def warning(title, message, sound=False):
    """
    Warning notification
    """

    default_notify = lambda title, message, sound: Notify(title, message, sound=sound).Show()
    if has_growl() and GROWL_ENABLED:
        NOTIFY_GROWL("Warning", title, message, sound, default_notify)
    elif _PLATFORM == "osx":
        NOTIFY_OSX(title, message, sound, default_notify)
    elif _PLATFORM == "linux":
        NOTIFY_OSD(title, message, sound, default_notify)
    elif _PLATFORM == "windows":
        NOTIFY_WIN(title, message, sound, WinNotifyLevel.ICON_WARNING, default_notify)
    else:
        default_notify(title, message, sound)
