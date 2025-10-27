import subprocess

# =============================
# Configuration
# =============================
file_path = "bookmarkLinks.txt"
MODE = "add"      # 🔁 Options: "add" or "remove"
CLICK_DELAY = 3   # seconds before and after clicking

# =============================
# Read URLs
# =============================
with open(file_path, "r") as f:
    urls = [line.strip() for line in f if line.strip().startswith("http")]

if not urls:
    print("⚠️ No valid URLs found in bookmarkLinks.txt")
    exit(0)

print(f"🌐 Opening {len(urls)} links in Safari (mode: {MODE})...\n")

# =============================
# Loop through and process each URL
# =============================
for i, url in enumerate(urls, 1):
    print(f"➡️ [{i}/{len(urls)}] Opening: {url}")

    # Choose JS logic based on mode
    if MODE == "add":
        js_action = """
            var btn = document.querySelector('#bookmark-post-btn');
            if (btn && btn.getAttribute('aria-label') === 'Bookmark') {
                btn.click();
            }
        """
    elif MODE == "remove":
        js_action = """
            var btn = document.querySelector('#bookmark-post-btn');
            if (btn && btn.getAttribute('aria-label') === 'Remove bookmark') {
                btn.click();
            }
        """
    else:
        print("❌ Invalid MODE — must be 'add' or 'remove'.")
        exit(1)

    # AppleScript to open, click, and close
    script = f'''
tell application "Safari"
    if not (exists window 1) then make new document
    tell window 1
        set newTab to make new tab with properties {{URL:"{url}"}}
        set current tab to newTab
    end tell
    delay {CLICK_DELAY}
    try
        do JavaScript "{js_action}" in newTab
    end try
    delay {CLICK_DELAY}
    tell window 1 to close newTab
end tell
'''

    subprocess.run(["osascript", "-e", script])

print(f"🎉 Done — all tabs processed in '{MODE}' mode!")