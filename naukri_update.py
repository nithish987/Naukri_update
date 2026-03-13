"""
NAUKRI AUTO PROFILE UPDATER
Opens Resume Headline, adds/removes a space, saves — marks profile as updated
"""
from playwright.sync_api import sync_playwright
import time
import datetime

# ============================================================
#  FILL IN YOUR DETAILS
# ============================================================
NAUKRI_EMAIL    = "unithish22@gmail.com"
NAUKRI_PASSWORD = "Nithu98@"
# ============================================================

LOG_FILE = "naukri_log.txt"

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")

def get_toggle():
    try:
        with open("naukri_state.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_toggle(val):
    with open("naukri_state.txt", "w") as f:
        f.write(str(val))

def update_naukri():
    log("Starting Naukri profile update...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()

        try:
            # Step 1: Login
            log("Opening Naukri.com...")
            page.goto("https://www.naukri.com/nlogin/login", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(8)

            log("Logging in...")
            page.wait_for_selector('input[placeholder="Enter Email ID / Username"]', timeout=60000)
            page.fill('input[placeholder="Enter Email ID / Username"]', NAUKRI_EMAIL)
            page.fill('input[placeholder="Enter Password"]', NAUKRI_PASSWORD)
            page.get_by_role("button", name="Login", exact=True).click()
            time.sleep(8)

            # Step 2: Go to profile
            log("Going to profile page...")
            page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(8)

            # Step 3: Click Resume Headline edit button
            log("Opening Resume Headline editor...")
            page.get_by_text("Resume headline").first.click(timeout=10000)
            time.sleep(3)
            page.locator("span.edit").nth(0).click(timeout=10000)
            time.sleep(4)

            # Step 4: Find textarea and add/remove a space
            log("Editing headline text...")
            page.wait_for_selector("textarea", timeout=30000)
            textarea = page.locator("textarea").first
            current_text = textarea.input_value()

            toggle = get_toggle()
            if toggle == 0:
                new_text = current_text + " "    # add a space
            else:
                new_text = current_text.rstrip() # remove the space

            textarea.fill(new_text)
            save_toggle(1 if toggle == 0 else 0)
            log("Headline text updated!")

            # Step 5: Click Save
            log("Clicking Save...")
            page.get_by_role("button", name="Save").click(timeout=10000)
            time.sleep(4)

            log("Profile updated successfully!")
            browser.close()

        except Exception as e:
            log(f"Error: {str(e)}")
            try:
                page.screenshot(path="naukri_error.png")
                log("Screenshot saved as naukri_error.png")
            except:
                pass
            browser.close()

if __name__ == "__main__":
    update_naukri()

