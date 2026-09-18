#!/usr/bin/env python3
"""
Google Drive Permanent Authentication Setup Helper for GitHub Actions
======================================================================
This tool helps you configure permanent, non-expiring Google Drive access
for personal Google accounts (e.g., 5TB Google One / Drive storage) to run
Binance historical data archival workflows on GitHub Actions.

Why Rclone's Built-in Client is the Best Solution:
--------------------------------------------------
1. Rclone has its own official, Google-verified OAuth Client ID built right in.
2. It is permanently "In Production" and approved by Google.
3. The refresh token it generates for your personal account NEVER EXPIRES.
4. You don't need any domain, branding, or Google Cloud verification.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path


def find_rclone() -> str:
    """Finds rclone executable either in PATH or in standard WinGet directory."""
    rclone_path = shutil.which("rclone")
    if rclone_path:
        return rclone_path

    # Check WinGet standard package location
    winget_rclone = Path(os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.75.1-windows-amd64\rclone.exe"
    ))
    if winget_rclone.exists():
        return str(winget_rclone)

    # Search LocalAppData generally
    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    for p in local_app_data.glob("**/rclone.exe"):
        if p.is_file():
            return str(p)

    return ""


def main():
    print("=" * 80)
    print("  GOOGLE DRIVE PERMANENT AUTHENTICATION SETUP HELPER")
    print("=" * 80)

    rclone_bin = find_rclone()
    if not rclone_bin:
        print("[!] Rclone was not found on your system.")
        print("    Please run: winget install Rclone.Rclone")
        return

    print(f"[+] Found Rclone installed at:\n    {rclone_bin}")

    # Standard rclone config path
    if os.name == "nt":
        appdata = os.environ.get("APPDATA", "")
        conf_path = Path(appdata) / "rclone" / "rclone.conf"
    else:
        conf_path = Path.home() / ".config" / "rclone" / "rclone.conf"

    if conf_path.exists():
        content = conf_path.read_text(encoding="utf-8")
        if "[gdrive]" in content and "refresh_token" in content:
            print("\n[+] SUCCESS! An active Google Drive remote '[gdrive]' was found in your rclone.conf:")
            print("-" * 80)
            print(content.strip())
            print("-" * 80)
            print("\n>>> NEXT STEP (Copy this to GitHub Secrets):")
            print("1. Open your repository: https://github.com/SamratSinghPhysicist/KCEX_bot/settings/secrets/actions")
            print("2. Click 'New repository secret'")
            print("3. Name  : RCLONE_CONFIG")
            print("4. Secret: Paste the content above")
            print("5. Click 'Add secret'. You are done!")
            return

    print("\n" + "-" * 80)
    print("NO GOOGLE DRIVE REMOTE CONFIGURED YET")
    print("-" * 80)
    print("""
To connect your Google Drive with a PERMANENT, NON-EXPIRING token
(without needing domains, branding, or Google Cloud verification):

Run this single command in your PowerShell or Command Prompt:

& "{rclone_bin}" config

Then follow these simple prompts:
  1. Press 'n' for New remote
  2. Name: gdrive
  3. Storage type: drive (or enter the number for Google Drive)
  4. client_id: <PRESS ENTER to leave blank - uses Rclone's verified client>
  5. client_secret: <PRESS ENTER to leave blank>
  6. scope: 1 (Full access to all files)
  7. root_folder_id: <PRESS ENTER to leave blank>
  8. service_account_file: <PRESS ENTER to leave blank>
  9. Edit advanced config: n
 10. Use auto config: y
     -> Your web browser will open.
     -> Log into your personal Google account (samratddypppis@gmail.com).
     -> Click 'Allow'.
 11. Configure as a team drive: n
 12. Keep this 'gdrive' remote: y
 13. Press 'q' to quit config.

Once done, run:
    python setup_gdrive_auth.py
It will print your exact GitHub secret ready to copy!
""".format(rclone_bin=rclone_bin))


if __name__ == "__main__":
    main()
