import subprocess

# Read URLs from file
file_path = "bookmarkLinks.txt"
with open(file_path, "r") as f:
    urls = [line.strip() for line in f if line.strip().startswith("http")]

if not urls:
    print("⚠️ No valid URLs found in bookmarkLinks.txt")
    exit(0)

print(f"🌐 Opening {len(urls)} links in Safari...\n")

for i, url in enumerate(urls, 1):
    print(f"➡️ [{i}/{len(urls)}] Opening: {url}")

    # AppleScript to open a new tab, click bookmark, then close the tab
    script = f'''
tell application "Safari"
    if not (exists window 1) then make new document
    tell window 1
        set newTab to make new tab with properties {{URL:"{url}"}}
        set current tab to newTab
    end tell
    -- Attempt to click the bookmark button after short delay
    delay 1
    try
        do JavaScript "var btn = document.querySelector('#bookmark-post-btn'); if(btn) {{ btn.click(); }}" in newTab
    end try
    delay 1
    -- Close the tab
    tell window 1 to close newTab
end tell
'''

    subprocess.run(["osascript", "-e", script])

print("🎉 Done — all tabs opened, clicked, and closed!")