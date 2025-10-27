import re
import subprocess
from bs4 import BeautifulSoup
import chime

# =============================
# Configuration
# =============================
chime.theme('pokemon')

BOOKMARKS_PAGE_URL = "https://app.daily.dev/bookmarks"
BOOKMARKS_FILE = "bookmarkLinks.txt"
BASE_URL = "https://app.daily.dev"

GRID_SELECTORS = [
    "div.grid.grid-cols-1",
    "div.grid.gap-8.grid-cols-2",
    "div.grid.gap-8.grid-cols-3"
]

CARD_LINK_CLASS = "Card_link__dw67X"
SCROLL_COUNT = 20       # 🔁 number of scrolls to perform
SCROLL_DELAY = 1.5      # ⏳ seconds to wait between scrolls

# =============================
# Step 1: Open Safari, auto-scroll, grab HTML
# =============================
print("🌐 Opening bookmarks page in Safari & auto-scrolling...")

selectors_js = (
    f"var el = document.querySelector('{GRID_SELECTORS[0]}');"
    f"if (!el) {{ el = document.querySelector('{GRID_SELECTORS[1]}'); }}"
    f"if (!el) {{ el = document.querySelector('{GRID_SELECTORS[2]}'); }}"
    "if (el) { el.outerHTML } else { '<<ELEMENT_NOT_FOUND>>' };"
)

scroll_js = f"""
let totalHeight = 0;
let distance = 800;
let timer = setInterval(() => {{
  window.scrollBy(0, distance);
  totalHeight += distance;
  if (totalHeight > document.body.scrollHeight) {{
    clearInterval(timer);
  }}
}}, {int(SCROLL_DELAY * 1000)});
"""

script = f'''
tell application "Safari"
    if not (exists window 1) then make new document
    tell window 1
        set newTab to make new tab with properties {{URL:"{BOOKMARKS_PAGE_URL}"}}
        set current tab to newTab
    end tell
    activate
    delay 5

    -- Auto-scroll loop
    repeat {SCROLL_COUNT} times
        do JavaScript "window.scrollBy(0, 1000);" in newTab
        delay {SCROLL_DELAY}
    end repeat

    -- After scrolling, capture HTML
    set htmlContent to do JavaScript "{selectors_js}" in newTab
    tell window 1 to close newTab
end tell
return htmlContent
'''

result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
html_content = result.stdout.strip()

# =============================
# Step 2: Extract visible & valid post links
# =============================
if not html_content or html_content == "<<ELEMENT_NOT_FOUND>>":
    print("⚠️ Could not find grid — try increasing delay or scroll count.")
else:
    soup = BeautifulSoup(html_content, "html.parser")

    visible_articles = [
        a for a in soup.find_all("article")
        if not a.get("style") or "display: none" not in a.get("style")
    ]

    hrefs = []
    for article in visible_articles:
        a_tag = article.find("a", class_=CARD_LINK_CLASS)
        if a_tag and a_tag.get("href"):
            hrefs.append(BASE_URL + a_tag["href"])

    # ✅ Filter only proper post URLs
    valid_links = [
        link for link in hrefs
        if re.match(r"^https://app\.daily\.dev/posts/[A-Za-z0-9_-]+$", link)
    ]

    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        f.writelines(link + "\n" for link in valid_links)

    print(f"💾 Saved {len(valid_links)} post links to {BOOKMARKS_FILE}")

chime.success()