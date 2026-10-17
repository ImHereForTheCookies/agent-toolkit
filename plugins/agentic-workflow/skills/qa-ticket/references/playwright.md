# Minimal Playwright check (Python)

Run from a scratch file in `$QA`, never inside the repo. Use the preinstalled browser; do not download one.

```python
import glob, os, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("QA_BASE") or f"http://127.0.0.1:{os.environ['PORT']}"  # PORT: the port found in SKILL.md section 2
SHOTS = os.path.join(os.environ["QA"], "shots")
os.makedirs(SHOTS, exist_ok=True)
chrome = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome)  # None = Playwright's own lookup
    page = browser.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))

    page.goto(BASE)
    page.screenshot(path=f"{SHOTS}/01-home.png")
    page.get_by_role("button", name="Add").click()          # act like a user
    assert page.get_by_text("Expected text").is_visible()   # check what is rendered
    page.reload()                                            # persistence
    page.screenshot(path=f"{SHOTS}/02-after-reload.png")
    print("console errors:", errors)
    browser.close()
```

Notes:
- If `launch` fails to find a browser, set `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` and retry; check `ls /opt/pw-browsers`.
- Prefer role and text locators over CSS selectors; they fail when the UI is actually wrong.
- Console errors and failed network requests count as observations; report them.
- Phone-width check when the ticket mentions mobile: `browser.new_page(viewport={"width": 390, "height": 844})`.
