from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

class BrowserController:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def _ensure_valid_window(self):
        """Ensure we're on a valid window, switch if current is closed"""
        try:
            _ = self.driver.current_window_handle
            return True
        except Exception:
            try:
                handles = self.driver.window_handles
                if handles:
                    self.driver.switch_to.window(handles[0])
                    print("⚠️  Previous window was closed. Switched to available window.")
                    return True
                else:
                    print("❌ No browser windows available!")
                    return False
            except Exception as e:
                print(f"❌ Cannot recover from closed window: {e}")
                return False

    def click_first_link(self):
        """Click the first organic link/product on page"""
        return self.click_nth_element(1, element_type="link")

    def click_nth_element(self, n, element_type="link"):
        """Click the nth link, video, or result instantly via in-browser JavaScript"""
        try:
            if not self._ensure_valid_window():
                return False

            print(f"🖱️  Clicking {n}th {element_type}...")
            target_idx = max(0, n - 1)

            # In-browser JavaScript locates and triggers the click without hanging Selenium
            js_script = """
            const targetIndex = arguments[0];
            const type = arguments[1];

            function getCandidates() {
                if (type === 'video') {
                    return Array.from(document.querySelectorAll('ytd-video-renderer a#video-title, a#video-title-link, video'));
                }
                
                // Prioritized list of modern search and e-commerce product selectors
                const selectors = [
                    "div[data-component-type='s-search-result'] h2 a",
                    "div.s-result-item h2 a",
                    "a.a-link-normal.s-underline-text",
                    "div#search div.g a:has(h3)",
                    "div#search a h3",
                    "ytd-video-renderer a#video-title",
                    "main h2 a",
                    "main h3 a",
                    "h2 a"
                ];

                for (let sel of selectors) {
                    let found = Array.from(document.querySelectorAll(sel));
                    let visible = found.filter(el => {
                        let rect = el.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0 && el.href && !el.href.startsWith('javascript:');
                    });
                    if (visible.length > 0) {
                        return visible;
                    }
                }

                // Fallback: visible semantic links
                return Array.from(document.querySelectorAll('main a[href], div#content a[href], body a[href]'))
                    .filter(el => {
                        let rect = el.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0 && el.innerText.trim().length > 3;
                    });
            }

            const candidates = getCandidates();
            if (candidates.length > targetIndex) {
                const target = candidates[targetIndex];
                target.scrollIntoView({behavior: 'smooth', block: 'center'});
                
                const title = target.innerText.trim() || target.getAttribute('aria-label') || target.href;
                
                // Dispatch click directly inside browser context
                try {
                    target.click();
                } catch(e) {
                    target.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
                }

                return { success: true, title: title, total: candidates.length };
            }

            return { success: false, total: candidates.length };
            """

            result = self.driver.execute_script(js_script, target_idx, element_type.lower())

            if result and result.get("success"):
                title = result.get("title", f"{element_type} #{n}")
                print(f"✓ Clicked {n}th {element_type}: {title[:60]}")
                return True
            else:
                total_found = result.get("total", 0) if result else 0
                print(f"✗ Found {total_found} {element_type}s, could not click #{n}")
                return False

        except Exception as e:
            print(f"✗ Click failed: {e}")
            return False

    def scroll_down(self, amount="medium"):
        try:
            if not self._ensure_valid_window():
                return False
            print("📜 Scrolling down...")
            scroll_amounts = {
                'small': 350,
                'medium': 650,
                'large': 1000,
            }
            pixels = scroll_amounts.get(amount, 650)
            self.driver.execute_script(f"""
                window.scrollBy({{top: {pixels}, left: 0, behavior: 'smooth'}});
                var el = document.scrollingElement || document.documentElement || document.body;
                if (el) el.scrollTop += {pixels};
            """)
            time.sleep(0.5)
            print("✓ Scrolled down!")
            return True
        except Exception as e:
            print(f"✗ Scroll failed: {e}")
            return False

    def scroll_up(self, amount="medium"):
        try:
            if not self._ensure_valid_window():
                return False
            print("📜 Scrolling up...")
            scroll_amounts = {
                'small': 350,
                'medium': 650,
                'large': 1000,
            }
            pixels = scroll_amounts.get(amount, 650)
            self.driver.execute_script(f"""
                window.scrollBy({{top: -{pixels}, left: 0, behavior: 'smooth'}});
                var el = document.scrollingElement || document.documentElement || document.body;
                if (el) el.scrollTop -= {pixels};
            """)
            time.sleep(0.5)
            print("✓ Scrolled up!")
            return True
        except Exception as e:
            print(f"✗ Scroll failed: {e}")
            return False

    def scroll_to_element(self, text):
        try:
            if not self._ensure_valid_window():
                return False
            print(f"📜 Scrolling to: {text}")
            xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
            elements = self.driver.find_elements(By.XPATH, xpath)
            for el in elements:
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
                    time.sleep(0.5)
                    print(f"✓ Scrolled to: {text}")
                    return True
            print(f"✗ Could not find: {text}")
            return False
        except Exception as e:
            print(f"✗ Scroll failed: {e}")
            return False

    def close_popup(self):
        try:
            if not self._ensure_valid_window():
                return False
            print("❌ Closing popup...")
            close_selectors = [
                "button[aria-label*='close' i]",
                "button[title*='close' i]",
                "[class*='close' i]",
                "button.close",
                "div[role='button'][aria-label*='close' i]",
                "svg[aria-label='Close']",
            ]
            for selector in close_selectors:
                try:
                    close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if close_btn.is_displayed():
                        close_btn.click()
                        time.sleep(0.5)
                        print("✓ Popup closed!")
                        return True
                except Exception:
                    continue
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
                print("✓ Pressed Escape key!")
                return True
            except Exception:
                pass
            print("✗ No popup found or could not close")
            return False
        except Exception as e:
            print(f"✗ Close popup failed: {e}")
            return False

    def volume_up(self):
        try:
            print("🔊 Increasing volume...")
            video = self.driver.find_element(By.TAG_NAME, "video")
            current_volume = self.driver.execute_script("return arguments[0].volume;", video)
            new_volume = min(current_volume + 0.1, 1.0)
            self.driver.execute_script(f"arguments[0].volume = {new_volume};", video)
            print(f"✓ Volume increased to {int(new_volume * 100)}%")
            return True
        except Exception as e:
            print(f"✗ Volume up failed: {e}")
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ARROW_UP).perform()
                print("✓ Sent volume up key")
                return True
            except Exception:
                return False

    def volume_down(self):
        try:
            print("🔉 Decreasing volume...")
            video = self.driver.find_element(By.TAG_NAME, "video")
            current_volume = self.driver.execute_script("return arguments[0].volume;", video)
            new_volume = max(current_volume - 0.1, 0.0)
            self.driver.execute_script(f"arguments[0].volume = {new_volume};", video)
            print(f"✓ Volume decreased to {int(new_volume * 100)}%")
            return True
        except Exception as e:
            print(f"✗ Volume down failed: {e}")
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ARROW_DOWN).perform()
                print("✓ Sent volume down key")
                return True
            except Exception:
                return False

    def click_element_by_text(self, text, page_reader=None):
        try:
            if not self._ensure_valid_window():
                return False
            print(f"🖱️  Clicking element: {text}")
            text_clean = re.sub(r'\b(called|titled|named|file|page|link|button|there is a|can you)\b', '', text.lower()).strip()
            wait = WebDriverWait(self.driver, 4)
            
            try:
                xpath = f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text_clean}')]"
                element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click();", element)
                print(f"✓ Clicked: {element.text.strip()}")
                return True
            except Exception:
                pass

            try:
                xpath = f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text_clean}')]"
                element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click();", element)
                print(f"✓ Clicked: {element.text.strip()}")
                return True
            except Exception:
                pass

            if page_reader:
                element = page_reader.find_element_by_partial_text(text_clean)
                if element:
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        print("✓ Clicked via PageReader!")
                        return True
                    except Exception:
                        pass

            print(f"✗ Could not find element: {text}")
            return False
        except Exception as e:
            print(f"✗ Click failed: {e}")
            return False

    def highlight_element(self, element):
        try:
            css = """
            @keyframes pulse-circle {
                0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
                50% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
            }
            .ai-highlight {
                animation: pulse-circle 2s infinite !important;
                border: 3px solid red !important;
                border-radius: 8px !important;
                padding: 5px !important;
                transition: all 0.3s ease !important;
            }
            """
            self.driver.execute_script(f"""
                if (!document.getElementById('ai-highlight-style')) {{
                    var style = document.createElement('style');
                    style.id = 'ai-highlight-style';
                    style.textContent = `{css}`;
                    document.head.appendChild(style);
                }}
            """)
            self.driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
                arguments[0].classList.add('ai-highlight');
            """, element)
            print("✨ Element highlighted with animation!")
            return True
        except Exception as e:
            print(f"⚠ Could not highlight element: {e}")
            return False

    def remove_highlight(self, element=None):
        try:
            if element:
                self.driver.execute_script("arguments[0].classList.remove('ai-highlight');", element)
            else:
                self.driver.execute_script("""
                    document.querySelectorAll('.ai-highlight').forEach(el => {
                        el.classList.remove('ai-highlight');
                    });
                """)
            return True
        except Exception:
            return False

    def play_video_by_title(self, title):
        try:
            if not self._ensure_valid_window():
                return False
            print(f"▶️  Playing video: {title}")
            youtube_selectors = [
                f"//ytd-video-renderer//a[@title[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title.lower()}')]]",
                f"//ytd-grid-video-renderer//a[@title[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title.lower()}')]]",
            ]
            for selector in youtube_selectors:
                try:
                    video_link = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", video_link)
                    time.sleep(0.5)
                    video_link.click()
                    print(f"✓ Playing video: {title}")
                    return True
                except Exception:
                    continue

            xpath = f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title.lower()}')]"
            elements = self.driver.find_elements(By.XPATH, xpath)
            for target in elements:
                if target.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target)
                    time.sleep(0.5)
                    target.click()
                    print(f"✓ Playing video: {title}")
                    return True

            print(f"✗ Video not found: {title}")
            return False
        except Exception as e:
            print(f"✗ Play video failed: {e}")
            return False
    
    # ==================== TAB MANAGEMENT ====================
    
    def create_new_tab(self, url=None):
        try:
            if not self._ensure_valid_window():
                return False
            print("📑 Creating new tab...")
            original_handle = self.driver.current_window_handle
            original_handles = self.driver.window_handles
            
            self.driver.execute_script("window.open('');")
            time.sleep(0.5)
            
            new_handles = self.driver.window_handles
            new_tab = [h for h in new_handles if h not in original_handles][0]
            self.driver.switch_to.window(new_tab)
            
            if url:
                self.driver.get(url)
                print(f"✓ New tab created and navigated to {url}")
            else:
                print("✓ New tab created!")
            
            try:
                self.driver.switch_to.window(original_handle)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"✗ Create new tab failed: {e}")
            self._ensure_valid_window()
            return False
    
    def switch_to_tab(self, tab_index):
        try:
            handles = self.driver.window_handles
            if 0 < tab_index <= len(handles):
                self.driver.switch_to.window(handles[tab_index - 1])
                print(f"✓ Switched to tab {tab_index}")
                return True
            else:
                print(f"✗ Tab {tab_index} not found. Only {len(handles)} tabs open.")
                return False
        except Exception as e:
            print(f"✗ Switch tab failed: {e}")
            return False
    
    def switch_to_first_tab(self):
        try:
            handles = self.driver.window_handles
            if handles:
                self.driver.switch_to.window(handles[0])
                print("✓ Switched to first tab!")
                return True
            return False
        except Exception as e:
            print(f"✗ Switch to first tab failed: {e}")
            return False
    
    def switch_to_last_tab(self):
        try:
            handles = self.driver.window_handles
            if handles:
                self.driver.switch_to.window(handles[-1])
                print("✓ Switched to last tab!")
                return True
            return False
        except Exception as e:
            print(f"✗ Switch to last tab failed: {e}")
            return False
    
    def switch_to_next_tab(self):
        try:
            handles = self.driver.window_handles
            current_handle = self.driver.current_window_handle
            current_index = handles.index(current_handle)
            next_index = (current_index + 1) % len(handles)
            self.driver.switch_to.window(handles[next_index])
            print(f"✓ Switched to next tab (tab {next_index + 1})")
            return True
        except Exception as e:
            print(f"✗ Switch to next tab failed: {e}")
            return False
    
    def switch_to_previous_tab(self):
        try:
            handles = self.driver.window_handles
            current_handle = self.driver.current_window_handle
            current_index = handles.index(current_handle)
            prev_index = (current_index - 1) % len(handles)
            self.driver.switch_to.window(handles[prev_index])
            print(f"✓ Switched to previous tab (tab {prev_index + 1})")
            return True
        except Exception as e:
            print(f"✗ Switch to previous tab failed: {e}")
            return False
    
    def close_current_tab(self):
        try:
            handles = self.driver.window_handles
            if len(handles) > 1:
                self.driver.close()
                remaining_handles = self.driver.window_handles
                self.driver.switch_to.window(remaining_handles[0])
                print("✓ Tab closed!")
                return True
            else:
                print("✗ Cannot close the last tab")
                return False
        except Exception as e:
            print(f"✗ Close tab failed: {e}")
            return False
    
    def close_other_tabs(self):
        try:
            current_handle = self.driver.current_window_handle
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != current_handle:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
            self.driver.switch_to.window(current_handle)
            print("✓ All other tabs closed!")
            return True
        except Exception as e:
            print(f"✗ Close other tabs failed: {e}")
            return False
    
    def list_all_tabs(self):
        try:
            handles = self.driver.window_handles
            current_handle = self.driver.current_window_handle
            print("\n📑 Open Tabs:")
            print("=" * 70)
            for i, handle in enumerate(handles, 1):
                self.driver.switch_to.window(handle)
                title = self.driver.title or "(No title)"
                current_marker = " ← Current" if handle == current_handle else ""
                print(f"  {i}. {title}{current_marker}")
            self.driver.switch_to.window(current_handle)
            print("=" * 70)
            print(f"Total tabs: {len(handles)}\n")
            return True
        except Exception as e:
            print(f"✗ List tabs failed: {e}")
            return False
    
    # ==================== WINDOW MANAGEMENT ====================
    
    def create_new_window(self, url=None):
        try:
            if not self._ensure_valid_window():
                return False
            print("🪟 Creating new window...")
            original_handle = self.driver.current_window_handle
            original_handles = self.driver.window_handles
            
            self.driver.execute_script("window.open('', '_blank', 'width=1200,height=800');")
            time.sleep(0.5)
            
            new_handles = self.driver.window_handles
            new_window = [h for h in new_handles if h not in original_handles][0]
            self.driver.switch_to.window(new_window)
            
            if url:
                self.driver.get(url)
                print(f"✓ New window created and navigated to {url}")
            else:
                self.driver.get("about:blank")
                print("✓ New window created!")
            
            try:
                self.driver.switch_to.window(original_handle)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"✗ Create new window failed: {e}")
            self._ensure_valid_window()
            return False
    
    def create_incognito_window(self):
        return self.create_new_window()
    
    def maximize_window(self):
        try:
            self.driver.maximize_window()
            print("✓ Window maximized!")
            return True
        except Exception as e:
            print(f"✗ Maximize window failed: {e}")
            return False
    
    def minimize_window(self):
        try:
            self.driver.minimize_window()
            print("✓ Window minimized!")
            return True
        except Exception as e:
            print(f"✗ Minimize window failed: {e}")
            return False
    
    def fullscreen_window(self):
        try:
            self.driver.fullscreen_window()
            print("✓ Fullscreen mode activated!")
            return True
        except Exception as e:
            print(f"✗ Fullscreen failed: {e}")
            return False
    
    # ==================== NAVIGATION ====================
    
    def go_back(self):
        try:
            self.driver.back()
            time.sleep(0.5)
            print("✓ Navigated back!")
            return True
        except Exception as e:
            print(f"✗ Go back failed: {e}")
            return False
    
    def go_forward(self):
        try:
            self.driver.forward()
            time.sleep(0.5)
            print("✓ Navigated forward!")
            return True
        except Exception as e:
            print(f"✗ Go forward failed: {e}")
            return False
    
    def refresh_page(self):
        try:
            self.driver.refresh()
            time.sleep(1)
            print("✓ Page refreshed!")
            return True
        except Exception as e:
            print(f"✗ Refresh failed: {e}")
            return False
    
    def get_current_url(self):
        try:
            url = self.driver.current_url
            print(f"🔗 Current URL: {url}")
            return url
        except Exception as e:
            print(f"✗ Get URL failed: {e}")
            return None
    
    def get_page_title(self):
        try:
            title = self.driver.title
            print(f"📄 Page title: {title}")
            return title
        except Exception as e:
            print(f"✗ Get title failed: {e}")
            return None