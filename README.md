# Fire remote on Windows

An Amazon Fire TV remote does not work as a normal Windows keyboard. This project uses an Android phone that already understands the remote, then types those buttons into Windows.

The remote stays paired to the phone over Bluetooth. The phone and the PC talk over Wi-Fi with `adb`. While the tray icon is on, the phone ignores the remote and Windows gets the keys.

Windows only. You need a phone that can pair the remote.

## What you need

- Windows 10 or 11
- Python 3.11 or newer, from [python.org](https://www.python.org/downloads/). During setup, turn on **Add python.exe to PATH**. Skip the Microsoft Store alias if Windows offers one.
- An Android phone on the same Wi-Fi as the PC
- The Fire remote paired to that phone in Bluetooth settings
- [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) (`adb`)

A VPN that blocks the local network, such as GlobalProtect, will stop the PC from reaching the phone. Turn that off while you use the remote.

## Install

```bat
git clone https://github.com/Param2596/ar-remote.git
cd ar-remote
pip install -r requirements.txt
```

Unzip platform-tools so `adb.exe` is here:

```text
%LOCALAPPDATA%\Android\platform-tools\adb.exe
```

That is `C:\Users\<you>\AppData\Local\Android\platform-tools\adb.exe`. The script looks for `adb` at that path.

## First connection

On the phone:

1. Turn on Developer options.
2. Turn on **USB debugging**.
3. Turn on **Wireless debugging**.
4. Pair the Fire remote in Bluetooth settings and confirm the phone can navigate with it.

Plug the phone into the PC with a cable. If the phone asks, tap **Allow** and check **Always allow from this computer**.

Start the tray app:

```bat
pythonw ar_remote.py --tray
```

A round icon appears by the clock. Gray means off, green means on. Click it once. The first time, with the cable still plugged in, the script switches the phone to Wi-Fi debugging on port 5555. The phone may ask you to **Allow** again. After that, unplug the cable.

If nothing connects, run it in a window so you can read the error:

```bat
python ar_remote.py
```

`python ar_remote.py --list` prints the input devices the phone can see and exits. The remote usually shows up as `AR Keyboard`.

## Daily use

Leave these on whenever the tray icon is green:

- Phone Bluetooth, with the remote connected
- Wireless debugging
- Phone and PC on the same Wi-Fi

Click the tray icon to turn forwarding on or off. Off means the remote goes back to the phone.

Right-click the icon:

| Item | What it does |
| --- | --- |
| Use remote on this PC | Same as a left click. The check mark is on when forwarding is on. |
| Mode sound | Plays a short sound when Alexa changes mode. |
| Quit | Turns forwarding off and exits. |

After the phone reboots, turn Wireless debugging back on, then click the tray icon off and on.

`run.bat` starts the tray app with no console window. It expects Python at `%LOCALAPPDATA%\Python\pythoncore-3.14-64\pythonw.exe`. If your Python lives somewhere else, start it with `pythonw ar_remote.py --tray` or point a shortcut at your own `pythonw.exe`.

To start with Windows, put a shortcut in the Startup folder:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

Target your `pythonw.exe`, with arguments `"C:\path\to\ar-remote\ar_remote.py" --tray`. It comes up off, so the phone keeps the remote until you click the icon.

## Buttons

Alexa cycles three modes: **Controls**, **Volume**, **Cursor**. A label appears at the top of the screen. Holding a button keeps that key down. It does not trigger a separate long-press action. The remote's power, sleep, and mic buttons are ignored. The mic audio never leaves the remote.

### Controls

| Remote | Windows |
| --- | --- |
| Up, Down, Left, Right | Arrow keys |
| Center | Enter |
| Back | Escape |
| Home | Windows key |
| Menu | Menu key |
| Play / Pause | Play / Pause |
| Rewind, Fast forward | Previous track, Next track |
| App shortcut (three lines) | Task View (Win+Tab) |
| Alexa | Next mode |

### Volume

| Remote | Windows |
| --- | --- |
| Up, Down | Volume up, Volume down |
| Left, Right | Previous track, Next track |
| Center | Mute |
| Alexa | Next mode |

Back, Home, Menu, and Play / Pause still do what they do in Controls.

### Cursor

| Remote | Windows |
| --- | --- |
| Up, Down, Left, Right | Move the pointer. Holding a direction speeds it up. |
| Center | Left click. Hold it to drag. |
| Menu | Right click |
| Alexa | Next mode |

## Files that stay on your PC

These are created locally and are not in the repo:

| File | What it stores |
| --- | --- |
| `endpoint.txt` | The phone's `ip:port` after the first connection |
| `sound.txt` | Whether the mode sound is on |

## When it stops working

- **No phone found.** Wireless debugging is off, the phone is on another network, or a VPN is blocking LAN traffic. Plug in the cable once and click the tray icon again.
- **Not authorized.** Unlock the phone and tap Allow.
- **The remote still drives the phone.** The tray icon is off, or the grabber on the phone is not running. Turn the icon off and on.
- **Buttons do nothing on the PC.** Bluetooth dropped. Reconnect the remote to the phone, then toggle the tray icon.
- **Several command windows open.** Start with `pythonw`, not `python`. `pythonw` has no console, and the script hides `adb`'s windows.

## Rebuild the phone helper

`grabevent` is a small arm64 program already included in the repo. It holds the remote so Android does not act on the buttons. You only rebuild it if you change that program:

```bat
pip install keystone-engine
python build_grabevent.py
```

## Sound

The mode chime is `bong_001` from [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds). Thanks to Kenney for making that pack and letting people use it.
