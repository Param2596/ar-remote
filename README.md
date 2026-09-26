# Fire remote on Windows

An Amazon Fire TV remote does not work as a normal Windows keyboard. This project uses an Android phone that already understands the remote, then types those buttons into Windows.

The remote stays paired to the phone over Bluetooth. The phone and the PC talk over Wi-Fi with `adb`. While the tray icon is on, the phone ignores the remote and Windows gets the keys.

Windows only. You need a phone that can pair the remote.

## Do not use public Wi-Fi

**Do this only on a private network you trust, such as your home Wi-Fi.** A cafe, hotel, airport, school, or guest network is not safe.

Wireless debugging is not a harmless switch. While it is on, a computer on that network can run commands on the phone: install and remove apps, read files, and control the screen. This project uses that channel to read the remote. Anyone else who pairs with the phone on the same network can do the same things.

Turn **Wireless debugging** off when you are finished, and leave it off away from home. It has to stay on while the remote is controlling this PC. `setup.bat` stops and asks you to type `YES` before it will pair.

A VPN that blocks the local network will stop the PC from reaching the phone. Turn the VPN off while you use the remote.

## What you need

- Windows 10 or 11
- Python 3.11 or newer, from [python.org](https://www.python.org/downloads/). During setup, turn on **Add python.exe to PATH**. Skip the Microsoft Store alias if Windows offers one.
- An Android phone on the same private Wi-Fi as the PC
- The Fire remote paired to that phone in Bluetooth settings

`adb` is downloaded for you the first time you run setup. You do not install platform-tools yourself.

## Install

Install Python 3 from [python.org](https://www.python.org/downloads/) and turn on **Add python.exe to PATH**. Skip the Microsoft Store alias if Windows offers one.

On your home Wi-Fi, clone the repo and double-click `setup.bat`:

```bat
git clone https://github.com/Param2596/ar-remote.git
cd ar-remote
```

`setup.bat` installs the tray libraries, downloads `adb` if it is missing, and puts a **Fire Remote** shortcut on the desktop and in Startup. The Startup shortcut comes up off, so the phone keeps the remote until you click the icon. Then it asks for the phone's pairing code. No cable.

On the phone, before you type `YES`:

1. Turn on Developer options and **Wireless debugging**. Leave it on.
2. Pair the Fire remote in Bluetooth settings.
3. Tap **Pair device with pairing code** and leave the popup open.
4. Type the popup's IP, port, and 6-digit code into the setup window.

The code expires quickly. If pairing fails, open the popup again. If the PC still cannot see the phone, close the popup and type the **IP address & Port** from the main Wireless debugging page.

Click the round icon by the clock. Gray is off, green is on. The icon is the switch from then on.

To pair again later, double-click `setup.bat` or run `python ar_remote.py --pair`.

If nothing connects, run `python ar_remote.py` in a window and read the error. `python ar_remote.py --list` prints the phone's input devices. The remote usually shows up as `AR Keyboard`.

## Daily use

Leave these on while you want the remote on the PC:

- **Wireless debugging.** Turning it off drops the connection.
- Phone Bluetooth, with the remote connected
- Phone and PC on the same home Wi-Fi
- The VPN off, if it blocks the local network

Click the tray icon to turn forwarding on or off. Off means the remote goes back to the phone. Debugging can stay on while the icon is gray.

Right-click the icon:

| Item | What it does |
| --- | --- |
| Use remote on this PC | Same as a left click. The check mark is on when forwarding is on. |
| Mode sound | Plays a short sound when Alexa changes mode. |
| Quit | Turns forwarding off and exits. |

After the phone reboots, turn Wireless debugging back on, then click the tray icon off and on.

When you are done, or when you leave home, turn Wireless debugging off.

`run.bat` opens the tray app again with no console window. `setup.bat` is only for the first install.

## Buttons

Alexa cycles three modes: **Controls**, **Volume**, **Cursor**. A label appears at the top of the screen. On the direction buttons and Menu, a tap does one step and holding repeats faster and faster. Other buttons stay down while held. Nothing uses a separate long-press action. The remote's power, sleep, and mic buttons are ignored. The mic audio never leaves the remote.

### Controls

| Remote | Windows |
| --- | --- |
| Up, Down, Left, Right | Arrow keys. A tap is one step. Holding speeds it up. |
| Center | Enter |
| Back | Full screen (F11) |
| Home | Windows key |
| Menu | Tab. A tap is one step. Holding speeds it up. |
| Play / Pause | Play / Pause |
| Rewind, Fast forward | Previous track, Next track |
| App shortcut (three lines) | Task View (Win+Tab) |
| Alexa | Next mode |

### Volume

| Remote | Windows |
| --- | --- |
| Up, Down | Volume up, Volume down. A tap is one step. Holding speeds it up. |
| Left, Right | Left arrow, Right arrow. A tap is one step. Holding speeds it up. |
| Center | Mute |
| Alexa | Next mode |

Home, Menu, Play / Pause, Rewind, and Fast forward still do what they do in Controls. Back is Escape here.

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
| `bridge.txt` | The private token between this PC and the phone |

## When it stops working

- **No phone found.** Wireless debugging is off, the phone is on another network, or a VPN is blocking LAN traffic. On your home Wi-Fi, run `python ar_remote.py --pair` again.
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
