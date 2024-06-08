import re
from typing import Literal, Union
from .windows_ps import psstr, run_powershell as ps

KEYBOARD_TEMPLATE = r"""[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
[System.Windows.Forms.SendKeys]::SendWait({keys}) """


def send_keys(keys: str):
    """Sends the specified keys to the active window.

    Specify keys like ``{ENTER}`` for enter, ``{TAB}`` for tab, ``%{f4}`` for alt F4, etc.

    ```
    Key  | Code
    -----------
    SHIFT  +
    CTRL   ^
    ALT    %
    ```

    Args:
        keys (str): The keys to send to the active window.
    """
    ps(KEYBOARD_TEMPLATE, {"keys": psstr(keys)})


def write(text: str):
    """Writes the specified text to the active window.

    Automatically replaces ``\\n`` (new line) to `BACKSLASHn`.
    This is relatively safe since it is not using ``~``.

    Args:
        text (str): The text to write to the active window.
    """
    if re.findall(r"[\^+~]|{[A-Z]{2,}}|{F(?:[1-9]|1[0-6])}", text):
        raise ValueError(
            "Invalid text. (Found possible key codes which can harm your computer)"
        )

    send_keys(text.replace("\n", "~"))


Keys = Literal[
    "⌘",
    "ctrl",
    "control",
    "⌥",
    "alt",
    "⇧",
    "shift",
    "⌃",
    "⌫",
    "backspace",
    "bs",
    "esc",
    "escape",
    "⌦",
    "del",
    "delete",
    "⏎",
    "enter",
    "⇪",
    "capslock",
]
Chars = Literal[
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

hotkey_map = {
    "⌘": "^",
    "ctrl": "^",
    "control": "^",
    "⌥": "%",
    "alt": "%",
    "⇧": "+",
    "shift": "+",
    "⌫": "{bs}",
    "escape": "{esc}",
    "⌦": "{del}",
    "⏎": "~",
    "enter": "~",
    "⇪": "{capslock}",
}


def hotkey(*keys: Union[Keys, Chars]):
    """Sends the specified keys to the active window.

    Args:
        *keys (Union[Keys, Chars]): The keys to send to the active window.
    """
    keycache = ""
    for key in keys:
        keycache += hotkey_map.get(key, "{%s}" % key).upper()

    assert keycache not in {
        "^%{DEL}",
        "^%{DELETE}",
    }, "This wouldn't work. (Evaluating CTRL SHIFT DEL)"
    send_keys(keycache)
