import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

class DriverManager:
    def __init__(self):
        self.system = platform.system()
        self.use_existing_profile = False

    def install_webdriver_manager(self):
        try:
            import webdriver_manager
            print("webdriver-manager already installed")
            return True
        except ImportError:
            print("Installing webdriver-manager...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "webdriver-manager", "selenium"
                ])
                print("webdriver-manager installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to install webdriver-manager: {e}")
                return False

    def get_chrome_driver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        try:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--remote-allow-origins=*')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)

            # macOS specific Chrome binary path verification
            if self.system == 'Darwin':
                chrome_mac_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                if os.path.exists(chrome_mac_path):
                    options.binary_location = chrome_mac_path

            # Use a clean isolated temporary profile to avoid JSON parse & lock crashes
            isolated_profile = tempfile.mkdtemp(prefix="either_assistant_chrome_")
            options.add_argument(f'--user-data-dir={isolated_profile}')
            print(f"✓ Using isolated Chrome profile: {isolated_profile}")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            try:
                driver.maximize_window()
            except Exception:
                pass
            print("✓ Chrome driver initialized successfully")
            return driver
        except Exception as e:
            print(f"❌ Chrome driver failed: {str(e)[:150]}")
            return None

    def get_firefox_driver(self):
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service
        from selenium.webdriver.firefox.options import Options
        from webdriver_manager.firefox import GeckoDriverManager
        try:
            firefox_paths = {
                'Darwin': ['/Applications/Firefox.app/Contents/MacOS/firefox'],
                'Linux': ['/usr/bin/firefox', '/snap/bin/firefox'],
                'Windows': [r'C:\Program Files\Mozilla Firefox\firefox.exe']
            }
            if not any(os.path.exists(p) for p in firefox_paths.get(self.system, [])):
                print("Firefox browser not found")
                return None

            options = Options()
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            return driver
        except Exception as e:
            print(f"❌ Firefox driver failed: {str(e)[:150]}")
            return None

    def get_brave_driver(self):
        print("Brave browser skipped or not found")
        return None

    def get_chromium_driver(self):
        print("Chromium driver skipped")
        return None

    def get_edge_driver(self):
        print("Edge driver skipped")
        return None

    def get_default_browser_driver(self):
        browsers = [
            ('Chrome', self.get_chrome_driver),
            ('Firefox', self.get_firefox_driver),
        ]
        print("\n" + "="*60)
        print("BROWSER DRIVER INITIALIZATION")
        print("="*60)
        for browser_name, get_driver_func in browsers:
            print(f"\nTrying {browser_name}...")
            try:
                driver = get_driver_func()
                if driver:
                    print(f"\nSuccessfully initialized {browser_name} driver")
                    print("="*60 + "\n")
                    return driver
            except Exception as e:
                print(f"{browser_name} initialization error: {str(e)[:100]}")
                continue
        print("\nNo browser driver could be initialized")
        return None

def setup_driver():
    manager = DriverManager()
    if not manager.install_webdriver_manager():
        return None
    return manager.get_default_browser_driver()

if __name__ == "__main__":
    driver = setup_driver()
    if driver:
        print("Driver is ready to use!")
        driver.get("https://www.google.com")
        input("Press Enter to close the browser...")
        driver.quit()
    else:
        print("Failed to setup driver")