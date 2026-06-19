#!/usr/bin/env python3
"""
Helper CLI tool for managing profiles and running the auto-filler bot
"""

import sys
import requests
import subprocess
from datetime import datetime

API_BASE_URL = "http://localhost:8000"


class FormFillerCLI:
    """Command-line interface for form filler"""

    @staticmethod
    def check_server():
        """Check if backend server is running"""
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Backend server is running\n")
                return True
        except:
            pass
        
        print("❌ Backend server is NOT running!")
        print("   Start it with: cd backend && python -m uvicorn app.main:app --reload\n")
        return False

    @staticmethod
    def list_profiles():
        """List all available profiles"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/profiles")
            profiles = response.json().get('profiles', [])
            
            if not profiles:
                print("📭 No profiles found!\n")
                print("📤 Upload your resume first:")
                print("   1. Open http://localhost:3000/job-application-form.html")
                print("   2. Click 'Upload Your Resume'")
                print("   3. Select your resume file\n")
                return

            print("📋 AVAILABLE PROFILES\n" + "="*50)
            for i, profile in enumerate(profiles, 1):
                print(f"\n{i}. {profile['profile_name']}")
                print(f"   ID: {profile['profile_id']}")
                data = profile.get('extracted_data', {})
                if data.get('first_name'):
                    print(f"   Name: {data.get('first_name')} {data.get('last_name', '')}")
                if data.get('email'):
                    print(f"   Email: {data.get('email')}")
                if data.get('phone'):
                    print(f"   Phone: {data.get('phone')}")
                if data.get('skills'):
                    skills = data.get('skills', [])
                    if isinstance(skills, list):
                        print(f"   Skills: {', '.join(skills[:3])}...")
            
            print("\n" + "="*50 + "\n")

        except Exception as e:
            print(f"❌ Error listing profiles: {e}\n")

    @staticmethod
    def fill_form(profile_id: str, url: str, auto_submit: bool = False, headless: bool = False):
        """Fill a job form"""
        print(f"\n🚀 Starting form filler...\n")
        
        # Build command
        cmd = [
            sys.executable,
            "auto_form_filler.py",
            profile_id,
            url
        ]
        
        if auto_submit:
            cmd.append("--auto-submit")
        
        if headless:
            cmd.append("--headless")

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("\n❌ Form filler encountered an error")
        except FileNotFoundError:
            print("❌ auto_form_filler.py not found!")

    @staticmethod
    def show_help():
        """Show help menu"""
        help_text = """
╔═══════════════════════════════════════════════════════════════╗
║         JOB APPLICATION AUTO-FILLER CLI TOOL                 ║
╚═══════════════════════════════════════════════════════════════╝

COMMANDS:
  python cli.py check          - Check if backend is running
  python cli.py list           - List all profiles
  python cli.py fill <ID> <URL> - Fill a job form
  python cli.py help           - Show this help

EXAMPLES:

1. Check server status:
   python cli.py check

2. List your resume profiles:
   python cli.py list

3. Fill a LinkedIn job form:
   python cli.py fill abc123 https://linkedin.com/jobs/view/12345

4. Fill and auto-submit:
   python cli.py fill abc123 https://indeed.com/jobs?q=python --auto-submit

5. Run in headless mode (no browser window):
   python cli.py fill abc123 https://example.com/apply --headless

WORKFLOW:

Step 1: Start Backend Server
   cd backend
   python -m uvicorn app.main:app --reload

Step 2: Upload Your Resume
   Open: http://localhost:3000/job-application-form.html
   Upload your resume (PDF or TXT)
   Remember the profile ID or name

Step 3: Find Profile ID
   python cli.py list

Step 4: Fill Job Forms Automatically
   python cli.py fill <PROFILE_ID> <JOB_URL>

Step 5: Review and Submit
   Review the filled form in the browser
   Click Submit button

FLAGS:

--auto-submit       Automatically submit form after filling
--headless          Run browser in headless mode (no window)

SUPPORTED WEBSITES:

✅ LinkedIn Jobs
✅ Indeed.com
✅ Glassdoor
✅ Monster.com
✅ Dice.com
✅ Company career pages
✅ Any website with job forms

TROUBLESHOOTING:

Q: Backend not responding?
A: cd backend && python -m uvicorn app.main:app --reload

Q: No profiles found?
A: Upload your resume at http://localhost:3000

Q: Form not filling?
A: Make sure backend is running and profile ID is correct

Q: Browser won't open?
A: Install: pip install selenium

For more help, check: https://github.com/your-repo
"""
        print(help_text)


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Job Application Auto-Filler CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Check command
    subparsers.add_parser("check", help="Check if backend is running")

    # List command
    subparsers.add_parser("list", help="List all profiles")

    # Help command
    subparsers.add_parser("help", help="Show help")

    # Fill command
    fill_parser = subparsers.add_parser("fill", help="Fill a job form")
    fill_parser.add_argument("profile_id", help="Profile ID to use")
    fill_parser.add_argument("url", help="Job URL to fill")
    fill_parser.add_argument("--auto-submit", action="store_true", help="Auto-submit form")
    fill_parser.add_argument("--headless", action="store_true", help="Headless mode")

    args = parser.parse_args()

    if not args.command or args.command == "help":
        FormFillerCLI.show_help()
        return

    if args.command == "check":
        FormFillerCLI.check_server()
        FormFillerCLI.list_profiles()

    elif args.command == "list":
        if not FormFillerCLI.check_server():
            return
        FormFillerCLI.list_profiles()

    elif args.command == "fill":
        if not FormFillerCLI.check_server():
            return
        FormFillerCLI.fill_form(
            args.profile_id,
            args.url,
            auto_submit=args.auto_submit,
            headless=args.headless
        )


if __name__ == "__main__":
    main()
