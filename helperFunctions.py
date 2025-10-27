import time
import subprocess
import pyautogui
import pyperclip

# focus dia browser
def focus_dia():
    """Bring the Dia browser window to the front using AppleScript."""
    apple_script = '''
    tell application "Dia" to activate
    tell application "System Events"
        tell process "Dia"
            set frontmost to true
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script], check=False)

# send ⌘T to open new tab
def send_cmd_t():
    """Press ⌘T with a brief hold to ensure macOS registers it."""
    pyautogui.keyDown("command")
    time.sleep(0.18)
    pyautogui.press("t")
    time.sleep(0.18)
    pyautogui.keyUp("command")

# execute JS in console
def execute_js_in_console(js_code):
    """Paste and execute JS code in DevTools Console and return clipboard content."""
    pyperclip.copy("")  # Clear clipboard
    pyperclip.copy(js_code)
    pyautogui.hotkey("command", "v")
    time.sleep(0.4)
    pyautogui.press("enter")

    # Wait for clipboard to update
    timeout = 6
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(0.5)
        content = pyperclip.paste()
        if content and not content.startswith("var el ="):
            return content
    return None

# focus devtools
def focus_devtools():
    """Click approximate middle of DevTools to ensure focus."""
    pyautogui.click(x=370, y=886)
    time.sleep(0.5)