import time
import pyautogui
import chime
from helperFunctions import focus_dia, execute_js_in_console, send_cmd_t, focus_devtools

BOOKMARKS_FILE = "bookmarkLinks.txt"
chime.theme('pokemon')

# =============================
# New Feature: Remove bookmarks for all links (Improved Stability)
# =============================

try:
    # Read all bookmarks into a list
    with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
        bookmarks = [line.strip() for line in f if line.strip()]

    if not bookmarks:
        print("⚠️ No bookmarks found in file.")
    else:
        for idx, link in enumerate(bookmarks, start=1):
            print(f"\n🔗 [{idx}/{len(bookmarks)}] Opening bookmark: {link}")

            # Ensure browser is active
            focus_dia()
            time.sleep(1.2)

            # Open new tab and navigate
            send_cmd_t()
            time.sleep(0.6)
            pyautogui.write(link)
            pyautogui.press("enter")
            print("🌍 Navigating to link...")
            time.sleep(7)  # Allow page to load fully

            # Open DevTools
            focus_dia()
            pyautogui.hotkey("command", "option", "i")
            time.sleep(2)

            # Focus DevTools
            focus_devtools()

            # Switch to Console
            pyautogui.hotkey("command", "]")
            time.sleep(1.2)
            print("🧭 Switched to Console panel.")

            # Execute JS with retry logic
            remove_button_js = (
                'var btn = document.getElementById("bookmark-post-btn");'
                'if(btn){ btn.click(); copy("CLICKED"); } else { copy("BTN_NOT_FOUND"); }'
            )

            print("🖱 Attempting to click remove button...")
            for attempt in range(3):
                result = execute_js_in_console(remove_button_js)
                if result:
                    break
                print(f"⏳ Retry {attempt + 1}/3: waiting for clipboard update...")
                time.sleep(1.5)

            if result == "CLICKED":
                print("✅ Bookmark removed successfully!")
            elif result == "BTN_NOT_FOUND":
                print("⚠️ Remove button not found on page.")
            else:
                print("❌ No response from console — possible focus issue.")

            # Close current tab
            pyautogui.hotkey("command", "w")
            print("🔒 Closed browser tab")

            # Allow browser to settle before next link
            time.sleep(3.5)
            focus_dia()
            time.sleep(0.8)

except Exception as e:
    print(f"❌ Error removing bookmarks: {e}")
finally:
    chime.success()