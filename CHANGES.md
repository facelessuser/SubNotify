## SubNotify

## 1.6.0

-   **NEW**: Changes to support Python 3.13 on ST 4201+.

## 1.5.2

-   **FIX**: Default to homebrew path for `terminal-notifier`.
-   **FIX**: Include `typing` dependency for Python 3.3.

## 1.5.1

-   **FIX**: Fix Linux audio not playing.
-   **FIX**: Notification setup not reloading on settings change.

## 1.5.0

-   **NEW**: Drop Growl support.
-   **NEW**: No longer requires the `gntp` dependency.
-   **NEW**: Allow configuring of default sound and audio player for Linux sound.
-   **NEW**: Ensure all messages use Sublime Text's icon.
-   **NEW**: Rework notification handling on Windows.
-   **NEW**: Change default location for the `terminal-notifier` option.

## 1.4.4

-   **FIX**: Cleanup on reload and delete task icon on notify.

## 1.4.3

-   **FIX**: Update dependencies.

## 1.4.2

-   **FIX**: Use official ST icon for messages in Linux and Growl.
-   **FIX**: Fix blocking issue with `terminal-notifier`.

## 1.4.1

-   **NEW**: Provide workaround for terminal-notifier not physically showing a popup even though notification center
sees the notification.

## 1.4.0

-   **NEW**: Restrict phantoms to 3124+.

## 1.3.0

-   **NEW**: Move gntp to external dependecy (#5).
-   **NEW**: Add support commands such as changelog etc.
