# revilo <kbd>AI</kbd>
Revilo Computer API. Will support AI soon.

## Windows API
The Revilo Windows API plays some tricks with Powershell and provides clean APIs. What's more, it's: ✨ LIGHTWEIGHT! ✨

To import, -

```python
from revilo.windows import ...   # import item (e.g., ps, mouse, ...)
```

### Run Powershell

This is the core building block of the Revilo Computer API for Windows — Powershell.

```python
ps.run("Write-Host I love chocolate!")  # 'I love chocolate!\n'
ps.run('Write-Host "Yo: $({c})"', vars={"c": "6*9 + 6+9"})  # 'Yo: 69\n'
```

### Keyboard API <kbd>* AI</kbd>

The keyboard API provides a clean interface for sending keys to the current foreground application.
It provides both text and hotkeys API.

```python
# Simple write API
keyboard.write("I love Texas!")
keyboard.write("Multi-\nlines work, too!")

# Hotkey (equivalents)
keyboard.hotkey("⌘", "shift", "esc")  # Opens Task Manager
keyboard.hotkey("ctrl", "shift", "esc")  # Seriously, again!
```

### Mouse API <kbd>* AI</kbd>

The mouse API is elegant, too!

```python
mouse.move(100, 200)   # (x, y)

mouse.click()
mouse.click(100, 200)  # (x, y)
mouse.get_position()   # -> (x, y)
```

### Screen API <kbd>* AI</kbd>

The screen API will be integrated with AI soon!
Just a quick note: don't copy Microsoft's idea of stalking people's history (it's a decent idea for privacy leaks) because everyone loves their idea and will definitely go stonks!

```python
# Takes a screenshot
screen.take_screenshot("./my-screenshot.png")

# Gets the current app name (foreground)
screen.get_current_app()
```

### Notifications (Toast) API

The toast API is not 100% covered (for `<toast>`), but overall it's clean!

```python
# Send a simple toast
toast.notify("Epic title!", "Epic text")

# Add a sound
toast.notify(
    "Hear me!",
    "Yes you will.", 
    audio="ms-winsoundevent:Notification.Looping.Call9",  # don't worry: type hints!
    audio_loops=True,
    duration="long",  # or short
    scenario="incomingCall"  # "reminder" | "alarm" | "incomingCall" | "urgent"
)

# Add actions
toast.notify(
    "📈 Time to increase traffic!",
    "Click to open Google for no reason!!!",
    actions=[
        toast.Action("Google Time", "https://google.com")
    ]
)
```
