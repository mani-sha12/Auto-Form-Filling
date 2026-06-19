#!/usr/bin/env python3
"""
Automated Job Form Filler Bot
Automatically fills job application forms on external websites
"""

import sys
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Configuration
API_BASE_URL = "http://localhost:8000"
HEADLESS = False  # Set to True to run without showing browser window


class JobFormFiller:
    """Automatically fills job application forms with resume data"""

    def __init__(self, profile_id: str, headless: bool = HEADLESS):
        """
        Initialize the form filler
        
        Args:
            profile_id: ID of the resume profile to use
            headless: Whether to run browser in headless mode
        """
        self.profile_id = profile_id
        self.headless = headless
        self.driver = None
        self.profile_data = None
        self.filled_fields = []

    def get_profile_data(self) -> bool:
        """Fetch profile data from API"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/profiles/{self.profile_id}")
            data = response.json()
            self.profile_data = data.get('extracted_data', {})
            print(f"✅ Loaded profile: {data.get('profile_name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Error loading profile: {e}")
            return False

    def start_browser(self, url: str):
        """Start Chrome browser and navigate to URL"""
        try:
            chrome_options = ChromeOptions()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Suppress logging
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            self.driver = webdriver.Chrome(options=chrome_options)
            print(f"🌐 Opening: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            print("✅ Page loaded")
            return True
        except Exception as e:
            print(f"❌ Error starting browser: {e}")
            return False

    def fill_form(self) -> int:
        """Fill all form fields with profile data"""
        if not self.profile_data:
            print("❌ No profile data loaded")
            return 0

        try:
            # Find all form fields
            inputs = self.driver.find_elements(By.CSS_SELECTOR,
                "input[type='text'], input[type='email'], input[type='tel'], input[type='number'], textarea, select"
            )

            print(f"🔍 Found {len(inputs)} form fields")

            # Fill each field
            for input_elem in inputs:
                self._try_fill_field(input_elem)

            # Check checkboxes for job preferences
            self._check_job_checkboxes()

            print(f"✅ Filled {len(self.filled_fields)} fields")
            return len(self.filled_fields)

        except Exception as e:
            print(f"❌ Error filling form: {e}")
            return 0

    def _try_fill_field(self, element):
        """Try to match and fill a single field"""
        try:
            # Get field identifiers
            field_name = element.get_attribute('name') or element.get_attribute('id') or ""
            field_placeholder = element.get_attribute('placeholder') or ""
            field_label = self._get_field_label(element)
            
            combined_name = f"{field_name} {field_placeholder} {field_label}".lower()

            # Try to match with profile data
            value = self._find_matching_value(combined_name)

            if value:
                # Fill the field
                element.clear()
                element.send_keys(str(value))
                
                # Trigger change events
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
                
                self.filled_fields.append((field_name, value))
                print(f"  ✓ {field_name}: {value if len(str(value)) < 30 else str(value)[:30] + '...'}")

        except Exception as e:
            # Field might not be fillable, skip it
            pass

    def _get_field_label(self, element) -> str:
        """Get the label associated with a form field"""
        try:
            # Try to find associated label
            elem_id = element.get_attribute('id')
            if elem_id:
                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{elem_id}']")
                return label.text

            # Check aria-label
            aria_label = element.get_attribute('aria-label')
            if aria_label:
                return aria_label

            # Check parent label
            parent = element.find_element(By.XPATH, "..")
            try:
                label = parent.find_element(By.TAG_NAME, "label")
                return label.text
            except:
                pass

            return ""
        except:
            return ""

    def _find_matching_value(self, field_name: str) -> Optional[str]:
        """Find matching value in profile data"""
        field_name = field_name.lower()

        # Define field patterns
        patterns = {
            r'first[_\s]?name|firstname|given|fname|first': self.profile_data.get('first_name'),
            r'last[_\s]?name|lastname|family|lname|last|surname': self.profile_data.get('last_name'),
            r'email|email[_\s]?address|e-mail': self.profile_data.get('email'),
            r'phone|mobile|telephone|cell|contact': self.profile_data.get('phone'),
            r'address|street|location|city': self.profile_data.get('address'),
            r'city|town': self.profile_data.get('city'),
            r'state|province|region': self.profile_data.get('state'),
            r'zip|postal|postcode': self.profile_data.get('zip'),
            r'skills|expertise|specialties|competencies': self._format_skills(),
            r'experience|years|background|summary': self.profile_data.get('experience'),
            r'education|degree|school|university|college': self.profile_data.get('education'),
            r'salary|compensation|rate|pay': self.profile_data.get('salary'),
            r'linkedin|linkedin[_\s]?url|profile[_\s]?url|website': self.profile_data.get('linkedin_url'),
            r'cover|letter|about|summary|bio': self.profile_data.get('cover_letter'),
        }

        # Match patterns
        import re
        for pattern, value in patterns.items():
            if value and re.search(pattern, field_name):
                return value

        return None

    def _format_skills(self) -> str:
        """Format skills list as string"""
        skills = self.profile_data.get('skills', [])
        if isinstance(skills, list):
            return ', '.join(skills)
        return str(skills) if skills else None

    def _check_job_checkboxes(self):
        """Check common job preference checkboxes"""
        try:
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            
            for checkbox in checkboxes:
                name = (checkbox.get_attribute('name') or checkbox.get_attribute('id') or "").lower()
                
                # Check job type preferences
                if any(word in name for word in ['full', 'willing', 'agree', 'terms', 'accept', 'remote', 'relocate']):
                    if not checkbox.is_selected():
                        checkbox.click()
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", checkbox)
                        print(f"  ✓ Checked: {name}")
        except Exception as e:
            pass

    def take_screenshot(self, filename: str = "form_filled.png"):
        """Take screenshot of filled form"""
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving screenshot: {e}")

    def submit_form(self, auto_submit: bool = False):
        """Find and optionally submit the form"""
        try:
            # Find submit button
            submit_button = None
            
            # Try different selectors
            selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Submit')",
                "button:contains('Apply')",
                "button:contains('Next')",
            ]

            for selector in selectors:
                try:
                    if "contains" in selector:
                        # XPath for contains
                        xpath = f"//{selector.split(':')[0]}[contains(text(), '{selector.split(\"'\")[1]}')]"
                        submit_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if submit_button:
                        break
                except:
                    continue

            if submit_button:
                print(f"🔘 Found submit button")
                if auto_submit:
                    print("📤 Submitting form...")
                    submit_button.click()
                    time.sleep(2)
                    print("✅ Form submitted!")
                else:
                    print("⏳ Form ready. Click submit button to continue")
                return True
            else:
                print("⚠️  Submit button not found")
                return False

        except Exception as e:
            print(f"❌ Error finding submit button: {e}")
            return False

    def wait_for_user(self):
        """Wait for user to complete any additional manual steps"""
        print("\n" + "="*50)
        print("🤖 Form filling complete!")
        print("="*50)
        print("👉 Review the filled form in the browser")
        print("👉 Make any manual corrections if needed")
        print("👉 Click Submit to apply")
        print("\nPress Enter to close browser and continue...")
        input()

    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🚪 Browser closed")

    def run(self, url: str, auto_submit: bool = False, wait: bool = True):
        """Run the complete form filling process"""
        print("\n" + "="*50)
        print("🤖 JOB FORM AUTO-FILLER")
        print("="*50 + "\n")

        # Load profile
        if not self.get_profile_data():
            return False

        # Start browser
        if not self.start_browser(url):
            return False

        # Fill form
        filled_count = self.fill_form()

        if filled_count > 0:
            # Take screenshot
            self.take_screenshot()

            # Check for submit button
            self.submit_form(auto_submit=auto_submit)

            # Wait for user if requested
            if wait and not auto_submit:
                self.wait_for_user()

        # Close browser
        self.close_browser()

        return True


# Command-line interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automatically fill job application forms")
    parser.add_argument("profile_id", help="Profile ID to use (find with: list-profiles command)")
    parser.add_argument("url", help="Job posting URL to fill (e.g., https://linkedin.com/jobs/view/123)")
    parser.add_argument("--auto-submit", action="store_true", help="Automatically submit the form")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for user review")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    # Run filler
    filler = JobFormFiller(args.profile_id, headless=args.headless)
    filler.run(args.url, auto_submit=args.auto_submit, wait=not args.no_wait)
