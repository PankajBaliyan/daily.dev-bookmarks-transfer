import pyautogui
import pyperclip
import time
import chime
import subprocess
from bs4 import BeautifulSoup
from helperFunctions import focus_dia, execute_js_in_console, send_cmd_t, focus_devtools

# =============================
# Configuration
# =============================
chime.theme('pokemon')
URL = "https://app.daily.dev/bookmarks"
OUTPUT_HTML_FILE = "output.txt"
BOOKMARKS_FILE = "bookmarkLinks.txt"
BASE_URL = "https://app.daily.dev"

# Add this new configuration variable
GRID_SELECTOR1 = "div.grid.grid-cols-1"  
GRID_SELECTOR2 = "div.grid.gap-8.grid-cols-2"
GRID_SELECTOR3 = "div.grid.gap-8.grid-cols-3"  


CARD_LINK_CLASS = "Card_link__dw67X"


# =============================
# Automation Steps
# =============================
try:
    print("🚀 Starting automation...")

    # 1️⃣ Focus Dia browser
    focus_dia()
    time.sleep(1.5)

    # 2️⃣ Open new tab
    send_cmd_t()
    time.sleep(1)

    # 3️⃣ Navigate to target URL
    pyautogui.write(URL)
    pyautogui.press("enter")
    print("🌐 Navigating to page...")
    time.sleep(6)  # Adjust based on network speed

    # 4️⃣ Open DevTools
    pyautogui.hotkey("command", "option", "i")
    time.sleep(1.5)

    # 5️⃣ Focus DevTools (click approximate middle)
    focus_devtools()

    # 6️⃣ Switch to Console panel
    pyautogui.hotkey("command", "]")
    time.sleep(0.8)
    print("🧭 Switched to Console panel.")
    time.sleep(1.5)

    # 7️⃣ JavaScript to copy target element's outerHTML
    js_code = (
        f'var el = document.querySelector("{GRID_SELECTOR1}");'
        f'if (!el) {{ el = document.querySelector("{GRID_SELECTOR2}"); }}'
        f'if (!el) {{ el = document.querySelector("{GRID_SELECTOR3}"); }}'
        'if (el) { copy(el.outerHTML); } else { copy("<<ELEMENT_NOT_FOUND>>"); }'
    )
    print("📋 Executing copy() in Console...")
    div_html = execute_js_in_console(js_code)
    time.sleep(1.5)


    # 8️⃣ Validate clipboard content
    if not div_html:
        raise Exception(
            "Clipboard did not update — check if Console got focus or if copy() is allowed."
        )
    elif div_html == "<<ELEMENT_NOT_FOUND>>":
        print("⚠️ Element not found on page — selector might differ.")
    elif div_html.strip().startswith("<"):
        with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(div_html)
        print(f"✅ HTML content saved to {OUTPUT_HTML_FILE}")

        # Close current tab
        time.sleep(0.5)
        pyautogui.hotkey("command", "w")
        print("🔒 Closed browser tab")
    else:
        print("⚠️ Clipboard content doesn't look like HTML, skipping save.")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Check Accessibility permissions or adjust sleep timing if needed.")

finally:
    # Close DevTools (toggle same shortcut)
    try:
        pyautogui.hotkey("command", "option", "i")
    except Exception:
        pass
    print("🏁 Automation finished.")

# =============================
# Parse HTML and extract bookmark links
# =============================
try:
    with open(OUTPUT_HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Find all <article> elements
    all_articles = soup.find_all("article")

    # Filter out hidden ones
    visible_articles = [
        article for article in all_articles
        if not article.get("style") or "display: none" not in article.get("style")
    ]

    print(f"Found {len(visible_articles)} visible bookmark articles.")

    hrefs = []
    for article in visible_articles:
        a_tag = article.find("a", class_=CARD_LINK_CLASS)
        if a_tag and a_tag.get("href"):
            hrefs.append(a_tag["href"])

    # Prepend base URL and save final links
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        for href in hrefs:
            f.write(BASE_URL + href + "\n")

    print(f"Total {len(hrefs)} bookmark links saved to {BOOKMARKS_FILE}")

except Exception as e:
    print(f"❌ Error parsing HTML: {e}")

chime.success()